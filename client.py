import websocket
import sys
import pkgutil
import types
import os
import errno
from monitor import Monitor
from dispatcher import Route

string_types = (str,)


class Client(object):

    mt = None
    import_name = None

    def __init__(self, import_name, root_path=None):
        self.sk = Route()
        self.import_name = import_name
        if root_path is None:
            root_path = self._get_root_path(self.import_name)
        self.root_path = root_path
        print("root_path:", root_path)

    def _import_string(self, import_name, silent=False):

        import_name = str(import_name).replace(":", ".")
        try:
            try:
                __import__(import_name)
            except ImportError:
                if "." not in import_name:
                    raise
            else:
                return sys.modules[import_name]

            module_name, obj_name = import_name.rsplit(".", 1)
            module = __import__(module_name, globals(), locals(), [obj_name])
            try:
                return getattr(module, obj_name)
            except AttributeError as e:
                raise ImportError(e)

        except ImportError as e:
            if not silent:
                raise ImportError((import_name, e), sys.exc_info()[2])

    def _load_file_attr(self, filename):
        filename = os.path.join(self.root_path, filename)
        module = types.ModuleType("config")
        module.__file__ = filename

        try:
            with open(filename, mode="rb") as config_file:
                exec(compile(config_file.read(), filename, "exec"), module.__dict__)
        except IOError as e:
            e.strerror = "Unable to load configuration file ({})".format(e.strerror)
            raise

        if isinstance(module, string_types):
            module = self._import_string(module)

        for key in dir(module):
            if key.isupper():
                module[key] = getattr(module, key)

        return module

    def get_settings_attr(self, filename, attr):

        mod = self._load_file_attr(filename=filename)

        if hasattr(mod, attr):
            result = getattr(mod, attr)
        else:
            raise RuntimeError("Can not found the attribute ({}) in file ()".format(attr, filename))

        return result

    def _check_files(self):
        settings_file = os.path.join(self.root_path, "settings")
        if not os.path.exists(settings_file):
            raise RuntimeError("No settings file for this object")

    def _get_root_path(self, import_name):
        """Returns the path to a package or cwd if that cannot be found.  This
        returns the path of a package or the folder that contains a module.

        Not to be confused with the package path returned by :func:`find_package`.
        """
        mod = sys.modules.get(import_name)

        if mod is not None and hasattr(mod, "__file__"):
            return os.path.dirname(os.path.abspath(mod.__file__))

        loader = pkgutil.get_loader(import_name)

        if loader is None or import_name == "__main__":
            return os.getcwd()

        if hasattr(loader, "get_filename"):
            filepath = loader.get_filename(import_name)
        else:
            __import__(import_name)
            mod = sys.modules[import_name]
            filepath = getattr(mod, "__file__", None)

            if filepath is None:
                raise RuntimeError("No root path can be found for the provided module {}".format(import_name))

        # filepath is import_name.py for a module, or __init__.py for a package.
        return os.path.dirname(os.path.abspath(filepath))

    def send(self, request):
        ws = self.mt.ws
        print("请求下注:", request)
        ws.send(request, websocket.ABNF.OPCODE_BINARY)

    def run(self):
        request = self.get_settings_attr("settings.py", "request")
        url = self.get_settings_attr("settings.py", "url")
        print("url:", url)
        print("request:", request)
        self.__class__.mt = Monitor(self.sk, url, request)
        print("开始执行......")
        self.mt.connect()


class ConfigAttribute(object):
    """Makes an attribute forward to the config"""

    def __init__(self, name, get_converter=None):
        self.__name__ = name
        self.get_converter = get_converter

    def __get__(self, obj, tp=None):
        if obj is None:
            return self
        rv = obj.config[self.__name__]
        if self.get_converter is not None:
            rv = self.get_converter(rv)
        return rv

    def __set__(self, obj, value):
        obj.config[self.__name__] = value
