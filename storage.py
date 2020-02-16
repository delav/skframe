from exception import *

__all__ = ["RoundStorage", "CasesStorage", "RouteStorage"]


class BaseStorage(object):

    def __init__(self):
        self.result = {}

    def add(self, key, value):
        if key is None:
            raise KeyError("Add error, key of dict can not None")
        self.result[key] = value

    def delete(self, key):
        if key not in self.result:
            raise KeyError("Delete error, key of [{}]"
                           " can not be found in dict".format(key))
        self.result.pop(key)

    def get(self, key):
        if key not in self.result:
            raise KeyError("Get error, key of [{}] "
                           "can not be found in dict".format(key))
        return self.result[key]

    def update(self, key, value):
        if key not in self.result:
            raise KeyError("Update error, key of [{}] "
                           "can not be found in dict".format(key))
        self.result[key] = value

    def append(self, key, value):
        if key not in self.result:
            self.add(key, [])
        obj = self.get(key)
        if isinstance(obj, list):
            raise TypeError("Append error, value of key [{}] "
                            "except list type".format(key))
        else:
            obj.append(value)
        self.result[key] = obj

    def exists(self, key):
        if key in self.result:
            return True
        return False

    def keys(self):
        keys = self.result.keys()
        return list(keys)

    def values(self):
        values = self.result.values()
        return list(values)

    def size(self):
        size = len(self.result.keys())
        return size

    def all(self):
        return self.result


class RouteStorage(BaseStorage):
    pass


class RoundStorage(BaseStorage):
    pass


class CasesStorage(BaseStorage):
    pass

