# -*- coding: utf-8 -*- 
from iqsopenapi.marketdata.message import *

class HeartBeatReq(RequestMessage):
    """心跳请求"""

    def __init__(self):
        """请求类型"""
        self.RequestType = RequestType.HeartBeat

        
    def ToDict(self):
        return {"ReqID":self.ReqID,"RequestType":self.RequestType}
