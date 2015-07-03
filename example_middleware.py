from wsgiref.simple_server import make_server
from example_server import simple_app
def reverse_middleware(app):
    def wrapped_app(environ, start_response):
        response = app(environ, start_response)
        return [s[::-1] for s in response]
    return wrapped_app

CACHE_DICT = dict()

def cache_middleware(app):
    def wrapper(environ, start_response):
        if environ['PATH_INFO'] in CACHE_DICT.keys():
            return CACHE_DICT[environ['PATH_INFO']]
        else:
            response = app(environ, start_response)
            CACHE_DICT[environ['PATH_INFO']] = response
            return response

    return wrapper

if __name__ == '__main__':
    make_server('', 8000, cache_middleware(simple_app)).serve_forever()
