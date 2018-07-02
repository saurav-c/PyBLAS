import boto3
import cloudpickle as cp
import flask
from flask import session
from flask_session import Session
from threading import Thread
import uuid
import utils

import pyblas

app = flask.Flask(__name__)


@app.route('/connect', methods=['POST'])
def connect():
    pr_data = cp.loads(flask.request.get_data())
    pr_type = pr_data['type']
    info = pr_data['info']

    flask.session['provider'] = utils.create_provider(pr_type, info)
    return construct_response()




@app.route('/vector', methods=['POST'])
def vector():
    args = cp.loads(flask.request.get_data())
    vec = pyblas.Vector(args)

    return construct_response(vec)



@app.route('/create/<funcname>', methods=['POST'])
def create_func(funcname):
    provider = utils.get_provider(flask.session['provider'])
    func_binary = flask.request.get_data()

    app.logger.info('Creating function: ' + funcname + '.')
    provider.put(funcname, func_binary)

    return construct_response()


@app.route('/remove/<funcname>', methods=['POST'])
def remove_func(funcname):
    provider = utils.get_provider(flask.session['provider'])

    app.logger.info('Removing function: ' + funcname + '.')
    provider.remove(funcname)

    return construct_response()


@app.route('/<funcname>', methods=['POST'])
def call_func(funcname):
    obj_id = str(uuid.uuid4())
    t = Thread(target = _exec_func, args = (funcname, flask.session['provider'], obj_id, flask.request.get_data()))
    t.start()

    return construct_response(obj_id)


def _exec_func(funcname, p_obj, obj_id, arg_obj):
    provider = utils.get_provider(p_obj)
    func_binary = provider.get(funcname)
    func = cp.loads(func_binary)

    args = cp.loads(arg_obj)

    func_args = ()

    for arg in args:
        if isinstance(arg, sky.SkyReference):
            func_args = (_resolve_ref(arg, provider),)
        else:
            func_args += (arg,)


    res = func(*args)

    provider.put(obj_id, cp.dumps(res))

def _resolve_ref(ref, provider):
    ref_data = provider.get_object(ref.key)

    if ref.deserialize:
        return cp.loads(ref_data)
    else:
        return ref_data

@app.route('/list', methods=['GET'])
@app.route('/list/<prefix>', methods=['GET'])
def list_funcs(prefix=''):
    provider = utils.get_provider(flask.session['provider'])
    result = provider.get_list(prefix)

    return construct_response(result)

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
