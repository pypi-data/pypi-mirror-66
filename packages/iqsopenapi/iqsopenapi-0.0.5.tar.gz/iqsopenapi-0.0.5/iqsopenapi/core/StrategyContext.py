# -*- coding: utf-8 -*-

from iqsopenapi.environment import Environment 

class StrategyContext(object):
    """
    策略上下文
    """
    def __init__(self):
        """初始化"""
        pass
   
    def subscribe(self,*subInfos):
        """行情订阅"""
        return Environment.get_instance().market_api.Subscribe(*subInfos)

    def unsubscribe(self,*subInfos):
        """取消订阅"""
        return Environment.get_instance().market_api.Unsubscribe(*subInfos)

    def get_subscribelist(self):
        """获取订阅列表"""
        return Environment.get_instance().market_api.GetSubscibes()

    def get_contract(self, symbol, exchange):
        """获取合约信息"""
        return Environment.get_instance().basicdata_api.GetContract(symbol, exchange)

    def get_domain_contract(self, variety):
        """获取主力合约"""
        return Environment.get_instance().basicdata_api.GetMainContract(variety)

    def get_last_ticks(self, symbol, exchange, count):
        """获取最近几笔tick"""
        return Environment.get_instance().market_api.GetLastTick(symbol, exchange, count)

    def get_last_bars(self, symbol, exchange, barType, count):
        """获取最近几笔bar"""
        return Environment.get_instance().market_api.GetLastBar(symbol, exchange, barType, count)

    def get_history_bars(self, symbol, exchange, barType, startTime, endTime):
        """获取历史bar"""
        return Environment.get_instance().market_api.GetHisBar(symbol, exchange, barType, startTime, endTime)

    def get_history_ticks(self, symbol, exchange, startTime, endTime):
        """获取订阅列表"""
        return Environment.get_instance().market_api.GetHisTick(symbol, exchange, startTime, endTime)