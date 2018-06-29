class StorageProvider():
    def get(self, funcname):
        raise NotImplementedError("Abstract class should not be instantiated.")

    def get_object(self, obj_name):
        raise NotImplementedError("Abstract class should not be instantiated.")

    def put(self, funcname, obj):
        raise NotImplementedError("Abstract class should not be instantiated.")

    def get_list(self, prefix):
        raise NotImplementedError("Abstract class should not be instantiated.")

    def remove(self, funcname):
        raise NotImplementedError("Abstract class should not be instantiated.")
