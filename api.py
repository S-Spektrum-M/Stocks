import stats as st
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
        if id.isalpha():
            response = st.short(id)
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
                "error": "bad_id"
            }), 404
    else:
        return "Error: No id field provided. Please specify an id.", 404

@app.route('/api/long/', methods=['GET'])
def long():
    # Check if an ID was provided as part of the URL.
    # If ID is provided, assign it to a variable.
    # If no ID is provided, display an error in the browser.
    if 'id' in request.args:
        id = str(request.args['id'])
        if id.isalpha() == None:
            response = st.long(id)
            return jsonify({
                'upper': response[0],
                'lower': response[1]
            }), 200
        else:
            return jsonify({
                "error": "bad_id"
            }), 404
    else:
        return "Error: No id field provided. Please specify an id.", 404

app.run(host="localhost", port=8080, debug=True)
