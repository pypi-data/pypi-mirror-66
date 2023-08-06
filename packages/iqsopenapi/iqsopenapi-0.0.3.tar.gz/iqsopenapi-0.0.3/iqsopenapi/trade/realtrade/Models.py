# -*- coding: utf-8 -*-
from iqsopenapi.models.AssetInfo import *
from iqsopenapi.models.BarData import *
from iqsopenapi.models.Contract import *
from iqsopenapi.models.KlineData import *
from iqsopenapi.models.Order import *
from iqsopenapi.models.Position import *
from iqsopenapi.models.TickData import *

class kv:
    def __init__(self, key, value):
        self.Key = str(key)
        self.Value = str(value)

class ReposeModelBase:
    def __init__(self):
        self.ErrorNo = 0
        self.ErrorInfo = ''
    def ErrorHandle(self, flag):
        if (self.ErrorNo != 0): raise Exception(f'[{flag}错误]-{self.ErrorInfo}')

class FuturesCompanysModel(ReposeModelBase):
    def __init__(self):
        super().__init__()
        self.CompanyInfos = []
        self.ArgeementHerfText = ''
        self.ArgeementHerf = ''
        self.ArgeementTip = ''
        self.AppQRImage = ''

class LoginResult(ReposeModelBase):
    def __init__(self):
        super().__init__()
        self.TradeToken = ''
        self.IsSigned = False

class TradeCounterModel(ReposeModelBase):
    def __init__(self):
        super().__init__()
        self.CounterList = []

class PositionModel(ReposeModelBase):
    def __init__(self):
        super().__init__()
        self.PositionInfos = []

class EntrustModel(ReposeModelBase):
    def __init__(self):
        super().__init__()
        self.EntrustInfos = []

class ConOrderModel(ReposeModelBase):
    def __init__(self):
        super().__init__()
        self.Data = []

class StopOrderNotTriggerModel(ReposeModelBase):
    def __init__(self):
        super().__init__()
        self.Data = []

class UserAssetsModel(ReposeModelBase):
    def __init__(self):
        super().__init__()
        self.AssetInfo = AssetInfo()

class PositionModel(ReposeModelBase):
    def __init__(self):
        super().__init__()
        self.Position = Position()

class StopOrderNotTrigger:
    def __init__(self):
        self.StopId = -1
        self.Symbol = ''
        self.Name = ''
        self.PosSide = PosSide.Net
        self.PosSideStr = ''
        self.StopType = -1
        self.StopTypeStr = ''
        self.TriggerPrice = 0.0
        self.OrderType = -1
        self.OrderTypeStr = ''
        self.Quantity = -1
        self.StatusStr = '进行中'

class ConditionOrderEntity:
    def __init__(self):
        self.ConditionId = -1
        self.Symbol = ''
        self.ContractId = -1
        self.Status = -1
        self.StatusStr = ''
        self.OrderSide = OrderSide.Buy
        self.OrderSideStr = ''
        self.OffSet = OffSet.UnKnown
        self.OffSetStr = ''
        self.OrderType = OrderType.LMT
        self.OrderTypeStr = ''
        self.Price = ''
        self.Quantity = -1
        self.ExpireType = ConOrderTimeValidTypeEnum.CurrentTradingDayValid
        self.AddTimeStr = ''
        self.ExpireTimeStr = ''
        self.CondiValues = []
        self.CondiValueStr = ''
        self.OrderNo = -1
        self.OrderRet = ''
        self.OrderNote = ''
        self.TriggerTimeStr = ''

class EntrustInfo:
    def __init__(self):
        self.OrderId = ''
        self.Symbol = ''
        self.Exchange = Exchange.UnKnow
        self.OrderSide = OrderSide.Buy
        self.OffSet = OffSet.UnKnown
        self.Quantity = -1
        self.Price = ''
        self.OrderStatusStr = ''
        self.OrderTime = ''
        self.OrderTimeStr = ''
        self.OrderStatus = OrderStatus.UnKnow
        self.ErrorMsg = ''
        self.Filled = -1
        self.LastPx = ''
        self.CanCancel = -1
        self.Canceled = -1
        self.ClientOrderID = -1

class PositionInfo:
    def __init__(self):
        self.ContractId = -1
        self.Symbol = ''
        self.Name = ''
        self.Exchange = Exchange.UnKnow
        self.PosSide = PosSide.Net
        self.Volume = -1
        self.TodayVol = -1
        self.CanCloseVol = -1
        self.ToadayEnableVol = -1
        self.AvgPx = ''
        self.HoldAvgPx = 0.0
        self.Margin = 0.0
        self.LastPx = 0.0
        self.DropIncome = 0.0
        self.DropIncomeFloat = 0.0
        self.MarketValue = 0.0

class TradeCounterEntity:
    def __init__(self):
        self.CounterId = -1
        self.CounterName = ''
        self.TradeCounter = TradeCounterType.NONE
        self.ApiList = []

class TradeApiEntity:
    def __init__(self):
        self.ApiAddr = ''
        self.ApiName = ''
        self.ApiInfoId = -1

class CompanyInfo:
    def __init__(self):
        self.CompanyId = -1
        self.IsOnLine = 0
        self.BrokerType = -1
        self.CompanyName = ''
        self.Description = ''
        self.Icon = ''
        self.Phone = ''
        self.OpenAccountAddress = ''
        self.TradeCounter = TradeCounterType.NONE

class UserInfo:
    def __init__(self):
        self.AccountID = ''
        self.BrokerType = -1
        self.PassWord = ''
        self.CounterID = -1
        self.CounterAddr = ''
        self.ApiInfoId = -1
        self.SupInfo = SuperviseInfo()
        self.TradeToken = ''

class SuperviseInfo:
    def __init__(self):
        self.TradeCounter = TradeCounterType.NONE
        self.SysInfo = ''
        self.SysInfoIntegrity = ''
        self.EncrypKeyVersion = ''
        self.ExceptionType = ''

class SendOrder:
    def __init__(self):
        self.ClientOrderID = -1
        self.Symbol = ''
        self.Exchange = Exchange.UnKnow
        self.OrderSide = OrderSide.Buy
        self.Price = 0.0
        self.Quantity = -1
        self.OrderType = OrderType.LMT
        self.OffSet = OffSet.UnKnown