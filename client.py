import cloudpickle as cp
import boto3
import requests
import utils

class SkyConnection():
    def __init__(self, addr='127.0.0.1', port=7000, pr_type='FS', pr_info={'dir': 'funcs/'}):
        self.service_addr = addr + ":" + str(port)

        pr_dict = { 'type': pr_type, 'info': pr_info }
        self.provider = utils.create_provider(pr_type, pr_info)

        self.session = requests.Session()
        r = self.session.post(self.service_addr + "/connect", data=cp.dumps(pr_dict))

    def list(self, prefix=None):
        for fname in self._get_func_list(prefix):
            print(fname)

    def get(self, name):
        if name not in self._get_func_list():
            print("No function found with name '" + name + "'.")
            print("To view all functions, use the `list` method.")
            return None

        return SkyFunc(name, self._name_to_handle(name), self)

    def _get_func_list(self, prefix=None):
        if prefix == None:
            r = self.session.get(self.service_addr + "/list")
        else:
            r = self.session.get(self.service_addr + "/list/" + prefix)
        return cp.loads(r.content)


    def _name_to_handle(self, name):
        return name

    def exec_func(self, handle, args):
        args_bin = cp.dumps(args)

        r = self.session.post(self.service_addr + "/" + handle, data=args_bin)
        return cp.loads(r.content)

    def register(self, func, name):
        self.session.post(self.service_addr + "/create/" + name, data=cp.dumps(func))

    def deregister(self, name):
        self.session.post(self.service_addr + "/remove/" + name)


class SkyFuture():
    def __init__(self, obj_id, conn):
        self.obj_id = obj_id
        self.conn = conn

    def get(self):
        obj = utils.get_provider(self.conn.provider).get(self.obj_id)

        while not obj:
            obj = utils.get_provider(self.conn.provider).get(self.obj_id)

        return cp.loads(obj)

class SkyFunc():
    def __init__(self, name, func_handle, conn):
        self.name = name
        self.handle = func_handle
        self._conn = conn

    def __call__(self, *args):
        obj_id = self._conn.exec_func(self.handle, args)
        return SkyFuture(obj_id, self._conn)

class SkyReference():
    def __init__(self, key, deserialize):
        self.key = key
        self.deserialize = deserialize

def connect(addr='http://127.0.0.1', port=7000, pr_type='FS', pr_info={'dir': 'funcs/'}):
    return SkyConnection(addr, port, pr_type, pr_info)
