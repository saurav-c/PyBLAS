import cloudpickle as cp
import flask
from flask import session
from flask_session import Session
from threading import Thread
import uuid

import pyblas

app = flask.Flask(__name__)


@app.route('/connect', methods=['POST'])
def connect():

    flask.session['dict'] = {}
    flask.session['OBJ_ID'] = 0
    flask.session['funcs'] = ['swap', 'add', 'sub']
    return construct_response()


def getcurrID():
    return flask.session['OBJ_ID']

def incrID():
    flask.session['OBJ_ID'] += 1




@app.route('/vector', methods=['POST'])
def vector():
    data = cp.loads(flask.request.get_data())
    serial = data[0]
    arg = data[1]

    if arg is None:
        vec = pyblas.Vector()
        vec.clear()

    else:
        if serial:
            arg = flask.session['dict'][arg]
            vec = pyblas.Vector(arg)
        else:
            vec = pyblas.Vector(arg)
            vec.clear()

    key = getcurrID()
    flask.session['dict'][key] = vec

    resp = key
    incrID()

    return construct_response(resp)


@app.route('/matrix', methods=['POST'])
def matrix():
    data = cp.loads(flask.request.get_data())
    serial = data[0]
    arg = data[1]

    if arg is None:
        mat = pyblas.Matrix()
        mat.clear()

    else:
        if serial:
            arg = flask.session['dict'][arg]
            mat = pyblas.Matrix(arg)
        else:
            mat = pyblas.Matrix(arg[0], arg[1])
            mat.clear()

    key = getcurrID()
    flask.session['dict'][key] = mat

    resp = key
    incrID()

    return construct_response(resp)



@app.route('/request', methods=['POST'])
def request():
    call = cp.loads(flask.request.get_data())
    obj_id = call[0]
    fname = call[1]
    args = call[2]

    if fname in flask.session['funcs']:
        args[0] = flask.session['dict'][args[0]] 

    vec = flask.session['dict'][obj_id]
    handle = getattr(vec, fname)
    ret = handle(*args)

    return construct_response(ret)


@app.route('/innerproduct', methods=['POST'])
def func_value():
    call = cp.loads(flask.request.get_data())
    fname = call[0]
    args = call[1]
    for i in range(len(args)):
        args[i] = flask.session['dict'][args[i]]


    handle = getattr(pyblas, fname)
    ret = handle(*args)

    return construct_response(ret)


@app.route('/outerproduct', methods=['POST'])
@app.route('/matrixvector', methods=['POST'])
@app.route('/matrixmatrix', methods=['POST'])
def func_object():
    call = cp.loads(flask.request.get_data())
    fname = call[0]
    args = call[1]
    for i in range(len(args)):
        args[i] = flask.session['dict'][args[i]]


    handle = getattr(pyblas, fname)
    ret = handle(*args)

    key = getcurrID()
    flask.session['dict'][key] = ret
    incrID()

    return construct_response(key)




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
    app.debug = True
    app.run(threaded=True, host='0.0.0.0', port=7000)


run()
