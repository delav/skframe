from storage import RoundStorage
from storage import RouteStorage


class Router(object):

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            orig = super(Router, cls)
            cls._instance = orig.__new__(cls)

        return cls._instance

    def __init__(self):
        self.url_map = RouteStorage()
        self.round_storage = RoundStorage()

        self.judge_list = []
        self.last_message = None

    def route(self, rule=None):
        def decorator(f):
            self._add_url_rule(rule, f)
            return f

        return decorator

    def _add_url_rule(self, rule, view_func=None):
        if view_func is not None:
            key = rule
            self.url_map.add(key, view_func)

    # @property
    # def determine(self):
    #     def decorator(f):
    #         self._add_judge(f)
    #         return f
    #     return decorator
    #
    # def _add_judge(self, view_func=None):
    #     self.judge_list.append(view_func)
    #
    # def judge_type(self, view_func=None):
    #     if inspect.isclass(view_func):
    #         cls = view_func()
    #     elif inspect.isfunction(view_func):
    #         print("判断器属于函数")
    #     elif inspect.ismethod(view_func):
    #         print("判断器属于方法")
    #     else:
    #         pass





