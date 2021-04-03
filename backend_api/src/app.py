from setup import setup

setup()


from flask import Flask, request, make_response, jsonify
import json
from sys import exc_info
from models.ifsc import ifsc, load_ifsc_data, search_ifsc
from models.leaderboard import leaderboard
from models.statistics import statistics


ifsc_data = load_ifsc_data()

leaderboard_data = leaderboard()
leaderboard_data.load_bank_leaderboard_data()

statistics_data = statistics()


app = Flask(__name__)


@app.route('/ifsc-search', methods=['GET'])
def ifsc_search():
    try:
        ifsc_code = request.args.get('ifsc_code')
        if ifsc_code is not None and ifsc_code != '':
            branch_data = search_ifsc(ifsc_data, ifsc_code)
            if branch_data is not None or ifsc_code == '':
                statistics_data.search(ifsc_code)
                return make_response(jsonify({'Success': True, 'data': branch_data}))
            else:
                return make_response(jsonify({'Success': False}), 404)
        else:
            return make_response(jsonify({'Success': False, 'error': 'Validation Error', 'message': 'ifsc_code validation error'}), 422)
    except Exception as e:
        print("Oops!", e, "occurred.")
        return make_response(jsonify({'Success': False, 'error': 'Internal Server Error'}), 500)


@app.route('/leaderboard', methods=['GET'])
def bank_leaderboard():
    try:
        sortorder = request.args.get('sortorder')
        fetchcount = request.args.get('fetchcount')
        __statistics_data = None

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
    try:
        sortorder = request.args.get('sortorder')
        fetchcount = int(request.args.get('fetchcount')
                         ) if request.args.get('fetchcount') else None
        __statistics_data = None
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
        return make_response(jsonify({'Success': True, 'data': __statistics_data}))
    except Exception as e:
        print("Oops!", e, "occurred.")
        return make_response(jsonify({'Success': False, 'error': 'Internal Server Error'}), 500)
