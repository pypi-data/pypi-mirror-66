# -*- coding: utf-8 -*-
class IMarketApi(object):
    """行情接口"""

    def __init__(self,event_bus):
        """构造函数"""
        pass

    def Init(self,strategyID):
        """初始化"""
        pass

    def Subscribe(self,subInfos):
        """行情订阅"""
        pass

    def Unsubscribe(self,subInfos):
        """取消订阅"""
        pass

    def GetHisBar(self,symbol, exchange, barType, startTime, endTime):
        """获取历史K线数据"""
        pass

