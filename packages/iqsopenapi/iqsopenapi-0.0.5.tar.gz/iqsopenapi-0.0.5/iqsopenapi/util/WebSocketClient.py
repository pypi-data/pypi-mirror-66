# -*- coding: utf-8 -*-
from iqsopenapi.util import *
from websocket import *
from queue import Queue
import datetime
import threading
import time
import json
import ssl

class websocketCfg(object):
    """websocket配置信息"""

    def __init__(self):
        """地址"""
        self.address = ""

        """心跳间隔"""
        self.hbInternal = 5

        """超时"""
        self.keepAliveTimeout = 30

        """心跳内容"""
        self.hbContent = None

        """收到数据回调"""
        self.recvCallback = None

class WebSocketClient(object):
    """WebSocket"""

    def __init__(self,cfg):
        """构造函数"""

        #连接地址
        self.config = cfg
        #websocket
        self.__wsclinet = None
        #上次活跃时间
        self.__lastActiveTime = datetime.datetime.now()
        #缓存队列
        self.__unhandledQueue = Queue()
        t = threading.Thread(target=self.__TimerHandleMsg)
        t.start()
    
    def Connect(self):
        """连接"""
        if self.__IsAvaliable(self.__wsclinet):
            return True
        logger.debug("begin connect:{0}".format(self.config.address))
        self.__wsclinet = create_connection(self.config.address,  sslopt={"cert_reqs": ssl.CERT_NONE})
        logger.debug("conenect succeed:{0},state:{1}".format(self.config.address,self.__wsclinet.connected))
        self.__lastActiveTime = datetime.datetime.now()
        t = threading.Thread(target=self.__TimerReceiveMsg)
        t.start()
        t1 = threading.Thread(target=self.__TimerAutoHeartBeat)
        t1.start()
        return True

    def IsConnected(self):
        """判断是否连接"""
        if not self.__wsclinet:
            return False
        return self.__wsclinet.connected

    def __IsAvaliable(self,client):
        """判断是否是有效连接"""
        if not client:
            return False
        return client.connected

    def Send(self,content):
        """发送消息"""
        if not content:
            return None
        if not self.__IsAvaliable(self.__wsclinet):
            return None
        data = bytes(content, encoding = "utf8") 
        return self.__wsclinet.send(data)
 
    def __TimerReceiveMsg(self):
        """接收消息"""
        while True:
            try:
                 if not self.__IsAvaliable(self.__wsclinet):
                     time.sleep(1)
                     continue
                 result = self.__wsclinet.recv()
                 self.__lastActiveTime = datetime.datetime.now()
                 self.__unhandledQueue.put(result)
            except Exception as e:
                logger.error(e)
                self.__Close()
                time.sleep(1)

    def __TimerHandleMsg(self):
        """处理消息"""
        while True:
            try:
                msg = self.__unhandledQueue.get()
                if not msg:
                    time.sleep(1)
                    continue
                self.__RaiseMessage(msg)
            except Exception as e:
                logger.error(e)
                time.sleep(1)
    
    def __TimerAutoHeartBeat(self):
        """心跳"""
        if not self.config.hbContent:
            logger.warn("heart beat content is None, skip heart beat:{0}".format(self.config.address))
            return
        logger.debug("start heart beat:{0}...".format(self.config.address))
        while True:
            time.sleep(self.config.hbInternal)
            try:
                if not self.__IsAvaliable(self.__wsclinet):
                    logger.error("session disconnected on heart beat:{0}".format(self.config.address))
                    continue
                if(datetime.datetime.now() - self.__lastActiveTime).seconds > self.config.keepAliveTimeout:
                    self.__Close()
                    logger.error("heart beat timeout, disconnect session:{0}".format(self.config.address))
                    continue
                self.Send(self.config.hbContent)
                logger.debug("send heart beat:{0}".format(self.config.address))
            except Exception as e:
                logger.error(e)
                self.__Close()

    def __RaiseMessage(self,msg):
        if not msg:
            return
        logger.debug("receive message:{0},{1}".format(msg,self.config.address))
        data = json.loads(msg,encoding='utf-8')
        self.config.recvCallback(data)
    
    def __Close(self):
        if self.__wsclinet:
            self.__wsclinet.close()
        self.__wsclinet = None
        
if __name__ == '__main__':
    cfg = websocketCfg()
    cfg.address = "wss://dev_quotegateway.inquantstudio.com"
    cfg.hbContent = json.dumps({ 'requestType' : 'HeartBeat','reqID' : '' })
    cfg.recvCallback = lambda msg:logger.info(msg)

    ws = WebSocketClient(cfg)
    ws.Connect()
