from settings import reqBet
from converter import str2bin
from runclient import cli, sk, storage

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
    message = storage.last_msg
    round_id = message.roundId
    storage.set_round_id(round_id)


@sk.route(key4)
def rsp_into_room():
    print("99999999")
    bet_data = str2bin(reqBet)
    cli.send(bet_data)


