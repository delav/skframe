from client import Client
from settings import requestBet

cli = Client(__name__)
sk = cli.rt

key1 = "ResBet"
key2 = "NotifyStart"
key3 = "NotifyFinish"
key4 = "RspIntoRoom"

# 判断器必须返回该消息唯一的keyword
# @sk.determine
# def judge(key, message):
#     pass

# @sk.determine
# class Judge(object):
#     def __init__(self, key, message):
#         pass
#     def do(self):
#         pass


@sk.route(key1)
def resBetAction():
    print("6666666")


@sk.route(key2)
def reqNotify():
    print("7777777")


@sk.route(key3)
def reqNotify():
    print("88888888")


@sk.route(key4)
def rspIntoRoom():
    print("99999999")
    message = cli.last_msg
    print("message:", message)
    cli.send(requestBet)


cli.run()
