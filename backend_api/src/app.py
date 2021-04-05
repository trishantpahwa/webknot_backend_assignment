from dotenv import load_dotenv
load_dotenv()


from flask import Flask, request, make_response, jsonify
import json
from sys import exit
from os import environ
from models.ifsc import ifsc, load_ifsc_data, search_ifsc
from models.leaderboard import leaderboard
from models.statistics import statistics

try:
    for env_check in ['DATASTORE', 'HOST', 'PORT', 'DEV_MODE']:
        if env_check not in environ:
            raise Exception('Setup env variables first: ' + env_check)
except Exception as e:
    print(e)
    exit(1)


'''
    Loads the data from the excel to the primary memory

    [|==== Loading =========>.......|]

    data_structures
     - ifsc_data: dict(<str>, <ifsc object>)
     - leaderboard_data: dict(<str>, <int>)
     - statistics_data
'''

ifsc_data = load_ifsc_data()  # Loads IFSC data

leaderboard_data = leaderboard()  # init leaderboard
leaderboard_data.load_bank_leaderboard_data()  # Loads the leaderboard

statistics_data = statistics()  # init statistics


app = Flask(__name__)


@app.route('/ifsc-search', methods=['GET'])
def ifsc_search():
    '''
        summary: Search details of a bank's branch using an IFSC code. [Backend]
        description: Search details of a bank's branch using an IFSC code. [Backend]. Searches the IFSC Code within the loaded data from the excel document. If found updates the `statistics` about the search and logs the successful search.
        parameters: 
         - `ifsc_code`: (required) str
        responses:
         - 200:
            success: True
            description: Data corresponding to the IFSC code found and sent successfully.
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
            description: ifsc_code not provided
            schema: json({
                "Success": false,
                "error": "Validation Error",
                "message": "ifsc_code validation error"
            })
         - 500:
            success: False
            description: Unhandled exception has occurred. Probably we found a bug!
            schema: json({
                "Success": false,
                "error": "Internal Error",
            })
    '''
    try:
        ifsc_code = request.args.get('ifsc_code')
        if ifsc_code is not None and len(ifsc_code) == 11:
            branch_data = search_ifsc(ifsc_data, ifsc_code)
            if branch_data is not None or ifsc_code == '':
                statistics_data.search(ifsc_code)
                return make_response(jsonify({'Success': True, 'data': branch_data}))
            else:
                return make_response(jsonify({'Success': False, 'data': None}), 404)
        else:
            return make_response(jsonify({'Success': False, 'error': 'Validation Error', 'message': 'ifsc_code validation error'}), 422)
    except Exception as e:
        print("Oops!", e, "occurred.")
        return make_response(jsonify({'Success': False, 'error': 'Internal Server Error'}), 500)


@app.route('/leaderboard', methods=['GET'])
def bank_leaderboard():
    '''
        summary: To fetch list of banks with their branch count with sortorder and fetchcount to dynamically.
        description: Fetches the list of banks with their branch count. Allows to sort both in !@ ASC @! and !@ DESC @! and limit the amount of results using fetchcount.
        parameters:
         - `sortorder`: (optional) enum<str['ASC', 'DESC'])>
         - `fetchcount`: (optional) int
        resposnes:
         - 200:
            success: True
            description: Successfully returned list of banks and their branch counts in specified sortorder and limited by fetchcount
            schema: json({
                "Success": true,
                "data": [
                    {
                        "XXXXXXXXXXXXXX": 18500
                    },
                    {
                        "XXXXXXXXXXXXXX": 10037
                    },
                    .
                    .

                    .
                    .
                    {
                        "XXXXXXXXXXXXXX": 5242
                    }
                ]
            })
         - 422:
            success: False
            description: invalid sortorder value.
            schema: json({
                "Success": false,
                "error": "Validation Error",
                "message": "sortorder validation error"
            })
         - 422:
            success: False
            description: invalid fetchcount value.
            schema: json({
                "Success": false,
                "error": "Validation Error",
                "message": "fetchcount validation error"
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
        sortorder = request.args.get('sortorder')
        fetchcount = request.args.get('fetchcount')

        if sortorder != 'ASC' and sortorder != 'DESC' and sortorder != None:
            return make_response(jsonify({'Success': False, 'error': 'Validation Error', 'message': 'sortorder validation error'}), 422)
        if fetchcount is not None:
            try:
                fetchcount = int(fetchcount)
                if fetchcount < 1:
                    raise Exception()
            except Exception:
                return make_response(jsonify({'Success': False, 'error': 'Validation Error', 'message': 'fetchcount validation error'}), 422)

        if sortorder is not None:
            if fetchcount is not None:
                __leaderboard_data = leaderboard_data.get_leaderboard(
                    sortorder, fetchcount)
            else:
                __leaderboard_data = leaderboard_data.get_leaderboard(
                    sortorder)
        else:
            if fetchcount is not None:
                __leaderboard_data = leaderboard_data.get_leaderboard(
                    limit=fetchcount)
            else:
                __leaderboard_data = leaderboard_data.get_leaderboard()
        return make_response(jsonify({'Success': True, 'data': __leaderboard_data}))
    except Exception as e:
        print("Oops!", e, "occurred.")
        return make_response({'Success': False, 'error': 'Internal Server Error'}, 500)


@app.route('/statistics', methods=['GET'])
def statistics_route():
    '''
        summary: To fetch statistics of the 
        description: Allows to sort both in !@ ASC @! and !@ DESC @! and limit the amount of results using fetchcount.
        parameters:
         - `sortorder`: (optional) enum<str['ASC', 'DESC'])>
         - `fetchcount`: (optional) int
        resposnes:
         - 200:
            success: True
            description: Successfully returned list of banks and their branch counts in specified sortorder and limited by fetchcount
            schema: json({
                "Success": true,
                "data": [
                    {
                        "ifsc": "XXXX0000000",
                        "timestamp": 1617480129.377363
                    },
                    .
                    .
                    .

                    {
                        "ifsc": "XXXX0000000",
                        "timestamp": 1617480129.377363
                    },
                    {
                        "ifsc": "XXXX0000000",
                        "timestamp": 1617481567.3770797
                    },
                ]
            })
         - 422:
            success: False
            description: invalid sortorder value.
            schema: json({
                "Success": false,
                "error": "Validation Error",
                "message": "sortorder validation error"
            })
         - 422:
            success: False
            description: invalid fetchcount value.
            schema: json({
                "Success": false,
                "error": "Validation Error",
                "message": "fetchcount validation error"
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
        sortorder = request.args.get('sortorder')
        fetchcount = request.args.get('fetchcount')
        if sortorder != 'ASC' and sortorder != 'DESC' and sortorder != None:
            return make_response(jsonify({'Success': False, 'error': 'Validation Error', 'message': 'sortorder validation error'}), 422)
        if fetchcount is not None:
            try:
                fetchcount = int(fetchcount)
                if fetchcount < 1:
                    raise Exception()
            except Exception:
                return make_response(jsonify({'Success': False, 'error': 'Validation Error', 'message': 'fetchcount validation error'}), 422)

        if sortorder is not None:
            if fetchcount is not None:
                __statistics_data = statistics_data.get_data(
                    sortorder, fetchcount)
            else:
                __statistics_data = statistics_data.get_data(sortorder)
        else:
            if fetchcount is not None:
                __statistics_data = statistics_data.get_data(limit=fetchcount)
            else:
                __statistics_data = statistics_data.get_data()
        if len(__statistics_data) == 0:
            return make_response(jsonify({'Success': False, 'data': __statistics_data}))
        else:
            return make_response(jsonify({'Success': True, 'data': __statistics_data}))
    except Exception as e:
        print("Oops!", e, "occurred.")
        return make_response(jsonify({'Success': False, 'error': 'Internal Server Error'}), 500)


if __name__ == '__main__':
    app.run(host=environ['HOST'], port=environ['PORT'], debug=environ['DEV_MODE'])