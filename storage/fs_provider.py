from .storage_provider import StorageProvider

import os

class FSProvider(StorageProvider):
    def __init__(self, path=None):
        if path == None:
            os.makedirs("funcs")
            path = "funcs"
        self.path = path

    def get(self, funcname):
        path = os.path.join(self.path, funcname)
        with open(path, 'rb') as f:
            return f.read()

    def put(self, funcname, obj):
        path = os.path.join(self.path, funcname)
        with open(path, 'wb') as f:
            f.write(obj)

    def get_list(self, prefix=None):
        path = self.path

        if prefix == None:
            return os.listdir(path)

        files = []
        for f in os.listdir(path):
            if f.startswith(prefix):
                files.append(f)

        return files

    def remove(self, funcname):
        path = os.path.join(self.path, funcname)
        os.remove(path)
