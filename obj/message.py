from google.protobuf.json_format import MessageToDict
from boom.pb2.game_pb2 import Web
from boom.pb2.game_pb2 import ReqIntoRoom, ReqBet, ReqSettlementDataList
from boom.pb2.game_pb2 import RspIntoRoom, RspBet, NotifyStart, NotifyBetting, NotifyFinish, NotifyWait, \
    RspSettlementDataList, PBNotifyBet, PBNotifySelfBet, NotifyWiccSettlement
from boom.pb2 import package_pb2
from boom_data import RspIntoRoomData, PBNotifyBetData
from base import BasePack

game = "boom"
pack = package_pb2.Pack()


# 封装请求数据
class RequestPack(BasePack):
    def __init__(self, caseReqData):
        super().__init__(game, pack)
        self.reqIntoRoom = ReqIntoRoom()
        self.reqBet = ReqBet()
        self.reqSettlementDataList = ReqSettlementDataList()
        self.caseReqData = caseReqData

    # 请求进入房间
    def req_into_room(self):
        self.reqIntoRoom.uid = self.userWallet  # 用户uid，即钱包地址
        self.reqIntoRoom.platform = Web  # 平台数据，Web或Phone

        hexStr = self.reqIntoRoom.SerializeToString()
        basePack,  packHex = self.base_req(hexStr, "ReqIntoRoom")

        reqIntoRoomDict = MessageToDict(self.reqIntoRoom)
        packDict = MessageToDict(basePack)
        packDict["data"] = reqIntoRoomDict

        return packHex, packDict

    # 请求下注
    def req_bet(self, rspIntoRoom):
        roomData = RspIntoRoomData(rspIntoRoom)
        srvid = roomData.get_srvid()
        gameid = roomData.get_gameid()
        roomid = roomData.get_roomid()

        self.reqBet.txhash = self.caseReqData.txhash  # 签名
        self.reqBet.sysWalletAddr = self.sysWallet  # 系统钱包地址
        self.reqBet.idx.srvid = srvid  # 服务id
        self.reqBet.idx.roomid = roomid  # 房间id
        self.reqBet.idx.gameid = gameid  # 游戏id，区别于哪个游戏
        self.reqBet.idx.passwd = ''

        pbBetData = self.reqBet.betDatas.add()
        pbBetData.uid = self.userWallet  # 用户id，即钱包地址
        pbBetData.betCoinsHundred = self.caseReqData.betCoinsHundred   # 下注金额x100
        pbBetData.runAwayValueHundred = self.caseReqData.runAwayValueHundred  # 逃跑值x100

        hexStr = self.reqBet.SerializeToString()
        basePack, packHex = self.base_req(hexStr, "ReqBet")

        # 请求数据转为字典
        reqBetDict = MessageToDict(self.reqBet)
        packDict = MessageToDict(basePack)
        packDict["data"] = reqBetDict

        return packHex, packDict

    # 请求自己的下注信息
    def req_settlement_data_list(self, totalMessage, roundId):
        rspIntoRoom = totalMessage[roundId]["RspIntoRoom"]
        pbNotifyBet = totalMessage[roundId]["PBNotifyBet"]
        roomData = RspIntoRoomData(rspIntoRoom)
        pbNotifyBetData = PBNotifyBetData(pbNotifyBet)
        srvid = roomData.get_srvid()
        gameid = roomData.get_gameid()
        roomid = roomData.get_roomid()
        timestamp = int(pbNotifyBetData.get_timestamp())
        lastbetId = int(pbNotifyBetData.get_roundId())

        self.reqSettlementDataList.uid = self.userWallet
        self.reqSettlementDataList.pageNum = 1
        self.reqSettlementDataList.lastbetId = lastbetId
        self.reqSettlementDataList.lastOperateTimestamp = timestamp
        self.reqSettlementDataList.idx.srvid = srvid  # 服务id
        self.reqSettlementDataList.idx.roomid = roomid  # 房间id
        self.reqSettlementDataList.idx.gameid = gameid  # 游戏id，区别于哪个游戏
        self.reqSettlementDataList.idx.passwd = ''

        hexStr = self.reqSettlementDataList.SerializeToString()
        basePack, packHex = self.base_req(hexStr, "ReqSettlementDataList")

        # 请求数据转为字典
        reqSettlementDataListDict = MessageToDict(self.reqSettlementDataList)
        packDict = MessageToDict(basePack)
        packDict["data"] = reqSettlementDataListDict

        return packHex, packDict


# 解析接收到的响应
class ResponsePack(BasePack):

    def __init__(self):
        super().__init__(game, pack)

    # 响应进入房间
    def rsp_into_room(self, rsp):
        return self.base_rsp(rsp, "RspIntoRoom")

    # 响应请求下注
    def rsp_bet(self, rsp):
        return self.base_rsp(rsp, "RspBet")

    # 游戏开始
    def notify_start(self, rsp):
        return self.base_rsp(rsp, "NotifyStart")

    def notify_betting(self, rsp):
        return self.base_rsp(rsp, "NotifyBetting")

    # 游戏结束
    def notify_finish(self, rsp):
        return self.base_rsp(rsp, "NotifyFinish")

    # 等待开奖
    def notify_wait(self, rsp):
        return self.base_rsp(rsp, "NotifyWait")

    # 下注信息响应
    def rsp_settlement_data_list(self, rsp):
        return self.base_rsp(rsp, "RspSettlementDataList")

    # 下注广播消息
    def pb_notify_bet(self, rsp):
        return self.base_rsp(rsp, "PBNotifyBet")

    # 成功转账
    def pb_notify_self_bet(self, rsp):
        return self.base_rsp(rsp, "PBNotifySelfBet")

    def notify_wicc_settlement(self, rsp):
        return self.base_rsp(rsp, "NotifyWiccSettlement")
