from settings import requestBet
from runclient import cli, sk

key1 = "ResBet"
key2 = "NotifyStart"
key3 = "NotifyFinish"
key4 = "RspIntoRoom"


@sk.route(key1)
def res_bet_action():
    print("6666666")


@sk.route(key2)
def req_notify():
    print("7777777")


@sk.route(key3)
def finish_notify():
    print("88888888")


@sk.route(key4)
def rsp_into_room():
    print("99999999")
    # message = cli.last_msg
    # print("message:", message)
    cli.send(requestBet)

