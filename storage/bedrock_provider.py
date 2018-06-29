import cloudpickle as cp
import random

from .storage_provider import StorageProvider
from .bedrock.client import BedrockClient

class BedrockProvider(StorageProvider):
    def __init__(self, ip):
        self.client = BedrockClient(ip, random.randint(0, 100))

    def get(self, funcname):
        # TODO: change this when Bedrock has namespacing
        return self.client.get('funcs/' + funcname)

    def get_object(self, obj_name):
        return self.client.get(obj_name)

    def put(self, funcname, obj):
        val = self.client.put('funcs/' + funcname, obj)

        funcs = self.get_list('', fullname=True)
        funcs.append('funcs/' + funcname)
        self.client.put('allfuncs', cp.dumps(funcs))

    def get_list(self, prefix, fullname=False):
        funcs = self.client.get('allfuncs')
        if len(funcs) == 0:
            return []

        funcs = cp.loads(funcs)

        result = []
        prefix = "funcs/" + prefix

        for f in funcs:
            if f.startswith(prefix):
                if fullname:
                    result.append(f)
                else:
                    result.append(f[6:])

        return result

    def remove(self, funcname):
        raise NotImplementedError("Bedrock does not currently support " +
                "remove operations.")
