import websocket
import sys
import pkgutil
import types
import os
from monitor import Monitor
from dispatcher import Router
from dispatcher import Determiner

string_types = (str,)
settings_file = "settings.py"


class Client(object):

    receiver = None

    import_name = None

    def __init__(self, import_name, root_path=None):
        self.rt = Router()
        self.dt = Determiner()

        self.import_name = import_name

        if root_path is None:
            root_path = self._get_root_path(self.import_name)
        self.root_path = root_path

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

    def _get_settings_attr(self, filename, attr):

        mod = self._load_file_attr(filename=filename)

        if hasattr(mod, attr):
            result = getattr(mod, attr)
        else:
            raise RuntimeError("Can not found the attribute ({}) in file ()".format(attr, filename))

        return result

    @property
    def last_msg(self):

        return self.rt.last_message

    def _check_files(self):
        settings = os.path.join(self.root_path, settings_file)
        if not os.path.exists(settings):
            raise RuntimeError("No settings.py file for this object")

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

        ws = self.receiver.ws
        print("请求下注:", request)
        ws.send(request, websocket.ABNF.OPCODE_BINARY)

    def run(self):
        request = self._get_settings_attr(settings_file, "request")
        url = self._get_settings_attr(settings_file, "url")
        self.__class__.receiver = Monitor(self.rt, url, request)
        print("开始执行......")
        self.receiver.connect()

