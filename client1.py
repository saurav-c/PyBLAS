import cloudpickle as cp
import boto3
import requests
import utils

class SkyConnection():
    def __init__(self, addr='127.0.0.1', port=7000, pr_type='FS', pr_info={'dir': 'funcs/'}):
        self.service_addr = 'http://' + addr + ":" + str(port)

        self.session = requests.Session()
        r = self.session.post(self.service_addr + "/connect")


    def vector(self, args=[]):
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/vector", data=args_bin)
        
        return Vec_Resp(cp.loads(r.content), self.service_addr, self.session)


    def matrix(self, args=[]):
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/matrix", data=args_bin)
        return Mat_Resp(cp.loads(r.content), self.service_addr, self.session)


    def inner_product(self, Vec1, Vec2):
        funcname = 'inner_prod'
        objs = [Vec1.id, Vec2.id]
        args = [funcname, objs]
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/innerproduct", data=args_bin)
        return r.content

    
    def outer_product(self, Vec1, Vec2):
        funcname = 'outer_prod'
        objs = [Vec1.id, Vec2.id]
        args = [funcname, objs]
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/outerproduct", data=args_bin)
        return Mat_Resp(cp.loads(r.content), self.service_addr, self.session)


    # Matrix - Vector Multiplication
    def mv_mul(self, matx, vec):
        funcname = 'prod1'
        objs = [matx.id, vec.id]
        args = [funcname, objs]
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/matrixvector", data=args_bin)
        return Vec_Resp(cp.loads(r.content), self.service_addr, self.session)


    # Matrix - Matrix Multiplication
    def mm_mul(self, matx1, matx2):
        funcname = 'prod2'
        objs = [matx1.id, matx2.id]
        args = [funcname, objs]
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/matrixmatrix", data=args_bin)
        return Mat_Resp(cp.loads(r.content), self.service_addr, self.session)




class Vec_Resp():
    def __init__(self, id, addr, session):
        self.id = id
        self.service_addr = addr
        self.session = session


    def request(funcname, args=[]):
        call = [self.id, funcname, args]
        call_bin = cp.dumps(call)
        r = self.session.post(self.service_addr + "/request", data=call_bin)

        return r


    def __getitem__(self, index):
        r = request('__getitem__', [index])
        return cp.loads(r.content)


    def __setitem__(self, index, value):
        r = request('__setitem__', [index, value])


    def size(self):
        r = request('size')
        return cp.loads(r.content)


    def resize(self, size, save=True):
        r = request('resize', [size, save])


    def max_size(self):
        r = request('max_size')
        return cp.loads(r.content)

    
    def empty(self):
        r = request('empty')

    
    def swap(self, vector):
        r = request('swap', [vector.id])

    
    def clear(self):
        r = request('clear')


    def mul(self, scalar):
        r = request('mul', [scalar])


    def div(self, scalar):
        r = request('div', [scalar])


    def add(self, vector):
        r = request('add', [vector.id])


    def sub(self, vector):
        r = request('sub', [vector.id])



class Mat_Resp():
    def __init__(self, id, addr, session):
        self.id = id
        self.service_addr = addr
        self.session = session


def connect(addr='127.0.0.1', port=7000, pr_type='FS', pr_info={'dir': 'funcs/'}):
    return SkyConnection(addr, port, pr_type, pr_info)
