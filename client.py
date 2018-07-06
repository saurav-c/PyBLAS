import cloudpickle as cp
import requests
from responses import Vec_Resp, Mat_Resp

class PyBlasConnection():
    def __init__(self, addr='127.0.0.1', port=7000):
        self.service_addr = 'http://' + addr + ":" + str(port)

        self.session = requests.Session()
        r = self.session.post(self.service_addr + "/connect")


    def vector(self, args=None):
        serial = False
        
        if isinstance(args, Vec_Resp):
            serial = True
            args = args.id

        args = [serial, args]
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/vector", data=args_bin)
        
        return Vec_Resp(cp.loads(r.content), self.service_addr, self.session)


    def matrix(self, args=None):
        serial = False
        
        if isinstance(args, Mat_Resp):
            serial = True
            args = args.id

        args = [serial, args]
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/matrix", data=args_bin)
        return Mat_Resp(cp.loads(r.content), self.service_addr, self.session)


    def inner_product(self, Vec1, Vec2):
        funcname = 'inner_prod'
        objs = [Vec1.id, Vec2.id]
        args = [funcname, objs]
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/innerproduct", data=args_bin)
        return cp.loads(r.content)

    
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


def connect(addr='127.0.0.1', port=7000):
    return PyBlasConnection(addr, port)
