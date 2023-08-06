# -*- coding: utf-8 -*-
from iqsopenapi.basicdata  import *
from iqsopenapi.core  import *
from iqsopenapi.marketdata  import *
from iqsopenapi.models  import *
from iqsopenapi.trade  import *
from iqsopenapi.util  import *

def run_file(strategy_file_path, config=None):
    """执行文件"""

    loader = FileStrategyLoader(strategy_file_path)
    return __run(config,loader)

def run_code(source_code, config=None):
    """执行源代码"""

    loader = SourceCodeStrategyLoader(source_code)
    return __run(config,loader)


def run_func(**kwargs):
    """执行自定义函数"""

    config = kwargs.get('config', kwargs.get('__config__', None))
    user_funcs = {
        k: kwargs[k]
        for k in ['init', 'handle_bar', 'handle_tick', 'open_auction', 'before_trading', 'after_trading']
        if k in kwargs
    }

    loader = UserFuncStrategyLoader(user_funcs)
    return __run(config,loader)

def __run(config, strategy_loader):
    try:

        environment = Environment(config)

        ucontext = StrategyContext()

        event_bus = EventBus()

        from copy import copy

        scope = copy(iqsopenapi.__dict__)

        strategy_loader.load(scope)

        user_strategy = Strategy(event_bus, scope, ucontext)

        user_strategy.init()    

        marketApi = MarketApi(event_bus)

        marketApi.Init()

        ret1 = marketApi.Subscribe("rb2010.SHFE.TICK.0","rb2010.SHFE.BAR.300","rb2005.SHFE.TICK.0")

        event_bus.start()

    except Exception as e:
        logger.error(e)

