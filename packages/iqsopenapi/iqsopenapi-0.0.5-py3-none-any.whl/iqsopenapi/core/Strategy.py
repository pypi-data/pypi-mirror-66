# -*- coding: utf-8 -*-

from iqsopenapi.core.events import *

class Strategy(object):
    def __init__(self, event_bus,scope, ucontext):
        self.__user_context = ucontext
        self.__event_bus = event_bus
        self.__init = scope.get('on_init', None)
        self.__handle_bar = scope.get('on_bar', None)
        self.__handle_tick = scope.get('on_tick', None)

        if self.__init is not None:
            event_bus.add_listener(EVENT.On_Init, self.init)
        if self.__handle_tick is not None:
            event_bus.add_listener(EVENT.On_Tick, self.handle_tick)
        if self.__handle_bar is not None:
            event_bus.add_listener(EVENT.On_Bar, self.handle_bar)
        
    def user_context(self):
        return self.__user_context

    def init(self):
        if self.__init:
            self.__init(self.__user_context)

    def handle_bar(self, event):
        self.__handle_bar(self.__user_context, event.data)

    def handle_tick(self, event):
        self.__handle_tick(self.__user_context, event.data)

if __name__ == '__main__':

    from iqsopenapi import *
    from iqsopenapi.core import *

    ucontext = StrategyContext()

    event_bus = EventBus()

    loader = FileStrategyLoader(r'D:\gitwork\inquantstudio\IQSOpenApi\IQS.OpenApi.Python\iqsopenapi\example\teststrategy.py')

    from copy import copy

    scope = copy(iqsopenapi.__dict__)

    loader.load(scope)

    user_strategy = Strategy(event_bus, scope, ucontext)

    user_strategy.init()    

    marketApi = MarketApi(event_bus)

    marketApi.Init()

    event_bus.start()

    ret1 = marketApi.Subscribe("rb2010.SHFE.TICK.0","rb2010.SHFE.BAR.300","rb2005.SHFE.TICK.0")

    pass