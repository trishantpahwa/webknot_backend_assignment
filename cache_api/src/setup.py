from os import environ



def setup():
    if environ.get('BACKEND_API_URL') is None:
        backend_api_url = input(
            'Enter url of backend_api or set environment variable["BACKEND_API_URL"]: ')
        environ['BACKEND_API_URL'] = backend_api_url
