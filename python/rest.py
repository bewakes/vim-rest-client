import requests
import json
import re

METHODS = [
    'GET', 'PUT', 'POST', 'DELETE', 'PATCH', 'OPTIONS',
]

STATUSES = {
    200: 'OK',
    201: 'CREATED',
    400: 'BAD REQUEST',
    404: 'NOT FOUND',
    500: 'SERVER ERROR',
    403: 'FORBIDDEN',
    401: 'UNAUTHENTICATED',
    502: 'GATWAY TIMEOUT',
}


def parse_headers(headerstr):
    headers = {}
    headerstr = headerstr.strip()
    if not headerstr:
        return headers
    for x in headerstr.split('\n'):
        k, v = x.split(':')
        headers[k.strip()] = v.strip()
    return headers


def parse_body(bodystr, headers):
    contenttype = headers.get('Content-Type')
    if contenttype == 'application/json':
        return json.loads(bodystr)
    else:
        return '&'.join([x.strip() for x in bodystr.split('\n')])


def save_result(result, path):
    error = result['error']
    with open(path, 'w') as f:
        if error:
            f.write("ERROR\n=====\n\n")
            f.write(result['message'])
            return
        f.write("RESPONSE\n========\n\n")
        f.write("{} {}\nStatus {} {}\n\n".format(
            result['method'], result['url'], result['status_code'],
            STATUSES.get(result['status_code'], '')
        ))
        f.write("HEADERS\n=======\n")
        f.write('\n'.join(
            ["{}: {}".format(k, v) for k, v in result['headers'].items()]
        ))
        f.write("\n\nBODY\n====\n")
        f.write(result['body'])
        f.write("\n")


def process_and_call(line, text, path):
    linenum = int(line)
    lines = [x for x in text.split('\n')]

    try:
        # FIRST FIND first line
        firstline = None
        for i in range(linenum-1, -1, -1):
            line = lines[i].strip()
            if line and line.split()[0] in METHODS:
                firstline = i
                break
        if firstline is None:
            raise Exception("Invalid request block")

        # NOW FIND LAST line
        lastline = linenum-1
        for i in range(linenum, len(lines)):
            line = lines[i].strip()
            if line and line.split()[0] in METHODS:
                break
            lastline = i

        relevant_lines = lines[firstline:lastline+1]

        request_block = '\n'.join(relevant_lines)

        # Now regex match to find different blocks
        # First match body and non body parts
        splitted = request_block.split('\n\n\n')
        if not len(splitted) > 1:
            # Means no body present
            method_and_header = request_block
            bodystr = ''
        else:
            method_and_header = splitted[0]
            bodystr = '\n'.join(splitted[1:])

        # Now match method and header
        splitted = method_and_header.split('\n\n')
        if not len(splitted) > 1:
            # NO header
            headerstr = ''
            method_uri = method_and_header
        else:
            method_uri = splitted[0]
            headerstr = '\n'.join(splitted[1:])

        method, url = method_uri.strip().split()
        headers = parse_headers(headerstr)

        body = parse_body(bodystr, headers)

        requests_kwargs = {}
        if method.lower() == 'get':
            requests_kwargs['params'] = body
        else:
            requests_kwargs['json'] = body

        # now we are ready for sending request
        request_method = getattr(requests, method.lower())

        resp = request_method(url, headers=headers, **requests_kwargs)
    except requests.exceptions.SSLError as e:
        output = {
            'error': 1,
            'message': 'SSL error occured. Maybe the certificate of the website expired or you don\'t have updated certificates'  # noqa
        }
    except requests.exceptions.ConnectionError as e:
        output = {
            'error': 1,
            'message': 'Connection Error occured.\nPerhaps the site does not exist or you do not have internet connection.'  # noqa
        }
    except Exception as e:
        import traceback
        print(traceback.format_exc())
        output = {
            'error': 1,
            'message': str(e.args[0])
        }
    else:
        respheaders = resp.headers
        contenttype = respheaders.get('Content-Type', 'text/html')

        result = resp.text

        if 'application/json' in contenttype:
            result = json.dumps(resp.json(), indent=4)

        output = {
            'error': 0,
            'url': url,
            'method': method.upper(),
            'status_code': resp.status_code,
            'headers': resp.headers,
            'body': result
            }
    # write result to file
    save_result(output, path)
