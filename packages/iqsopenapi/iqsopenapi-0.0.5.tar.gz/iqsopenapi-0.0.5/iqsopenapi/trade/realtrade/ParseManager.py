# -*- coding: utf-8 -*-
from iqsopenapi.models.Models import *
from iqsopenapi.enums.Enums import *
import datetime

def __ParseBaseModelCore(model, json):
    if (model == None): model = ReposeModelBase()
    model.Json = json
    model.ErrorInfo = json['error_info']
    model.ErrorNo = json['error_no']
    return model

def ParseBaseModel(json):
    if not json: return None
    return __ParseBaseModelCore(None, json)

def ParseFuturesCompanysModel(json):
    if not json: return None
    model = FuturesCompanysModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    model.ArgeementTip = json['argeementTip']
    model.ArgeementHerfText = json['argeementHerfText']
    model.ArgeementHerf = json['argeementHerf']
    model.AppQRImage = json['appQRImg']
    data = json['data']
    for item in data:
        info = CompanyInfo()
        info.CompanyId = item['companyID']
        info.BrokerType = item['brokerType']
        info.CompanyName = item['brokerName']
        info.Description = item['desc']
        info.Phone = item['phone']
        info.Icon = item['ico']
        info.IsOnLine = item['isOnline']
        info.OpenAccountAddress = item['hkUrl']
        counter = item.get('tradingCounter')
        if (counter != None): info.TradeCounter = TradeCounterType(counter)
        model.CompanyInfos.append(info)
    return model

def ParseTradeCounterModel(json):
    if not json: return None
    model = TradeCounterModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    for item in json['counterList']:
        entity = TradeCounterEntity()
        entity.CounterId = item['counterID']
        entity.CounterName = item['counterName']
        counter = item.get('tradingCounter')
        if (counter != None): entity.TradeCounter = TradeCounterType(counter)
        for api in item['apiList']:
            api_entity = TradeApiEntity()
            api_entity.ApiAddr = api['apiAddr']
            api_entity.ApiName = api['apiName']
            api_entity.ApiInfoId = api['apiInfoId']
            entity.ApiList.append(api_entity)
        model.CounterList.append(entity)
    return model

def ParseLoginResult(json):
    if not json: return None
    model = LoginResult()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    model.TradeToken = json['tradeToken']
    model.IsSigned = json['isSigned'] != 0
    return model

def ParsePositionModel(json):
    if not json: return None
    model = PositionModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    for item in json['data']:
        info = PositionInfo()
        info.ContractId = item['contractID']
        info.Symbol = item['symbol']
        info.Name = item['name']
        info.Exchange = Exchange(item['exchange'])
        info.PosSide = PosSide(item['posSide'])
        info.Volume = item['volume']
        info.TodayVol = item['todayVol']
        info.CanCloseVol = item['canCloseVol']
        info.ToadayEnableVol = item['todayEnableVol']
        info.AvgPx = item['avgPx", "']
        info.HoldAvgPx = item['holdAvgPx']
        info.Margin = item['margin']
        info.LastPx = item['lastPx']
        info.DropIncome = item['dropIncome']
        info.DropIncomeFloat = item['dropIncomeFloat']
        info.MarketValue = item['marketValue']
        model.PositionInfos.append(info)
    return model

def ParseEntrustModel(json):
    if not json: return None
    model = EntrustModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    for item in json['data']:
        info = Order()
        # 实盘接口没有返回，OrderType，FilledPx，TradeDate，FilledTime，Note，Tag所对应的字段
        info.FilledPx = 0
        info.FilledTime = datetime.datetime(1970, 1, 1)
        info.TradeDate = datetime.datetime(1970, 1, 1)
        info.Note = ''
        #info.OrderType = OrderType(item['orderType'])
        #info.StrategyID = self.__strategyID
        info.Exchange = Exchange(item['exchange'])
        info.Filled = item['filled']
        info.Offset = OffSet(item['offset'])
        info.OrderID = str(item['orderID'])
        info.OrderSide = OrderSide.__dict__[item['orderSide']]
        info.OrderTime = datetime.datetime.strptime(item['orderTime'],'%Y%m%d%H%M%S')
        info.OrderTimeStr = item['orderTimeStr']
        info.Price = item['price']
        info.Quantity = item['quantity']
        info.Status = OrderStatus(item['orderStatus'])
        info.Symbol = item['symbol']
        info.OrderStatusStr = item['orderStatusStr']
        info.ErrorMsg = item['errorMsg']
        info.LastPx = item['lastPx']
        info.CanCancel = item['canCancel']
        info.Canceled = item['canceled']
        model.EntrustInfos.append(info)
    return model

def ParseConOrderModel(json):
    if not json: return None
    model = ConOrderModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    if(not hasattr(json, 'data')): return model
    for item in json['data']:
        info = ConditionOrderEntity()
        info.ConditionId = item['conditionID']
        info.Symbol = item['symbol']
        info.ContractId = item['contractID']
        info.Status = item['status']
        info.StatusStr = item['statusStr']
        info.OrderSide = OrderSide(item['orderSide']);
        info.OrderSideStr = item['orderSideStr']
        info.OffSet = OffSet(item['offset'])
        info.OffSetStr = item['offsetStr']
        info.OrderType = OrderType(item['orderType'])
        info.OrderTypeStr = item['orderTypeStr']
        info.Price = item['price']
        info.Quantity = item['quantity']
        info.ExpireType = ConOrderTimeValidTypeEnum(item['expireType'])
        info.AddTimeStr = item['addTimeStr']
        info.ExpireTimeStr = item['expireTimeStr']
        for ckv in item['condiValues']:
            kvi = kv()
            kvi.Key = ckv['k']
            kvi.Value = ckv['v']
            info.CondiValues.append(kvi)
        info.CondiValueStr = item['condiValueStr']
        info.OrderNo = item['orderNo']
        info.OrderRet = item['orderRet']
        info.OrderNote = item['orderNote']
        info.TriggerTimeStr = item['triggerTimeStr']
        model.Data.append(info)
    return model

def ParseStopOrderNotTriggerModel(json):
    if not json: return None
    model = StopOrderNotTriggerModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    if(not hasattr(json, 'data')): return model
    for item in json['data']:
        info = StopOrderNotTrigger()
        info.StopId = item['stopID']
        info.Symbol = item['symbol']
        info.Name = item['name']
        info.PosSide = PosSide(item['posSide'])
        info.PosSideStr = item['posSideStr']
        info.StopType = item['stopType']
        info.StopTypeStr = item['stopTypeStr']
        info.TriggerPrice = item['stopPrice']
        info.OrderType = item['orderType']
        info.OrderTypeStr = item['orderTypeStr']
        info.Quantity = item['quantity']
        info.StatusStr = item['statusStr']
        model.Data.append(info)
    return model

def ParseUserAssetsModel(json):
    if not json: return None
    model = UserAssetsModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    info = AssetInfo()
    #info.StrategyID = json['accountID']
    info.TotalAsset = json['total']
    info.Available = json['available']
    #实盘没有现金余额 info.Balance
    info.Margin = json['margin']
    info.Currency = Currency(json['margin'])
    model.AssetInfo = info
    return model

def ParsePositionModel(json):
    if not json: return None
    model = PositionModel()
    ret = __ParseBaseModelCore(model, json)
    if (ret.ErrorNo != 0): return model
    if(not hasattr(json, 'data')): return model
    for item in json['data']:
        info = Position()
        info.Symbol = item['symbol']
        info.Exchange = Exchange(item['exchange'])
        #info.Quantity = item['volume']
        #实盘接口没有冻结数量 info.Frozen
        #实盘接口没有持仓成本 info.CostPx
        info.PosSide = PosSide(item['posSide'])
        info.Margin = item['margin']
        model.Data.append(info)
    return model