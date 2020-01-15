from storage import RouteStorage


class Route(object):

    def __init__(self):
        self.url_map = RouteStorage()

    def route(self, rule):
        def decorator(f):
            self.add_url_rule(rule, f)
            return f
        return decorator

    def add_url_rule(self, rule, view_func=None):
        if view_func is not None:
            key = rule
            self.url_map.add(key, view_func)

    def _find_keyword(self, key, message):
        if str(message).find(key) > -1:
            return True
        return False

    def dispatch_message(self, message):
        keys = self.url_map.keys()
        keyword = None

        for key in keys:
            if self._find_keyword(key, message):
                keyword = key
                break

        action_func = self.url_map.get(keyword)

        return action_func()

