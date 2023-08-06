# -*- coding: utf-8 -*-
from enum import IntEnum

class TradeCounterType(IntEnum):
    ''' 柜台类型 '''

    ''' 默认-无 '''
    NONE=0
    ''' CTP '''
    CTP = 1
    ''' 恒生 '''
    HS = 2
    ''' 顶点 '''
    DD = 3
    ''' 金仕达 '''
    JSD = 4
    ''' 飞马 '''
    FM = 5
    
class OffSet(IntEnum):
    ''' 开平仓方向 '''

    ''' 未知 '''
    UnKnown=0
    ''' 开仓 '''
    Open=1
    ''' 平仓 '''
    Close=2
    ''' 平今 '''
    CloseToday=3
    ''' 平昨 '''
    CloseYesterday=4
    ''' 快平 '''
    QuickClose=5

class OrderType(IntEnum):
    ''' 委托类型 '''

    ''' 限价 '''
    LMT=0
    ''' 市价(即涨跌停价) '''
    MKT=1
    ''' 对手价 '''
    DST=2
    ''' 排队价 '''
    PDT=3
    
class ConOrderTimeValidTypeEnum(IntEnum):
    ''' 条件单查询日期类型 '''

    ''' 当前交易日有效 '''
    CurrentTradingDayValid=-1
    ''' 永久有效 '''
    ForverValid=0