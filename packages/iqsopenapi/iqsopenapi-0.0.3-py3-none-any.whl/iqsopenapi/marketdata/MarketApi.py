# -*- coding: utf-8 -*-
from iqsopenapi.models import *
from iqsopenapi.util import *
from iqsopenapi.marketdata.message import *
from iqsopenapi.marketdata.IMarketApi import *
from iqsopenapi.core import *
from iqsopenapi.environment import *
import json
import time
import uuid
import iqsopenapi.util.logutil
import datetime
import traceback
import threading


class MarketApi(IMarketApi):
    """行情接口"""

    def __init__(self,event_bus):
        """构造函数"""
        super(MarketApi,self).__init__(event_bus)

        self.__event_bus = event_bus

        #自动重连检测时间
        self.__AutoReconnectInterval = 10

        cfg = websocketCfg()
        cfg.address = Environment.get_instance().get_quoteaddr()
        cfg.hbContent = json.dumps({ 'requestType' : 'HeartBeat','reqID' : '' })
        cfg.recvCallback = self.__OnRecv
        self.__wsClient = WebSocketClient(cfg)
        self.subscribes = []
        self.__responseMsgCache = MemCache()

    def Init(self):
        """初始化"""
        ret = self.__wsClient.Connect()

        t = threading.Thread(target=self.__AuotReconnect,args=(self.__wsClient,))
        t.start()
        return True

    def __AuotReconnect(self,client):
        """自动连接"""
        while True:
            try:
                if not client.IsConnected():
                    logger.debug("未连接，尝试连接...")
                    ret = client.Connect()
                    logger.debug("重连完成：{0}".format(ret))

                    if len(self.subscribes) > 0:
                        logger.debug("连接成功，开始订阅...")
                        subRet = self.Subscribe(*self.subscribes)
                        logger.debug("连接成功，订阅完成：{0}".format(subRet))
            except Exception as e:
                logger.error(e)
            time.sleep(self.__AutoReconnectInterval)

    def __OnRecv(self,msg):
        '''收到行情消息'''

        if not msg:
            return
        responseType = msg.get("rt")
        datas = msg.get("data")
        if responseType == ResponseType.Reply.name:
            self.__responseMsgCache.set(msg.get("ReqID"), msg, 60)
            return
        if responseType == ResponseType.TickData.name:
            for item in datas:
                tick = self.__ToTickData(item)
                if not tick:
                    return
                tick_event = Event(EVENT.On_Tick,data = tick)
                self.__event_bus.publish_event(tick_event)
        if responseType == ResponseType.KlineData.name:
            for item in datas:
                bar = self.__ToBar(item)
                if not bar:
                    return
                bar_event = Event(EVENT.On_Bar,data = bar)
                self.__event_bus.publish_event(bar_event)

    def Subscribe(self,*subInfos):
        """行情订阅"""
        if not subInfos:
            logger.error('订阅参数不能为空')
            return False
        if not self.__wsClient.IsConnected():
            logger.error('行情未连接')
            return False
        req = SubscribeReq()
        req.ReqID = uuid.uuid1().hex
        req.RequestType = RequestType.Subscribe
        req.Subscribes = subInfos
        message = json.dumps(req.__dict__,ensure_ascii=False)
        if not self.__Send(req.ReqID,message):
            logger.error("send fail:{0}".format(message))
            return False
        for x in subInfos:
            if x not in self.subscribes:
                self.subscribes.append(x)
        return True

    def __Send(self,id,msg):
        """消息发送"""
        if not msg:
            return False
        if not self.__wsClient.Send(msg):
            logger.error("send fail:{0}".format(msg))
            return False
        i = 0
        while i < 60:
            reply = self.__responseMsgCache.get(id)
            if reply:
                self.__responseMsgCache.delete(id)
                return reply["ErrorNo"] == 0
            i += 1
            time.sleep(0.1)
        return False


    def Unsubscribe(self,*subInfos):
        """取消订阅"""
        if not subInfos:
            logger.error('订阅参数不能为空')
            return False
        if not self.__wsClient.IsConnected():
            logger.error('行情未连接')
            return False
        req = UnsubscribeReq()
        req.ReqID = uuid.uuid1().hex
        req.RequestType = RequestType.Unsubscribe
        req.Unsubscribes = subInfos
        message = json.dumps(req.__dict__,ensure_ascii=False)
        if not self.__Send(req.ReqID,message):
            logger.error("send fail:{0}".format(message))
            return False
        for x in subInfos:
            if x in self.subscribes:
                self.subscribes.remove(x)
        return True

    def GetHisBar(self, symbol, exchange, barType, startTime, endTime):
        """获取历史K线数据"""
        if not symbol:
            logger.error("合约代码不能为空")
            return None
        url = Environment.get_instance().get_apiurl('api/MarketData/GetHisBar')
        params = {'symbol':symbol,'exchange':exchange,'dataType':barType,'begin':startTime,'end':endTime}
        resp = httpJsonPost(url,params) 
        strParams = json.dumps(params,ensure_ascii=False)
        if not resp:
            logger.error("请求应答为空：" + url + "," + strParams)
            return None
        js = json.loads(resp,encoding='utf-8')
        if js.get('error_no') != 0:
            logger.error("request:" + url + "," + strParams + "response：" + resp)
            return None
        data = js.get('data')
        if not data:
            return None
        result = []
        for x in data:
            bar = self.__ToBar(x)
            result.append(bar)
        return result

    def __ToBar(self,data):
        #消息长度可能会增加
        if not data:
            return None
        bar = BarData()
        bar.Symbol = data.get("s")
        bar.Exchange = Exchange[data.get("e")]
        bar.DataType = int(data.get("d"))
        bar.LocalTime = datetime.datetime.strptime(data.get("t"),'%Y-%m-%d %H:%M:%S') 
        bar.PreClosePx = float(data.get("pc"))
        bar.OpenPx = float(data.get("o"))
        bar.HighPx = float(data.get("h"))
        bar.LowPx = float(data.get("l"))
        bar.ClosePx = float(data.get("c"))
        bar.Volume = int(data.get("v"))
        bar.Amount = int(data.get("a"))
        bar.OpenInterest = int(data.get("oi"))
        bar.SettlementPx = int(data.get("sp"))
        return bar

    def __ToTickData(self,data):
        if not data:
            return None
        tick = TickData()
        tick.Symbol = data.get("s")
        tick.Exchange = Exchange[data.get("e")]
        tick.LocalTime = datetime.datetime.strptime(data.get("t"),'%Y-%m-%d %H:%M:%S') 
        tick.LastPx = float(data.get("px"))
        tick.OpenPx = float(data.get("o"))
        tick.HighPx = float(data.get("h"))
        tick.LowPx = float(data.get("l"))
        tick.UpLimitPx = float(data.get("up"))
        tick.DownLimitPx = float(data.get("dw"))
        tick.PreClosePx = float(data.get("pc"))
        tick.Volume = int(data.get("v"))
        tick.OpenInterest = int(data.get("oi"))
        tick.SettlementPx = int(data.get("sp"))
        bids = data.get("bid")
        for x in bids:
            unit = LevelUnit()
            unit.Px = float(x['p'])
            unit.Vol = int(x['v'])
            tick.Bids.append(unit)
        asks = data.get("ask")
        for x in asks:
            unit = LevelUnit()
            unit.Px = float(x['p'])
            unit.Vol = int(x['v'])
            tick.Asks.append(unit)
        return tick

if __name__ == '__main__':

    from iqsopenapi.core.events import *

    environment = Environment(None)

    event_bus = EventBus()

    event_bus.add_listener(EVENT.On_Bar,lambda msg:logger.info('bar:{0},{1},{2}'.format(msg.data.Symbol,msg.data.LocalTime,msg.data.ClosePx)))

    event_bus.add_listener(EVENT.On_Tick,lambda msg:logger.info('tick:{0},{1},{2}'.format(msg.data.Symbol,msg.data.LocalTime,msg.data.LastPx)))

    api = MarketApi(event_bus)
    api.Init()
    
    init_event = Event(EVENT.On_Init)
    event_bus.publish_event(init_event)

    event_bus.start()

    ret1 = api.Subscribe("rb2010.SHFE.TICK.0","rb2010.SHFE.BAR.300","rb2005.SHFE.TICK.0")

    ret2 = api.Unsubscribe("rb2005.SHFE.TICK.0")

    ret3 = api.GetHisBar("rb2010",Exchange.SHFE,60,20200220000000,20200420230000)

    pass