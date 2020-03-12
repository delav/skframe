import sys
import logging
import traceback
import websocket
from websocket import ABNF
from storage import RoundStorage
from storage import CasesStorage
from route import Router

logger = logging.getLogger()


class Monitor(object):
    """
    启动客户端和收集存储消息
    """

    round_id = None
    round_msg = RoundStorage()

    def __init__(self, url, data):
        self.ws = websocket.WebSocketApp(url)
        # 存储所有cases
        self.cases = CasesStorage()

        self.route = Router()
        self.data = data
        self.url_map = self.route.url_map
        self.last_message = None

    def connect(self):
        """
        与服务器进行长连接
        :return: None
        """
        self.ws.on_open = self.on_open
        self.ws.on_error = self.on_error
        self.ws.on_message = self.on_message
        self.ws.on_close = self.on_close
        print("开始连接.....")
        self.ws.run_forever()

    def disconnect(self):
        """
        断开客户端与服务器的连接
        :return: None
        """
        self.ws.keep_running = False

    def on_error(self, err):
        """
        客户端与服务器交互异常时触发
        :param err: 异常信息
        :return:
        """
        logger.debug("err:", err)

    def on_close(self):
        """
        客户端与服务器关闭时触发
        :return:
        """
        logger.debug("#close#")

    def on_open(self):
        """
        客户端请求连接服务器
        :return:
        """
        logger.debug("请求连接:", self.data)
        self.ws.send(self.data, ABNF.OPCODE_BINARY)

    def on_message(self, msg=None):
        """
        接受服务器推送的消息
        :param msg: 消息
        :return: None
        """
        logger.debug("收到消息:", msg)
        self.dispatch_message(msg)

    def send(self, data, key=None):
        """
        向服务器发送消息
        :param data: 二进制消息
        :param key: 使用key作为关键字来保存该发送的消息
        :return: None
        """
        logger.debug("请求下注:", data)
        if key is not None:
            self.save_massage(key, data)
        else:
            self.__class__.round_msg.append("request", data)
        self.ws.send(data, websocket.ABNF.OPCODE_BINARY)

    def save_massage(self, key, message, flag=None):
        """
        保存消息
        :param key: 键
        :param message: 消息
        :param flag: 键为空时保存到一个flag作为键的列表
        :return: None
        """
        if key is not None:
            self.__class__.round_msg.add(key, message)
        else:
            self.__class__.round_msg.append(flag, message)

    def last_massage(self):
        """
        获取服务器推送的最后一条消息
        :return: 最新的消息
        """
        return self.last_massage

    @staticmethod
    def _find_keyword(key, message):
        """
        判断某个字符串中是否有某个子字符串
        :param key: 子字符串
        :param message: 字符串
        :return: True或False
        """
        if str(message).find(key) > -1:
            return True
        return False

    def dispatch_message(self, message):
        """
        接受到消息后判断执行哪一步
        :param message: 接受到的消息
        :return:
        """
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

        self.save_massage(keyword, message, "response")

        if not self.cases.exists(self.__class__.round_id):
            self.__class__.round_msg = RoundStorage()
            self.save_cases()

        self._callback(action_func)

    def _callback(self, callback, *args):
        """
        回调，执行与字符串同名的函数
        :param callback: 函数名
        :param args: 函数参数
        :return:
        """
        if callback:
            try:
                callback(self, *args)
            except Exception as e:
                logger.error(e)
                if logger.isEnabledFor(logging.DEBUG):
                    _, _, tb = sys.exc_info()
                    traceback.print_tb(tb)

    def set_round_id(self, round_id):
        """
        设置游戏的局数
        :param round_id: 局数
        :return:
        """
        self.__class__.round_id = round_id

    def round_storage(self):
        """
        获取某局游戏数据
        :return:
        """
        return self.__class__.round_msg

    def save_cases(self):
        """
        保存所有cases的数据
        :return:
        """
        if self.__class__.round_id is not None:
            self.cases.add(self.__class__.round_id, self.round_storage())
        else:
            logger.debug("本局游戏您没有下注")

    def cases_storage(self):
        """
        获取所有cases数据
        :return:
        """
        return self.cases







