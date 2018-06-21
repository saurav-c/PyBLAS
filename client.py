import cloudpickle as cp
import requests

class SkyConnection():
    def __init__(self, addr='127.0.0.1', port=7000):
        self.service_addr = addr + ":" + str(port)
        self.session = requests.Session()

    def exec_func(self, handle, args):
        data = [handle, args]
        data_bin = cp.dumps(data)

        r = self.session.post(self.service_addr + "/execute", data=data_bin)
        return cp.loads(r.content)


def connect(addr=None, port=7000):
    return SkyConnection(addr, port)
