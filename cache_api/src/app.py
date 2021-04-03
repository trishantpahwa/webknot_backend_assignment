from setup import setup

setup()
from functools import wraps
from flask import Flask, request, make_response, jsonify
import json
import requests
from os import environ


cached_ifsc = {}
ifsc_hit_count = {}
path_hit_count = {}


def path_hit_counter():
    def _path_hit_counter(f):
        @wraps(f)
        def __path_hit_counter(*args, **kwargs):
            if request.path in path_hit_count:
                path_hit_count[request.path] += 1
            else:
                path_hit_count[request.path] = 0
            result = f(*args, **kwargs)
            return result
        return __path_hit_counter
    return _path_hit_counter


app = Flask(__name__)


@app.route('/ifsc-search', methods=['GET'])
@path_hit_counter()
def ifsc_search():
    print(path_hit_count)
    print(ifsc_hit_count)
    ifsc_code = request.args.get('ifsc_code')
    if ifsc_code in cached_ifsc:
        ifsc_hit_count[ifsc_code] += 1  # Would be present, because can only be cached if searched once.
        return make_response(jsonify({'Success': True, 'data': cached_ifsc[ifsc_code]}))
    else:
        response = requests.get(
            environ['BACKEND_API_URL'] + '/ifsc-search?ifsc_code=' + ifsc_code)
        if response.status_code == 200:
            data = json.loads(response.text)
            cached_ifsc[data['data']['IFSC']] = data['data']
            ifsc_hit_count[ifsc_code] = 1  # Would only be called once per ifsc as they'll be cached.
            return make_response(jsonify(data))
        elif response.status_code == 404:
            return make_response(jsonify({}))
