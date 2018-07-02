import cloudpickle as cp
import boto3
import requests
import utils

class SkyConnection():
    def __init__(self, addr='127.0.0.1', port=7000, pr_type='FS', pr_info={'dir': 'funcs/'}):
        self.service_addr = 'http://' + addr + ":" + str(port)

        self.session = requests.Session()
        r = self.session.post(self.service_addr + "/connect")


    def vector(self, args):
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/vector", data=args_bin)
        return Vec_Resp(cp.loads(r.data), self.service_addr, self.session)


    def matrix(self, args):
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/matrix", data=args_bin)
        return Mat_Resp(cp.loads(r.data), self.service_addr, self.session)



class Vec_Resp():
    def __init__(self, id, addr, session):
        self.id = id
        self.service_addr = addr
        self.session = session

    def __getitem__(self, index):
        args = [index]
        fname = '__getitem__'
        call = [self.id, fname, args]
        call_bin = cp.dumps(call)

        r = self.session.post(self.service_addr + "/vector/request", data=call_bin)
        return cp.loads(r.data)

    def __setitem__(self, index, value):
        args = [index, value]
        fname = '__setitem__'
        call = [self.id, fname, args]
        call_bin = cp.dumps(call)

        r = self.session.post(self.service_addr + "/vector/request", data=call_bin)


    def size():
        args = []
        fname = 'size'
        call = [self.id, fname, args]
        call_bin = cp.dumps(call)

        r = self.session.post(self.service_addr + "/vector/request", data=call_bin)
        return cp.loads(r.data)

class Mat_Resp():
    def __init__(self, id, addr, session):
        self.id = id
        self.service_addr = addr
        self.session = session


def connect(addr='127.0.0.1', port=7000, pr_type='FS', pr_info={'dir': 'funcs/'}):
    return SkyConnection(addr, port, pr_type, pr_info)
