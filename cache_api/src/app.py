from setup import setup
'''
    TODO: use dotenv for quicker and deployment.
'''
setup()
from functools import wraps
from flask import Flask, request, make_response, jsonify
import json
import requests
from os import environ


'''
    ==== GLOBALS ====
    description: GLOBALS to store datastructures in primary memory.
    data_structures:
     - cached_ifsc: Caches searched ifsc. | dict(<str>,dict>)
     - ifsc_hit_count: Logs the count for ifsc_codes searched for. | dict(<str>,<int>)
     - path_hit_count: Logs the paths http request was made for. | dict(<str>,<int>)
'''
cached_ifsc = {}
ifsc_hit_count = {}
path_hit_count = {}


def path_hit_counter():
    '''
        summary: Middleware to count url hits [Django App 4.]
        description: Counts url hits and logs them in a dictionary | `path_hit_count`
        parameters: 
         - `request.path`: Flask.request.path
         - `path_hit_count`: global dict(<str>,<int>)
    '''
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
@path_hit_counter()  # Call to middleware to log path.
def ifsc_search():
    '''
        summary: Search details of a bank's branch using an IFSC code. [Frontend]
        description: Search details of a bank's branch using an IFSC code. [Frontend]. Queries to the backend_api to receive data about a particular bank's branch corresponding to the entered ifsc_code, if it exists.
        parameters: 
         - `ifsc_code`: (required) str
        responses:
         - 200:
            success: True
            description: Successfully returned data, either cached or fetched from the backend
            schema: json({
                "Success": True,
                "data": {
                    "ADDRESS": "XXXXXXXXXXXXXXXXXXXX",  # Address of a branch
                    "BANK": "XXXXXXXXXXXXXXXXXXXX",  # Name of the bank
                    "BRANCH": "XXXXXXXXXXXXXXXXXXXX",  # Name of the bank's branch
                    "CITY": "XXXXXXXXXXXXXXXXXXXX",  # City where the bank's branch is located
                    "CONTACT": 0000000,  # Contact of the branch
                    "DISTRICT": "XXXXXXXXXXXXXXXXXXXX",  # District where the bank's branch is located
                    "IFSC": "XXXXXXXXXXXXXXXXXXXX",  # IFSC Code of the branch
                    "MICR CODE": 123456789,  # MICR Code of the branch
                    "STATE": "XXXXXXXXXXXXXXXXXXXX",  # State where the bank's branch is located
                    "STD_CODE": 1  # Code of the state where the bank's branch is located
                }
            })
         - 404:
            success: False
            description: No data found from provided ifsc_code
            schema: json({
                "Success": False,
                "data": null
            })
         - 422:
            success: False
            description: The ifsc_code provided at input's length is not 11.
            schema: json({
                "Success": false,
                "error": "Validation Error",
                "message": "Invalid ifsc_code"
            })
        - 422:
            success: False
            description: ifsc_code not provided
            schema: json({
                "Success": false,
                "error": "Validation Error",
                "message": "ifsc_code is required"
            })
         - 500:
            success: False
            description: Unhandled exception has occurred. Probably we found a bug!
            schema: json({
                "Success": false,
                "error": "Internal Error"
            })
    '''
    try:
        ifsc_code = request.args.get('ifsc_code')
        if ifsc_code is not None and len(ifsc_code) != 11 and str(ifsc_code[:4]).isalpha() and str(ifsc_code[4:]).isdigit():
            if ifsc_code in cached_ifsc:
                ifsc_hit_count[ifsc_code] += 1  # Would be present, because can only be cached if searched once.
                return make_response(jsonify({'Success': True, 'data': cached_ifsc[ifsc_code]}))
            else:
                response = requests.get(
                    environ['BACKEND_API_URL'] + '/ifsc-search?ifsc_code=' + ifsc_code)  # Fetch data from backend here
                if response.status_code == 200:
                    data = json.loads(response.text)
                    cached_ifsc[data['data']['IFSC']] = data['data']
                    ifsc_hit_count[ifsc_code] = 1  # Would only be called once per ifsc as they'll be cached.
                    return make_response(jsonify(data))
                elif response.status_code == 404:
                    return make_response(jsonify(json.loads(response.text)))
        else:
            if ifsc_code is None:
                return make_response(jsonify({'Success': False, 'error': 'Validation Error', 'message': 'ifsc_code is required'}), 422)
            else:
                return make_response(jsonify({'Success': False, 'error': 'Validation Error', 'message': 'Invalid ifsc_code'}), 422)
    except Exception as e:
        print("Oops!", e, "occurred.")
        return make_response(jsonify({'Success': False, 'error': 'Internal Server Error'}), 500)