import requests
import json

headers = {"Content-Type": "application/json"}


def get_block_height():
    """
    获取当前区块链高度
    """
    url = "http://10.0.0.4:21052/block/getblockcount"
    res = requests.post(url=url, headers=headers)
    height = res.json()["data"]
    return height


def get_signature(kwargs):
    """
    转账交易获取上链签名数据
    """
    url = "http://10.0.0.4:21052/account/sign"
    data = {
        "coinAmount": 100000000,
        "destAddr": "wgd32jw7btMuYvC6rWny1meqopLZiYJkyo",
        "fees": 1000000,
        "coinSymbol": "WUSD",
        "feeSymbol": "WUSD",
        "height": get_block_height(),
        "momo": "",
        "privKey": "Y7UiVRpTAZNDtZakSHZwebHD6romu9jcuj1tjjujzwbSqdKLCEQZ"
    }
    data.update(kwargs)
    data = json.dumps(data)
    result = requests.post(url, data=data, headers=headers)
    signature = result.json()["data"]
    return signature
