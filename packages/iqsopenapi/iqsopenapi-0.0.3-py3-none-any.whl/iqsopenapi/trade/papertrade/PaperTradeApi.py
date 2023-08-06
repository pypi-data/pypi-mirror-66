# -*- coding: utf-8 -*-
from iqsopenapi.util.HttpUtil import *
from iqsopenapi.util.logutil import *
from iqsopenapi.util.MemCache import *
from iqsopenapi.util.DES3Cryptogram import *
from iqsopenapi.trade.ITradeApi import *
from iqsopenapi.models.Order import *
from iqsopenapi.models.ResultInfo import *
from iqsopenapi.models.AssetInfo import *
from iqsopenapi.models.Position import *
from iqsopenapi.util.WebSocketClient import *
import json
import time
import uuid
import iqsopenapi.util.logutil
import datetime
from concurrent.futures.thread import ThreadPoolExecutor

class PaperTradeApi(ITradeApi):
    """期货模拟交易"""

     #自动重连检测时间
    AutoReconnectInterval = 10

    #行情包头
    heartBeatInternal = 5

    #心跳超时时间
    keepAliveTimeout = 30

    def __init__(self,connectionUrl,apiHost,strategyKey,orderChangedCallback,orderExecutionCallback,orderCancelledCallBack):
        """构造函数"""
        super(PaperTradeApi,self).__init__(connectionUrl,apiHost,strategyKey,orderChangedCallback,orderExecutionCallback,orderCancelledCallBack)
        self.__apiHost = apiHost
        self.__strategyKey = strategyKey
        self.__orderChangedCallback = orderChangedCallback
        self.__orderExecutionCallback = orderExecutionCallback
        self.__orderCancelledCallBack = orderCancelledCallBack
        self.__cache = MemCache()
        self.__executor = ThreadPoolExecutor(max_workers=1)
        self.__client = WebSocketClient(connectionUrl,self.heartBeatInternal,self.keepAliveTimeout,self.__OnRecv,self.__OnError)
        isConnect = self.__client.Connect()
        if(isConnect):
            self.__Subscribe()

    def Init(self):
        """初始化"""
        t = threading.Thread(target=self.__AuotReconnect,args=(self.__client,))
        t.start()
        return True

    def __AuotReconnect(self,client):
        """自动连接"""
        self.__wirteInfo("启动自动连接")
        while True:
            try:
                if not client.IsConnected():
                    self.__wirteInfo("未连接，尝试连接...")
                    isConnect = client.Connect()                    
                    if(isConnect):
                     self.__Subscribe()
                     self.__wirteInfo("重连完成：{0}".format(ret))
            except Exception as e:
                self.__wirteError("重连失败")
            time.sleep(self.AutoReconnectInterval)

    def __Subscribe(self):
        req = SubscribeStgyReq()
        req.ReqID = uuid.uuid1().hex
        req.RequestType = RequestType.Subscribe
        req.StrategyKey = self.__strategyKey
        obj = req.ToDict()
        if not self.__client.Send(obj):
            self.__wirteError("订阅消息发送失败")
            return False
        return True

    def __OnRecv(self,msg):
        '''收到消息'''
        if not msg:
            return
        type = msg.get("rt")
        orders = msg.get("data")
        #委托回报
        if type == ResponseType.OrderChange.name:
            for item in orders:
                if not item:
                    return
                if self.__orderChangedCallback:
                    orderChange = self.__ToOrderChangeData(item)
                    self.__orderChangedCallback(orderChange)
        #成交回报
        if type == ResponseType.OrderExec.name:
            for item in orders:
                if not item:
                    return
                if self.__orderExecutionCallback:
                    orderExecution = self.__ToOrderExecutionData(item)
                    self.__orderExecutionCallback(orderExecution)
        #撤单回报
        if type==ResponseType.OrderCancelled.name:
              for item in orders:
                if not item:
                    return
                if self.__orderCancelledCallBack:
                    orderCancelled = self.__ToOrderExecutionData(item)
                    self.__orderCancelledCallBack(orderCancelled)

    def __ToOrderChangeData(self,orderChange):
        #委托回报
        if not orderChange:
            return None
        data = OrderChange()
        data.OrderId = orderChange.get("OrderId")
        data.ClientOrderId = orderChange.get("ClientOrderId")
        data.TradeAccount = orderChange.get("TradeAccount")
        data.Symbol = orderChange.get("Symbol")
        data.Price = float(orderChange.get("Price"))
        data.Quantity = int(orderChange.get("Quantity"))
        data.OrderType = OrderType[orderChange.get("OrderType")]
        data.OrderSide = OrderSide[orderChange.get("OrderSide")]
        data.Offset = Offset[orderChange.get("Offset")]
        data.OrderTime = datetime.datetime.strptime(orderChange.get("OrderTime"),'%Y-%m-%d %H:%M:%S')
        data.OldStatus = OrderStatus[orderChange.get("OldStatus")]
        data.NewStatus = OrderStatus[orderChange.get("NewStatus")]
        data.OldFilled = int(orderChange.get("OldFilled"))
        data.NewFilled = int(orderChange.get("NewFilled"))
        data.FilledPx = float(orderChange.get("FilledPx"))
        data.FilledTime = datetime.datetime.strptime(orderChange.get("FilledTime"),'%Y-%m-%d %H:%M:%S')
        data.Note = orderChange.get("Note")        
        data.Tag = orderChange.get("Tag")        
        return data

    def __ToOrderExecutionData(self,orderExecution):
        #成交回报
        if not orderExecution:
            return None
        data = OrderExecution()
        data.ClientOrderId = orderExecution.get("ClientOrderId")
        data.OrderId = orderExecution.get("OrderID")
        data.TradeAccount = orderExecution.get("TradeAccount")
        data.Status = OrderStatus(int(orderExecution.get("Status")))
        data.Symbol = orderExecution.get("Symbol")
        data.Exchange = Exchange(int(orderExecution.get("Exchange")))
        data.OrderSide = OrderSide[orderExecution.get("OrderSide")]
        data.OrderType = OrderType[orderExecution.get("OrderType")]
        data.Offset = Offset[orderExecution.get("Offset")]
        data.Quantity = int(orderExecution.get("Quantity"))
        data.Price = float(orderExecution.get("Price"))
        data.Filled = int(orderExecution.get("Filled"))
        data.FilledPx = float(orderExecution.get("FilledPx"))
        data.Fee = float(orderExecution.get("Fee"))
        data.OrderTime = datetime.datetime.strptime(orderExecution.get("OrderTime"),'%Y-%m-%d %H:%M:%S')
        data.FilledTime = datetime.datetime.strptime(orderExecution.get("FilledTime"),'%Y-%m-%d %H:%M:%S')
        data.UpdateTime = datetime.datetime.strptime(orderExecution.get("UpdateTime"),'%Y-%m-%d %H:%M:%S')
        return data

    def __OnError(self,excp):
        '''发生错误时触发'''
        if not excp:
            return
        log = str(excp)
        log += traceback.format_exc()
        self.__wirteError(log)
        
    def SendOrder(self,clientOrderID, symbol, exchange, orderSide, price, quantity, orderType, offset,tag):
        """下单"""
        if not symbol or symbol == '':
            self.__wirteError("symbol不能为空")
            return ResultInfo(-1,"symbol不能为空")
        if not isinstance(quantity, int):
            self.__wirteError("quantity必须为整数:{0},{1}".format(quantity,symbol))
            return ResultInfo(-1,"quantity必须为整数:{0},{1}".format(quantity,symbol))
        if orderSide == OrderSide.Buy:
            orderSide = "B"
        if orderSide == OrderSide.Sell:
            orderSide = "S"
        self.__wirteInfo("准备下单，symbol:{0},exchange:{1},orderSide:{2},offset:{3},orderType:{4},price:{5},quantity:{6},orderID:{7}".format(symbol, exchange.name, orderSide, offset.name, orderType.name, price, quantity, clientOrderID))

        params = {'symbol':symbol,'exchange':int(exchange),'orderSide':orderSide,'price':price,'quantity':quantity,'orderType':int(orderType),'offset':int(offset),'strategyKey':self.__strategyKey,'clientOrderId':clientOrderID,'tag':tag}
        url = self.__apiHost + "PaperTrade/SendOrder"
        resp = httpJsonPost(url, params)
        data = json.dumps(params,ensure_ascii=False)

        if not resp:
            self.__wirteError("请求应答为空：" + url + "," + data)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError("下单失败,request:" + url + "," + data + "response：" + resp)
            return None
        
        resData = js.get('data')
        self.__wirteInfo("下单完成，request:" + url + "," + data + "response：" + resp)
        return True

    def CancelOrder(self,clientOrderID):
        """撤单"""
        params = {'ClientOrderId':clientOrderID}
        url = self.__apiHost + 'PaperTrade/CancelOrder'
        resp = httpJsonPost(url,params)        
        data = json.dumps(params,ensure_ascii=False)
        if not resp:
            self.__wirteError("请求应答为空：" + url + "," + data)
            return False
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError("request:" + url + "," + data + "response：" + resp)
            return False
        return True

    def GetAssetInfo(self):
        """获取资产信息"""

        url = self.__apiHost + 'PaperTrade/GetAccount'
        params = {'StrategyId':self.__strategyKey}
        cacheKey = url + "." + self.__strategyKey
        cache = self.__cache.get(cacheKey)
        if cache:
            return cache        
        resp = httpJsonPost(url,params)
        data = json.dumps(params,ensure_ascii=False)
        if not resp:
            self.__wirteError("请求应答为空：" + url + "," + data)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError("request:" + url + "," + data + "response：" + resp)
            return None
        resData = js['data']
        asset = AssetInfo()
        asset.StrategyID = resData['strategyID']
        asset.Margin = resData['margin']
        asset.Balance = resData['balance']
        asset.TotalAsset = resData['total']
        asset.Available = resData['available']
        asset.InitAsset = resData['initAsset']
        asset.Withdraw = resData['withdraw']
        asset.Currency = Currency.CNY
        #5分钟缓存
        self.__cache.set(cacheKey,asset,60 * 5)
        return asset

    def GetOrder(self,clientOrderId):
        """根据订单ID号 获取订单详情"""
        orders = self.GetOrders()
        if not orders:
           return None
        for x in orders:
            if x.ClientOrderId == clientOrderId:
                return x
        return None

    def GetOpenOrders(self):
        """获取打开的订单"""
        orders = self.GetOrders()
        if not orders:
           return None
        openOrders = []
        for x in orders:
            if x.OrderStatus != OrderStatus.Cancelled and x.OrderStatus != OrderStatus.Filled and x.OrderStatus != OrderStatus.Rejected:
                openOrders.append(x)
        return openOrders

    def GetOrders(self):
        """获取委托"""
        url = self.__apiHost + 'PaperTrade/GetOrders'
        params = {'StrategyId':self.__strategyKey}
        cacheKey = url + "." + self.__strategyKey
        cache = self.__cache.get(cacheKey)
        if cache:
            return cache
        resp = httpJsonPost(url,params)
        data = json.dumps(params,ensure_ascii=False)
        if not resp:
            self.__wirteError("请求应答为空：" + url + "," + data)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError("request:" + url + "," + data + "response：" + resp)
            return None
        resData = js.get('data')
        if not resData:
            return None
        orders = []
        for item in resData:
            order = Order()
            order.Exchange = Exchange(item['exchange'])
            order.Filled = item['filled']
            order.FilledPx = item['filledPx']
            order.FilledTime = datetime.datetime.strptime(item['filledTime'],'%Y-%m-%d %H:%M:%S')
            order.Tag = item['tag']
            order.Note = item['note']
            order.Offset = Offset(item['offset'])
            order.OrderId = item['orderId']
            order.ClientOrderId = item['clientOrderId']
            order.OrderSide = OrderSide(item['orderSide'])
            order.OrderTime = datetime.datetime.strptime(item['orderTime'],'%Y-%m-%d %H:%M:%S')
            order.OrderType = OrderType(item['orderType'])
            order.Price = item['price']
            order.Quantity = item['quantity']
            order.OrderStatus = OrderStatus(item['orderStatus'])
            order.Symbol = item['symbol']
            order.TradeDate = datetime.datetime.strptime(item['tradeDate'],'%Y-%m-%d %H:%M:%S')
            order.StrategyKey = self.__strategyKey
            orders.append(order)
        #5分钟缓存
        self.__cache.set(cacheKey,orders,60 * 5)
        return orders

    def GetPositions(self):
        """获取持仓"""
        url = self.__apiHost + 'PaperTrade/GetPositions'
        params = {'StrategyId':self.__strategyKey}
        cacheKey = url + "." + self.__strategyKey
        cache = self.__cache.get(cacheKey)
        if cache:
            return cache
        resp = httpJsonPost(url,params)
        if not resp:
            self.__wirteError("请求应答为空：" + url + "," + data)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            self.__wirteError("request:" + url + "," + data + "response：" + resp)
            return None
        resData = js.get('data')
        if not resData:
            return None
        posList = []
        for item in resData:
            pos = Position()
            pos.Exchange = Exchange(item['exchange'])
            pos.TradeAccount = item['tradeAccount']
            pos.Frozen = item['frozen']
            pos.Margin = item['margin']
            pos.PosSide = PosSide(item['posSide'])
            pos.Quantity = item['quantity']
            pos.Symbol = item['symbol']
            pos.CostPx = item['costPx']
            pos.StrategyKey = self.__strategyKey
            posList.append(pos)
        #5分钟缓存
        self.__cache.set(cacheKey,posList,60 * 5)
        return posList

    def __wirteError(self,error):
        '''写错误日志'''
        logutil.writeLog('PaperTradeApiError',error)

    def __wirteInfo(self,info):
        '''写日志'''
        logutil.writeLog('PaperTradeApi',info)

