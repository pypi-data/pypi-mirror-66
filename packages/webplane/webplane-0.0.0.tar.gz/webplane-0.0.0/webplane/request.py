import cherrypy


def headers(name=None):
    request_headers = cherrypy.request.headers
    if str is None:
        return request_headers
    else:
        for header_name, header_value in request_headers.items():
            if header_name.lower() == name.lower():
                return request_headers[header_name]
