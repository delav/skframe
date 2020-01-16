import inspect
from storage import RouteStorage


class Router(object):

    def __init__(self):
        self.url_map = RouteStorage()
        self.last_message = None

    def route(self, rule):
        def decorator(f):
            self._add_url_rule(rule, f)
            return f
        return decorator

    def _add_url_rule(self, rule, view_func=None):
        if view_func is not None:
            key = rule
            self.url_map.add(key, view_func)

    def _find_keyword(self, key, message):
        if str(message).find(key) > -1:
            return True
        return False

    def _last_msg(self):

        return self.last_message

    def dispatch_message(self, message):
        keys = self.url_map.keys()
        keyword = None

        self.last_message = message

        for key in keys:
            if self._find_keyword(key, message):
                keyword = key
                break

        action_func = self.url_map.get(keyword)

        args = action_func.__code__.co_argcount
        if args != 0:
            raise TypeError("{}() required no argument, "
                            "but get {}".format(action_func, args))

        return action_func()


class Determiner(object):

    def __init__(self):
        self.judge_list = []

    @property
    def determine(self):
        def decorator(f):
            self.add_judge(f)
            return f
        return decorator

    def add_judge(self, view_func=None):
        if inspect.isclass(view_func):
            print("判断器属于类")
        if inspect.isfunction(view_func):
            print("判断器属于函数")
        if inspect.ismethod(view_func):
            print("判断器属于方法")
        self.judge_list.append(view_func)

    def do(self):
        pass