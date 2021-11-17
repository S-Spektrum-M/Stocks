import json
import numpy as np
import stats as st
from robin_stocks import robinhood as rh
import auth
import flask
from flask import request, jsonify

app = flask.Flask(__name__)
# app.config["DEBUG"] = True

@app.route('/api/short/', methods=['GET'])
def short():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = str(request.args['id'])
        a = st.short_linear_reg(id)
        if (len(a)) == 3:
            return jsonify('bad request')
        else:
            return jsonify({
                'upper': response[0],
                'lower': response[1]
            })
    else:
        return "Error: No id field provided. Please specify an id."

@app.route('/api/long/', methods=['GET'])
def long():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = str(request.args['id'])
        response  = st.long_linear_reg(id)
        if (len(response)) == 3:
            return jsonify('bad request')
        else:
            return jsonify({
                'upper': response[0],
                'lower': response[1]
            })
    else:
        return "Error: No id field provided. Please specify an id."

app.run(host="localhost", port=8080, debug=True)
