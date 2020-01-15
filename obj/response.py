from client import Client

cli = Client(__name__)
sk = cli.sk


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
    # cli.send(requestBet)


cli.run()
# print(cli.get_settings_attr("settings.py", "url"))
