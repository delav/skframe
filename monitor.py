import websocket
from storage import RoundStorage


class Monitor(object):

    def __init__(self, sk, url, request):
        self.ws = websocket.WebSocketApp(url)
        self.sk = sk
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
        pass

    def on_close(self):
        pass

    def on_open(self):
        print("请求连接:", self.request)
        self.ws.send(self.request, websocket.ABNF.OPCODE_BINARY)

    def on_message(self, msg=None):
        print("收到消息:", msg)
        self.sk.dispatch_message(msg)



