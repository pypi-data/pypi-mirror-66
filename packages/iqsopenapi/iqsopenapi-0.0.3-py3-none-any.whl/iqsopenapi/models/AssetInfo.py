# -*- coding: utf-8 -*-
from enum import IntEnum
from iqsopenapi.models.Contract import *

class AssetInfo(object):
    """资产信息"""

    def __init__(self):

        """券商账户编号"""
        self.StrategyID = 0

        """总资产"""
        self.TotalAsset = 0.0

        """可用资金"""
        self.Available = 0.0

        """余额"""
        self.Balance = 0.0

        """保证金"""
        self.Margin = 0.0

        """初始资产"""
        self.InitAsset = 0.0

        self.Withdraw = 0.0

        """币种"""
        self.Currency = Currency.CNY


