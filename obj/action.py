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
def start_notify():
    print("88888888")
    message = cli.last_msg
    round_id = message.roundId
    cli.set_round_id(round_id)


@sk.route(key4)
def rsp_into_room():
    print("99999999")
    cli.send(requestBet)


