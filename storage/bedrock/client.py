import random
import socket
import zmq

from .common import *
from .zmq_util import *
from .message_pb2 import *

class BedrockClient():
    def __init__(self, proxy_ips, offset):
        assert type(proxy_ips) == str or type(proxy_ips) == list, \
            'Proxy IPs argument must either be a string (filename) or a list.'

        if type(proxy_ips) == str:
            with open(proxy_ips) as f:
                self.proxy_ips = []
                self.proxy_ips.append(f.readline())
        else:
            self.proxy_ips = proxy_ips

        self.ut = UserThread(socket.gethostbyname(socket.gethostname()), offset)

        self.context = zmq.Context(1)

        self.address_cache = {}
        self.pusher_cache = SocketCache(self.context, zmq.PUSH)

        self.response_puller = self.context.socket(zmq.PULL)
        self.response_puller.bind(self.ut.get_request_pull_bind_addr())

        self.key_address_puller = self.context.socket(zmq.PULL)
        self.key_address_puller.bind(self.ut.get_key_address_bind_addr())

        self.rid = 0

    def get(self, key):
        worker_address = self._get_worker_address(key)
        send_sock = self.pusher_cache.get(worker_address)

        req, _ = self._prepare_data_request(key)
        req.type = 'GET'

        resp_obj = Response()

        # TODO: doesn't support invalidate yet
        ret_val = send_request(req, resp_obj, send_sock,
                self.response_puller).tuple[0].value

        return ret_val


    def put(self, key, value):
        worker_address = self._get_worker_address(key)
        send_sock = self.pusher_cache.get(worker_address)

        req, tup = self._prepare_data_request(key)
        req.type = 'PUT'
        tup.value = value
        tup.timestamp = 0
        resp_obj = Response()

        # TODO: doesn't support invalidate yet
        return send_request(req, resp_obj, send_sock,
                self.response_puller).tuple[0].err_number == 0

    def _prepare_data_request(self, key):
        req = Request()
        req.request_id = self.ut.get_ip() + ':' + str(self.rid)
        req.respond_address = self.ut.get_request_pull_connect_addr()
        tup = req.tuple.add()

        tup.key = key
        tup.num_address = len(self.address_cache[key])

        return (req, tup)

    def _get_worker_address(self, key):
        if key not in self.address_cache:
            proxy_addr = random.choice(self.proxy_ips)
            tid = random.randint(0, PROXY_THREAD_NUM - 1)

            addresses = self._query_proxy(key, ProxyThread(proxy_addr, tid))
            self.address_cache[key] = addresses

        return random.choice(self.address_cache[key])

    def _query_proxy(self, key, proxy_thread):
        key_request = Key_Request()

        key_request.respond_address = self.ut.get_key_address_connect_addr()
        key_request.keys.append(key)

        key_request.request_id = self.ut.get_ip() + ':' + str(self.rid)
        self.rid += 1

        send_sock = self. \
            pusher_cache.get(proxy_thread.get_key_address_connect_addr())
        resp = Key_Response()

        resp = send_request(key_request, resp, send_sock, self.key_address_puller)

        result = []
        for t in resp.tuple:
            if t.key == key:
                for a in t.addresses:
                    result.append(a)

        return result
