﻿# -*- coding: utf-8 -*- 

from datetime import *
from iqsopenapi.models.Contract import *

class BarData(object):
    """历史数据模型"""

    def __init__(self):

        """合约或股票代码名称"""
        self.Symbol = ""

        """交易所"""
        self.Exchange = Exchange.UnKnow

        """周期类型以秒计算"""
        self.DataType = 0

        """时间"""
        self.LocalTime = datetime.now()

        """昨收"""
        self.PreClosePx = 0.0

        """开盘价"""
        self.OpenPx = 0.0

        """最高价"""
        self.HighPx = 0.0

        """最低价"""
        self.LowPx = 0.0

        """收盘价"""
        self.ClosePx = 0.0

        """成交量"""
        self.Volume = 0

        """成交额"""
        self.Amount = 0.0      

        """持仓量"""
        self.OpenInterest = 0

        """结算价"""
        self.SettlementPx = 0.0  


        

        

        

        

        

        


