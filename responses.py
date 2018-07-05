import cloudpickle as cp
import requests

class Vec_Resp():
    def __init__(self, id, addr, session):
        self.id = id
        self.service_addr = addr
        self.session = session


    def request(self, funcname, args=[]):
        call = [self.id, funcname, args]
        call_bin = cp.dumps(call)
        r = self.session.post(self.service_addr + "/request", data=call_bin)

        return r


    def __getitem__(self, index):
        r = self.request('__getitem__', [index])
        return cp.loads(r.content)


    def __setitem__(self, index, value):
        r = self.request('__setitem__', [index, value])


    def size(self):
        r = self.request('size')
        return cp.loads(r.content)


    def resize(self, size, save=True):
        r = self.request('resize', [size, save])


    def max_size(self):
        r = self.request('max_size')
        return cp.loads(r.content)

    
    def empty(self):
        r = self.request('empty')

    
    def swap(self, vector):
        r = self.request('swap', [vector.id])

    
    def clear(self):
        r = self.request('clear')


    def mul(self, scalar):
        r = self.request('mul', [scalar])


    def div(self, scalar):
        r = self.request('div', [scalar])


    def add(self, vector):
        r = self.request('add', [vector.id])


    def sub(self, vector):
        r = self.request('sub', [vector.id])



class Mat_Resp():
    def __init__(self, id, addr, session):
        self.id = id
        self.service_addr = addr
        self.session = session


    def request(self, funcname, args=[]):
        call = [self.id, funcname, args]
        call_bin = cp.dumps(call)
        r = self.session.post(self.service_addr + "/request", data=call_bin)

        return r


    def __getitem__(self, pair):
        r = self.request('get', [pair[0], pair[1]])
        return cp.loads(r.content)



    def __setitem__(self, pair, val):
        r = self.request('set', [pair[0], pair[1], val])


    def resize(self, row, col, save=True):
        r = self.request('resize', [row, col, save])


    def rows(self):
        r = self.request('rows')
        return cp.loads(r.content)


    def cols(self):
        r = self.request('cols')
        return cp.loads(r.content)


    def clear(self):
        r = self.request('clear')


    def swap(self, matrix):
        r = self.request('swap', [matrix.id])


    def mul(self, scalar):
        r = self.request('mul', [scalar])


    def div(self, scalar):
        r = self.request('div', [scalar])


    def add(self, matrix):
        r = self.request('add', [matrix.id])


    def sub(self, matrix):
        r = self.request('sub', [matrix.id])




