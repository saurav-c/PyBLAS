import cloudpickle as cp
import flask
from flask import session
from flask_session import Session

import ublas

app = flask.Flask(__name__)

@app.route('/connect', methods=['POST'])
def connect():
    return construct_response()

@app.route('/execute', methods=['POST'])
def execute():
    data_bin = flask.request.get_data()
    data = cp.loads(data_bin)
    funcname = data[0]
    args = data[1]

    return construct_response()

def construct_response(obj=None):
    resp = flask.make_response()
    if obj != None:
        resp.data = cp.dumps(obj)
        resp.content_type = 'text/plain'

    resp.status_code = 200

    return resp

def return_error(error=''):
    resp = flask.make_response()
    if error != '':
        resp.data = error
        resp.content_type = 'text/plain'

    resp.status_code = 400

    return resp

def run():
    app.secret_key = "this is a secret key"
    app.config['SESSION_TYPE'] = 'filesystem'
    Session(app)
    app.run(threaded=True, host='0.0.0.0', port=7000)

run()
