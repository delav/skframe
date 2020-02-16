import websocket
from websocket import ABNF
from storage import RoundStorage
from storage import CasesStorage
from route import Router


class Monitor(object):

    round_id = None

    def __init__(self, url, request):
        self.ws = websocket.WebSocketApp(url)
        self.round = RoundStorage()
        self.cases = CasesStorage()
        self.route = Router()
        self.request = request
        self.url_map = self.route.url_map
        self.last_message = None

    def connect(self):
        self.ws.on_open = self.on_open
        self.ws.on_error = self.on_error
        self.ws.on_message = self.on_message
        self.ws.on_close = self.on_close
        print("开始连接.....")
        self.ws.run_forever()

    def disconnect(self):
        self.ws.keep_running = False

    def on_error(self, err):
        print("err:", err)

    def on_close(self):
        print("#close#")

    def on_open(self):
        print("请求连接:", self.request)
        self.ws.send(self.request, ABNF.OPCODE_BINARY)

    def on_message(self, msg=None):
        print("收到消息:", msg)
        self.dispatch_message(msg)

    def send(self, request):
        print("请求下注:", request)
        self.ws.send(request, websocket.ABNF.OPCODE_BINARY)

    def save_massage(self, key, message):
        if key is not None:
            self.round.add(key, message)
        else:
            self.round.append("other", message)

    def last_massage(self):
        return self.last_massage

    @staticmethod
    def _find_keyword(key, message):
        if str(message).find(key) > -1:
            return True
        return False

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

        self.save_massage(keyword, message)

        if not self.cases.exists(self.__class__.round_id):
            self.save_cases()

        return action_func()

    def set_round_id(self, round_id):
        self.__class__.round_id = round_id

    def round_storage(self):
        return self.round

    def save_cases(self):
        if self.__class__.round_id is not None:
            self.cases.add(self.__class__.round_id, self.round_storage())
        else:
            print("本局游戏您没有下注")

    def cases_storage(self):
        return self.cases







