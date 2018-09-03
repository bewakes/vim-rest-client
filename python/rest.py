import requests
import json
import vim


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


def get_headers(headerlines):
    headers = {}
    for x in headerlines:
        k, v = x.split(':')
        headers[k.strip()] = v.strip()
    return headers


def to_vim(name, val):
    vim.command(r'let {} = {}'.format(name, val))


def process_and_call(line, text):
    linenum = int(line)
    lines = [x for x in text.split('\n') if x.strip()]

    firstline = 0
    endline = 0

    try:
        for i, line in enumerate(lines):
            if line.strip().replace(' ', '').startswith('<request>'):
                if i <= linenum - 1:
                    firstline = i
            elif line.strip().replace(' ', '').startswith('</request>'):
                if i > linenum - 1:
                    endline = i
                    break
        if firstline >= endline:
            raise Exception('Request must be enclosed in <request> </request> tag')  # noqa

        relevant_lines = lines[firstline+1:endline]  # need not include borders
        # Strip off empty lines
        relevant_lines = [x for x in relevant_lines if x.strip() != '']

        # get header lines
        headerlines, methodstart = get_lines_for('header', relevant_lines)

        # get method lines
        methodlines, bodystart = get_lines_for(
            'method',
            relevant_lines[methodstart:]
        )

        # get body lines
        bodylines, _ = get_lines_for(
            'body',
            relevant_lines[methodstart+bodystart:]
        )
        # TODO: check for optional body

        headers = get_headers(headerlines)
        method, url = methodlines[0].strip().split()

        # body = get_body(headers, bodylines)
    except Exception as e:
        output = {
            'error': 1,
            'message': e.args[0]
        }
    else:
        # now we are ready for sending request
        request_method = getattr(requests, method.lower())

        # NOTE: now, this is for get only
        resp = request_method(url, headers=headers)

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
    to_vim('vim_rest_client_data', output)
