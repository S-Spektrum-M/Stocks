import stats as st
import flask
import json
from flask import request, jsonify

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

@app.route('/api/short/multi', methods=['GET'])
def short_multi():
    if 'params' in request.args:
        params = request.args['params']
        params_list = params.split(',')
        if len(params_list) < 500:
            ret_list = []
            for param in params_list:
                if param.isalpha():
                    response = st.short(param.upper())
                    if response != None:
                        ret_list.append({
                            param: {
                                'upper': response[0],
                                'lower': response[1]
                            }
                        })
                else:
                    return jsonify({
                        "error": "bad_id",
                        "bad_id": param
                    }), 404
            return jsonify(ret_list), 200
        else:
            return jsonify({
                "error": "too long",
                "size": len(params_list)
            })
    else:
        return jsonify({
            "error": "no_id"
        }), 404

@app.route('/api/short/', methods=['GET'])
def short():
    if 'id' in request.args:
        id = str(request.args['id'])
        if id.isalpha():
            response = st.short(id.upper())
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

@app.route('/api/long/multi', methods=['GET'])
def long_multi():
    if 'params' in request.args:
        params = request.args['params']
        params_list = params.split(',')
        ret_list = []
        for param in params_list:
            if param.isalpha():
                response = st.long(param.upper())
                if response != None:
                    ret_list.append({
                        param: {
                            'upper': response[0],
                            'lower': response[1]
                        }
                    })
            else:
                return jsonify({
                    "error": "bad_id",
                    "bad_id": param
                }), 404
        return jsonify(ret_list), 200
    else:
        return jsonify({
            "error": "no_id"
        }), 404

@app.route('/api/long/', methods=['GET'])
def long():
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

app.run(host="localhost", port=8080, debug=True)
