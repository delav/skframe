import websocket
from websocket import ABNF


class Monitor(object):

    def __init__(self, route, url, request):
        self.ws = websocket.WebSocketApp(url)
        self.rt = route
        self.request = request

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
        self.rt.dispatch_message(msg)



