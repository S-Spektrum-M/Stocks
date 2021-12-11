"""
A Share Trading API built on flask
Check out the github README for docs
https://github.com/S-Spektrum-M/Stocks
"""
import stats as st
import flask
import json
from flask import request, jsonify

APP = flask.Flask(__name__)
# app.config["DEBUG"] = True

@APP.route('/api/short/multi', methods=['GET'])
def short_multi():
    """Return JSON representing return"""
    if 'params' in request.args:
        params = request.args['params']
        params_list = params.split(',')
        if len(params_list) < 500:
            ret_list = []
            for param in params_list:
                if param.isalpha():
                    response = st.short(param.upper())
                    if response is not None:
                        ret_list.append({
                            param: response
                        })
                    else:
                        ret_list.append({
                            "error": "bad_id",
                            "bad_id": param
                        })
                else:
                    ret_list.append({
                        "error": "bad_id",
                        "bad_id": param
                    })
            return jsonify(ret_list), 200
        return jsonify({
            "error": "too long",
            "size": len(params_list)
        })
    return jsonify({
        "error": "no_param"
    }), 404

@APP.route('/api/short', methods=['GET'])
def short():
    """Return JSON representing return"""
    if 'id' in request.args:
        ticker = str(request.args['id'])
        if ticker.isalpha():
            response = st.short(ticker.upper()) # Upper case for better DB Caching
            if response is not None:
                return jsonify({
                    'upper': response[0],
                    'lower': response[1]
                }), 200
            return jsonify({
                "error": "bad_id"
            }), 404
        return jsonify({
            "error": "no_id"
        }), 400

    else:
        return jsonify({
            "error": "no_id"
        }), 400

@APP.route('/api/long/multi', methods=['GET'])
def long_multi():
    """Return JSON representing return"""
    if 'params' in request.args:
        params = request.args['params']
        params_list = params.split(',')
        ret_list = []
        for param in params_list:
            if param.isalpha():
                response = st.long(param.upper())
                if response != None:
                    ret_list.append({
                        param: response
                    })
            else:
                ret_list.append({
                    "error": "bad_id",
                    "bad_id": param
                }), 404
        return jsonify(ret_list), 200
    else:
        return jsonify({
            "error": "no_id"
        }), 404

@APP.route('/api/long', methods=['GET'])
def long():
    """Return JSON representing return"""
    if 'id' in request.args:
        id = str(request.args['id'])
        if id.isalpha():
            response = st.long(id.upper())
            if response != None:
                return jsonify({
                    'upper': response[0],
                    'lower': response[1]
                }), 200
            else:
                return jsonify({
                    "error": "bad_id"
                }), 404
        else:
            return jsonify({
                "error": "no_id"
            }), 400
    else:
        return jsonify({
            "error": "no_id"
        }), 400

@APP.route('/api/current')
def current():
    """Return JSON representing return"""
    if 'id' in request.args:
        ticker = str(request.args['id'])
        if ticker.isalpha():
            respone = st.current(ticker)
            if respone is not None:
                return jsonify({
                    'current_price':  respone
                })
            return jsonify({
                "error": "bad_id"
            }), 404
        return jsonify({
            "error": "bad_id"
        }), 404
    return jsonify({
        "error": "no_id"
    }), 400

APP.run(host="localhost", port=8080, debug=True)
