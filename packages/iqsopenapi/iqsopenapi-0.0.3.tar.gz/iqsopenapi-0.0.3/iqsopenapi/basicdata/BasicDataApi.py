# -*- coding: utf-8 -*-
from iqsopenapi.util.HttpUtil import *
from iqsopenapi.util.logutil import *
from iqsopenapi.basicdata.IBasicDataApi import *
from iqsopenapi.models.Contract import *
from iqsopenapi.environment import *
import json
import datetime

class BasicDataApi(IBasicDataApi):
    """期货数据API"""

    def __init__(self):
        """构造函数"""
        super(BasicDataApi,self).__init__()

    def GetContract(self, symbol, exchange):
        """获取合约信息"""
        url = Environment.get_instance().get_apiurl('api/BasicData/GetContract')
        params = {'symbol':symbol,'exchange':str(int(exchange))}
        strParams = json.dumps(params,ensure_ascii=False)
        resp = httpJsonPost(url,params)
        if not resp:
            logger.error("请求应答为空：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            logger.error("data为空,request:" + url + "," + strParams + "response：" + resp)
            return None
        contract = self.__ToContract(data)
        return contract

    def __ToContract(self,data):
        """根据clientOrderID 获取订单详情"""
        if not data:
            return None
        contract = Contract()
        contract.ContractName = data["contractName"]
        contract.ContractType = ContractType(data["contractType"])
        contract.Exchange = Exchange(data["exchange"])
        contract.ExpiryDate = datetime.datetime.strptime(data["expiryDate"],'%Y-%m-%d')
        contract.ListingDate = datetime.datetime.strptime(data["listingDate"],'%Y-%m-%d')
        contract.Lots = data["lots"]
        contract.PriceStep = data["priceStep"]
        contract.Right = data["right"]
        contract.StrikePx = data["strikePx"]
        contract.Symbol = data["symbol"]
        for x in data['tradeTimes']:
            tradingTime = TradingTime()
            tradingTime.Begin = x['begin']
            tradingTime.End = x['end']
            contract.TradingTimes.append(tradingTime)
        return contract

if __name__ == '__main__':

    environment = Environment(None)

    api = BasicDataApi()
    contract = api.GetContract("rb2005",4)
    logger.info(contract)

