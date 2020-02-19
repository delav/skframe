import sys
import pkgutil
import types
import os
from monitor import Monitor

string_types = (str,)
settings_file = "settings.py"


class Client(object):

    # 引入Client类的文件名
    import_name = None

    def __init__(self, import_name, root_path=None):

        self.import_name = import_name

        if root_path is None:
            root_path = self._get_root_path(self.import_name)
        self.root_path = root_path

    @staticmethod
    def _import_string(import_name, silent=False):

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
        """
        引入文件的属性
        :param filename: 文件名
        :return:
        """
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
        """
        获取配置文件的属性值
        :param filename: 配置文件
        :param attr: 属性名
        :return:
        """

        mod = self._load_file_attr(filename=filename)

        if hasattr(mod, attr):
            result = getattr(mod, attr)
        else:
            raise RuntimeError("Can not found the attribute ({}) in file ()".format(attr, filename))

        return result

    def _check_files(self):
        """
        检查配置文件是否存在
        :return:
        """
        settings = os.path.join(self.root_path, settings_file)
        if not os.path.exists(settings):
            raise RuntimeError("No settings.py file for this object")

    @staticmethod
    def _get_root_path(import_name):
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

    @property
    def storage(self):
        url = self._get_settings_attr(settings_file, "url")
        msg = self._get_settings_attr(settings_file, "data")
        print("url:", url)
        print("data:", msg)
        receiver = Monitor(url, msg)
        return receiver

    def run(self):
        receiver = self.storage
        print("开始执行......")
        receiver.connect()



