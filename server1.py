import boto3
import cloudpickle as cp
import flask
from flask import session
from flask_session import Session
from threading import Thread
import uuid
import utils

OBJ_ID = 0

import pyblas

app = flask.Flask(__name__)


@app.route('/connect', methods=['POST'])
def connect():

    flask.session['dict'] = {}
    return construct_response()




@app.route('/vector', methods=['POST'])
def vector():
    args = cp.loads(flask.request.get_data())
    vec = pyblas.Vector(args)

    flask.session['dict'][OBJ_ID] = vec

    resp = OBJ_ID
    OBJ_ID += 1

    return construct_response(resp)


app.route('/vector/request', methods=['POST'])
def vector_request():
    call = cp.loads(flask.request.get_data())
    obj_id = call[0]
    fname = call[1]
    args = call[2]

    vec = flask.session['dict'][obj_id]
    handle = getattr(vec, fname)
    ret = handle(*args)

    return construct_response(ret)




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
