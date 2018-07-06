import cloudpickle as cp
import requests

class Vec_Resp():
    def __init__(self, id, addr, session):
        self.id = id
        self.service_addr = addr
        self.session = session
        self.rep = ''
        self.changed = True


    def __str__(self):
        if self.changed:
            rep = '[ '
            for i in range(self.size()):
                rep += str(self.__getitem__(i)) + ' '
            rep += ']'
            self.rep = rep
            self.changed = False
        return self.rep



    def request(self, funcname, args=[]):
        call = [self.id, funcname, args]
        call_bin = cp.dumps(call)
        r = self.session.post(self.service_addr + "/request", data=call_bin)

        return r


    def __getitem__(self, index):
        assert index >= 0 and index < self.size(), "Index out of bound"
        r = self.request('__getitem__', [index])
        return cp.loads(r.content)


    def __setitem__(self, index, value):
        assert index >= 0 and index < self.size(), "Index out of bound"
        self.changed = True
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

        self.rep = ''
        self.changed = True


    def __str__(self):
        if self.changed:
            rep = '['
            for i in range(self.rows()):
                rep += ' ['
                for j in range(self.cols()):
                    rep += str(self.__getitem__([i, j])) + ' '
                rep += ']'
            rep += ' ]'
            self.rep = rep
        return self.rep




    def request(self, funcname, args=[]):
        call = [self.id, funcname, args]
        call_bin = cp.dumps(call)
        r = self.session.post(self.service_addr + "/request", data=call_bin)

        return r


    def __getitem__(self, pair):
        assert isinstance(pair, list), "Must input index as a list: [ROW, COL]"
        row = pair[0]
        col = pair[1]
        assert row >= 0 and row < self.rows(), "Row index out of bounds"
        assert col >= 0 and col < self.col(), "Col index out of bounds"

        r = self.request('get', [pair[0], pair[1]])
        return cp.loads(r.content)



    def __setitem__(self, pair, val):
        assert isinstance(pair, list), "Must input index as a list: [ROW, COL]"
        row = pair[0]
        col = pair[1]
        assert row >= 0 and row < self.rows(), "Row index out of bounds"
        assert col >= 0 and col < self.col(), "Col index out of bounds"

        self.changed = True

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




