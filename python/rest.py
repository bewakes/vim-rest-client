import requests
import json
import re
import vim

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


def get_lines_for(tag, lines):
    tag = tag.lower()

    if not lines[0].replace(' ', '').lower() == '<{}>'.format(tag):
        raise Exception('Expected tag <{}>'.format(tag))

    nextstart = 0
    relevant_lines = []

    for i, line in enumerate(lines[1:]):
        if line.strip().replace(' ', '').lower() == '</{}>'.format(tag):
            nextstart = i + 2  # +2 because we start from index 1 (lines[1:])
            break
        relevant_lines.append(line)
    else:
        raise Exception('No end tag for <{}>'.format(tag))

    return relevant_lines, nextstart


def parse_headers(headerstr):
    headers = {}
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


def to_vim_str(name, val):
    vim.command(r'let {} = "{}"'.format(name, val))


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
                print('FIRST LINE IS NONE')
                raise Exception("Invalid request block")

        # NOW FIND LAST line
        lastline = None
        for i in range(linenum, len(lines)):
            line = lines[i].strip()
            lastline = i-1
            if line and line.split()[0] in METHODS:
                break

        relevant_lines = lines[firstline:lastline+1]

        request_block = '\n'.join(relevant_lines)

        # Now regex match to find different blocks
        # First match body and non body parts
        match = re.match('(.*)\n\n\n(.*)', request_block)
        if not match:
            # Means no body present
            method_and_header = request_block
            bodystr = ''
        else:
            method_and_header = match.group(1)
            bodystr = match.group(2)
        # Now match method and header
        match = re.match('(.*)\n\n(.*)', method_and_header)
        if not match:
            # NO header
            headerstr = ''
            method_uri = method_and_header
        else:
            headerstr = match.group(2)
            method_uri = match.group(1)

        method, url = method_uri.strip().split()
        headers = parse_headers(headerstr)

        body = parse_body(bodystr, headers)

        requests_kwargs = {}
        if method.lower() == 'get':
            requests_kwargs['params'] = body
        else:
            requests_kwargs['data'] = body

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
