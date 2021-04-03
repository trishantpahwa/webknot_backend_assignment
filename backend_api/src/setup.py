from os import environ, path



def setup():
    if environ.get('DATASTORE') is None:
        datastore = path.abspath(input(
            'Enter path to datastore or set environment variable["DATASTORE"]: '))
        environ['DATASTORE'] = datastore
