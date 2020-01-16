from client import Client
from settings import requestBet

cli = Client(__name__)
sk = cli.rt
dk = cli.dt


# @dk.determine
# def judge():
#     pass

# @dk.determine
# class Judge(object):
#     pass


@sk.route("ResBet")
def resBetAction():
    print("6666666")


@sk.route("NotifyStart")
def reqNotify():
    print("7777777")


@sk.route("NotifyFinish")
def reqNotify():
    print("88888888")


@sk.route("RspIntoRoom")
def rspIntoRoom():
    print("99999999")
    message = cli.last_msg
    print("message:", message)
    cli.send(requestBet)


cli.run()
