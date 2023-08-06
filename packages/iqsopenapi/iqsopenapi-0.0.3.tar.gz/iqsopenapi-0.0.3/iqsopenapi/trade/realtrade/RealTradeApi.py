# -*- coding: utf-8 -*-
from iqsopenapi.util.HttpUtil import *
from iqsopenapi.util.logutil import *
from iqsopenapi.util.MemCache import *
from iqsopenapi.util.DES3Cryptogram import *
from iqsopenapi.util.ParseManager import *
from iqsopenapi.util.SupervisionHelper import *
from iqsopenapi.trade.ITradeApi import *
from iqsopenapi.models.Order import *
from iqsopenapi.models.AssetInfo import *
from iqsopenapi.models.Position import *
from iqsopenapi.models.Models import *
from iqsopenapi.enums.Enums import *
from urllib.parse import quote
import string
import json
import time
import uuid
import iqsopenapi.util.logutil
import datetime
from concurrent.futures.thread import ThreadPoolExecutor

class RealTradeApi(ITradeApi):
    """期货交易"""

    def __init__(self,strategyID,orderChangedCallback):
        """构造函数"""
        super().__init__(strategyID,orderChangedCallback)
        self.__strategyID = strategyID
        self.__orderChangedCallback = orderChangedCallback
        self.__userInfo = None
        dir = os.path.abspath('inquant/Supervision')
        self.__supervision_helper = SupervisionHelper(dir)
        self.__passwordKey = 'password'
        self.__tradeTokenKey = 'tradeToken'
        self.__cache = MemCache()
        self.__post_fix = f'?strategyID={strategyID}'
        self.__loginUrl = self.__encodeUrl(f'gateway/login.ashx{self.__post_fix}')
        self.__sendOrderUrl = self.__encodeUrl(f'gateway/sendorder.ashx{self.__post_fix}')
        self.__cancelOrderUrl = self.__encodeUrl(f'gateway/cancelorder.ashx{self.__post_fix}')
        self.__qryEntrustUrl = self.__encodeUrl(f'gateway/qryorder.ashx{self.__post_fix}')
        self.__fundUrl = self.__encodeUrl(f'gateway/qryasset.ashx{self.__post_fix}')
        self.__positionUrl = self.__encodeUrl(f'gateway/qryposition.ashx{self.__post_fix}')
        self.__executor = ThreadPoolExecutor(max_workers=1)
        
    def AccountLogin(self, account):
        """登录"""
        borkerType = account.BrokerType
        counterId = account.CounterID
        addr = account.CounterAddr
        userName = account.AccountID
        password = account.PassWord
        url = f'{addr}{self.__loginUrl}'
        kvp = [
            kv('brokerType', borkerType), 
            kv('accountID', userName), 
            kv(self.__passwordKey, password), 
            kv('counterID', counterId)]
        js = self.__supervision_helper.SetInfo(account.SupInfo)
        kvp[len(kvp):len(js)] = js
        param = self.__getJson(kvp)
        info = self.__post_crypt_core(url, param, ParseLoginResult)
        if not info or info.ErrorNo != 0:
            self.__wirteError(f'AccountLogin, {param}\n\t{info.Json}')
            return None
        else: 
            self.__wirteInfo(f'AccountLogin, {param}\n\t{info.Json}')
            self.__delete_cache()
            return info

    def SendOrder(self, order):
        """下单"""
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__sendOrderUrl}'
        kvp = [
            kv(self.__tradeTokenKey, account.TradeToken), 
            kv(self.__passwordKey, account.PassWord), 
            kv('clientOrderID', order.OrderID), 
            kv('symbol', order.Symbol), 
            kv('exchange', order.Exchange.name), 
            kv('orderSide', order.OrderSide.name), 
            kv('price', order.Price), 
            kv('quantity', order.Quantity), 
            kv('orderType', order.OrderType.value), 
            kv('offset', order.OffSet.value)]
        param = self.__getJson(kvp)
        #self.__executor.submit(self.__raiseOrderChanged,order)
        js = self.__post_crypt_core(url, param, ParseBaseModel)

        if not js or js.ErrorNo != 0:
            self.__wirteError(f'SendOrder, {param}\n\t{js.Json}')
            neworder = self.CreateNewOrder(order)
            neworder.Status = OrderStatus.Rejected
            neworder.Note = js.ErrorInfo
            #self.__executor.submit(self.__raiseOrderChanged,neworder)
            return False
        else:
            self.__wirteInfo(f'SendOrder, {param}\n\t{js.Json}')
            ''' 实盘接口不返回订单id，无法查询订单状态 '''
            #result = self.__getEntrustInfos(order.OrderID)
            #if not result: return True #即使查询不成功也返回下单成功
            #neworder = self.CreateNewOrder(order)
            #neworder.Filled = js["filled"]
            #neworder.FilledPx = js["filledPx"]
            #neworder.FilledTime = datetime.datetime.strptime(js["filledTime"],'%Y-%m-%d %H:%M:%S')
            #neworder.Status = OrderStatus(js["status"])
            #neworder.TradeDate = datetime.datetime.strptime(js["tradeDate"],'%Y-%m-%d %H:%M:%S')
            #self.__executor.submit(self.__raiseOrderChanged,neworder)
            return True

    def CancelOrder(self,orderID,clientOrderID):
        """撤单"""
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__cancelOrderUrl}'
        kvp = [
            kv(self.__tradeTokenKey, account.TradeToken), 
            kv(self.__passwordKey, account.PassWord), 
            kv('orderID', orderID)]
        param = self.__getJson(kvp)
        js = self.__post_crypt_core(url, param, ParseBaseModel)
        if not js or js.ErrorNo != 0:
            self.__wirteError(f'CancelOrder, {param}\n\t{js.Json}')
            return False
        else:
            self.__wirteInfo(f'CancelOrder, {param}\n\t{js.Json}')
            return True

    def GetAssetInfo(self):
        """获取资产信息"""
        cache = self.__cache.get(self.__fundUrl)
        if cache: return cache
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__fundUrl}'
        kvp = [
            kv(self.__tradeTokenKey, account.TradeToken), 
            kv(self.__passwordKey, account.PassWord)]
        param = self.__getJson(kvp)
        js = self.__post_crypt_core(url, param, ParseUserAssetsModel)
        if not js or js.ErrorNo != 0:
            self.__wirteError(f'GetAssetInfo, {param}\n\t{js.Json}')
            return None
        else:
            self.__wirteInfo(f'GetAssetInfo, {param}\n\t{js.Json}')
            asset = js.AssetInfo
            asset.StrategyID = self.__strategyID
            #5分钟缓存
            self.__cache.set(self.__fundUrl,asset,60 * 5)
            return asset

    def GetOrder(self,clientOrderID):
        """根据内联ID号 获取订单详情"""
        orders = self.GetOrders()
        if not orders:
            None
        for x in orders:
            if x.OrderID == clientOrderID:
                return x
        return None

    def GetOpenOrders(self):
        """获取打开的订单"""
        orders = self.GetOrders()
        if not orders:
            None
        openOrders = []
        for x in orders:
            if x.Status != OrderStatus.Cancelled and x.Status != OrderStatus.Filled and x.Status != OrderStatus.Filled:
                openOrders.append(x)
        return openOrders

    def GetOrders(self):
        """获取当日委托"""
        cache = self.__cache.get(self.__qryEntrustUrl)
        if cache: return cache
        info = self.__getEntrustInfos()
        info.ErrorHandle('获取当日委托')
        orders = info.EntrustInfos
        for order in orders:
            order.StrategyID = self.__strategyID
        #5分钟缓存
        self.__cache.set(self.__qryEntrustUrl,orders,60 * 5)
        return orders

    def GetPositions(self):
        """获取持仓"""
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__positionUrl}'
        kvp = [
            kv(self.__tradeTokenKey, account.TradeToken), 
            kv(self.__passwordKey, account.PassWord), 
            kv('qryFund', 1)]
        kvp[len(kvp):len(js)] = js
        param = self.__getJson(kvp)
        info = self.__post_crypt_core(url, param, ParsePositionModel)
        if not info or info.ErrorNo != 0:
            self.__wirteError(f'GetPositions, {param}\n\t{info.Json}')
            return None
        else: 
            self.__wirteInfo(f'GetPositions, {param}\n\t{info.Json}')
            positions = info.Position
            for item in positions:
                item.StrategyID = self.__strategyID
            #5分钟缓存
            self.__cache.set(self.__positionUrl,positions,60 * 5)
            return positions

    def __raiseOrderChanged(self,order):
        '''触发订单改变事件'''
        if not order: return
        self.__delete_cache()
        if self.__orderChangedCallback != None:
            self.__orderChangedCallback(order)

    def __delete_cache(self):
        '''删除缓存'''
        self.__cache.delete(self.__qryEntrustUrl)
        self.__cache.delete(self.__fundUrl)
        self.__cache.delete(self.__positionUrl)

    def __getEntrustInfos(self, id=None):
        account = self.__getUserInfo()
        url = f'{account.CounterAddr}{self.__qryEntrustUrl}'
        kvp = [kv(self.__tradeTokenKey, account.TradeToken)]
        if id != None:
            kvp[len(kvp):1] = [kv('orderID', id)]
        param = self.__getJson(kvp)
        info = self.__post_crypt_core(url, param, ParseEntrustModel)
        if not info or info.ErrorNo != 0:
            self.__wirteError(f'__getEntrustInfos, {param}\n\t{info.Json}')
            return None
        else: 
            self.__wirteInfo(f'__getEntrustInfos, {param}\n\t{info.Json}')
            return info

    def CreateNewOrder(self, order=None):
        neworder = Order()
        neworder.Exchange = Exchange.UnKnow
        neworder.Filled = 0
        neworder.FilledPx = 0
        neworder.FilledTime = datetime.datetime(1970, 1, 1)
        neworder.Note = ''
        neworder.Offset = OffSet.UnKnown
        neworder.OrderID = uuid.uuid1().hex
        neworder.OrderSide = OrderSide.Buy
        neworder.OrderTime = datetime.datetime.now()
        neworder.OrderType = OrderType.LMT
        neworder.Price = 0
        neworder.Quantity = 0
        neworder.StrategyID = self.__strategyID
        neworder.Symbol = ''
        if order != None:
            neworder.Exchange = order.Exchange
            neworder.Offset = order.OffSet
            neworder.OrderID = order.OrderID
            neworder.OrderSide = order.OrderSide
            neworder.OrderType = order.OrderType
            neworder.Price = order.Price
            neworder.Quantity = order.Quantity
            neworder.Symbol = order.Symbol
        return neworder

    def __getUserInfo(self):
        if(self.__userInfo != None): return self.__userInfo;
        info = UserInfo()
        info.AccountID = '896006290'
        info.PassWord = 'abcd4321'
        info.BrokerType = 151
        info.CounterID = 84
        info.CounterAddr = 'https://trade.inquant.cn/'
        info.SupInfo.TradeCounter = TradeCounterType.FM
        login = trade.AccountLogin(info)
        info.TradeToken = login.TradeToken
        self.__userInfo = info
        return info

    def __encodeUrl(self, url):
        return quote(url, safe=string.printable)

    def __getJson(self, kvp):
        return '{' + ','.join(['"%s":"%s"' % (item.Key, item.Value)  for item in kvp]) + '}'

    def __post_crypt_core(self, url, param, parsecore):
        def parse(x):
            de = decrypt(x.decode('utf-8'))
            return parsecore(json.loads(de))
        en = encrypt(param)
        return parse(httpPost(url, en))

    def __wirteError(self, error):
        '''写错误日志'''
        logutil.writeLog('FutRealTradeApiError', 'E- ;' + error)

    def __wirteInfo(self, info):
        '''写日志'''
        logutil.writeLog('FutRealTradeApi', 'I- ;' + info)

def __object_2_json(x):
    return x.__dict__

if __name__ == '__main__':
    """测试"""
    try:
        raise Exception('未测试')
        logutil.setLogPath("d:/logs/")
        trade = FutRealTradeApi('2-xk1211231243242314123534523453',None)

        position = trade.GetPositions()
        orders = trade.GetOrders()
        assets = trade.GetAssetInfo()

        order = trade.CreateNewOrder()
        order.Symbol = 'c2101'
        order.Exchange = Exchange.DCE
        order.OrderSide = OrderSide.Buy
        order.OffSet = OffSet.Open
        order.OrderType = OrderType.LMT
        order.Price = 1928
        order.Quantity = 1

        sendOrder = trade.SendOrder(account, order)

        orderId = uuid.uuid1().hex
        a1 = trade.SendOrder(orderId,'rb1905',Exchange.SHFE,OrderSide.Buy,0,1,OrderType.MKT,Offset.Open)
        a2 = trade.CancelOrder(orderId)
        a3 = trade.GetAssetInfo()
        a4 = trade.GetOpenOrders()
        a5 = trade.GetOrder(orderId)
        a6 = trade.GetOrders()
        a7 = trade.GetPositions()
    except Exception as e:
        print(e)
    pass
