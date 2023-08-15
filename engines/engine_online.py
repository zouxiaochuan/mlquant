import os
import importlib
import sys
import queue
import threading
import atexit
from typing import List
import time
import datetime
import logging

import base_classes
import utils_common
import bar_merger
import factor_manager

engine_instance = None

logger = logging.getLogger('mlquant')

def unsubscribe_on_exit():
    engine_instance.unsubscribe()
    pass


def on_tick(tick: base_classes.DataTick):
    # print('come here')
    engine_instance.on_datafeed_tick(tick)
    pass


class EngineOnline(base_classes.EngineBase):
    def __init__(self,
                 data_feed: base_classes.DataFeedBase,
                 data_manager: base_classes.DataFeedBase,
                 path_strategies: list):
        global engine_instance
        if engine_instance is not None:
            raise RuntimeError('EngineOnline should be instantiated once')

        self._data_feed = data_feed
        self._data_manager = data_manager
        self._path_strategies = path_strategies
        self._bar_merger = bar_merger.BarMerger()
        self._bar_merger.set_on_tick(self.on_bar_tick)
        self._bar_merger.set_on_bar(self.on_bar)
        self._queue_datafeed = queue.Queue()
        self._factor_manager = factor_manager.FactorManager()
        self._last_tick_ts = int(time.time() * 1000)
        self._mutex = threading.Lock()

        # load strategies
        self._strategies = self.load_strategies(self._path_strategies)

        # load factors
        self._factor_manager.load_factors(self._strategies)
        self._symbols = list(self._factor_manager.get_symbols())

        engine_instance = self
        pass

    def load_strategies(self, pathes: list):
        logger.info(f'load strategies from {pathes}')
        strategies = list()

        for path in pathes:
            for cls in utils_common.import_path_and_get_classes(path):
                if issubclass(cls, base_classes.StrategyBase):
                    strategies.append(cls())
                    pass
                pass
            pass
        return strategies

    def start(self):
        self._data_feed.set_on_tick(on_tick)
        self._data_feed.subscribe(self._symbols)
        atexit.register(unsubscribe_on_exit)

        threading.Thread(
            target=generate_tick_second,
            args=(self,)).start()

        while True:
            tick = self._queue_datafeed.get()
            self._bar_merger.put_tick(tick)
            pass
        pass

    def unsubscribe(self):
        self._data_feed.unsubscribe(self._symbols)
        pass

    def on_datafeed_tick(self, tick: base_classes.DataTick):
        self._queue_datafeed.put(tick)

        with self._mutex:
            self._last_tick_ts = tick.timestamp
            pass
        pass

    def on_bar_tick(self, tick: base_classes.DataTick):
        # print('{0},{1}'.format(
        #     datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f'), tick))
        # print('queue size: {0}'.format(self._queue_datafeed.qsize()))
        
        self._data_manager.put_tick(tick)
        self._data_manager.cache_tick(tick)

        for i, strategy in enumerate(self._strategies):
            if tick.symbol in strategy._symbols:
                strategy.on_tick(
                    tick, self._factor_manager.get_strategy_factor_values(i))
                pass
            pass
        pass

    def on_bar(self, period: int, bars: List[base_classes.DataBar]):
        # for bar in bars:
        #     print('{0},{1},{2}'.format(
        #         time.time(), self._queue_datafeed.qsize(), str(bar)))
        #     pass

        self._data_manager.put_bars(bars)

        if period == 1:
            # update factors every seconds
            self._factor_manager.update_factor_values()
            pass

        for i, strategy in enumerate(self._strategies):
            strategy.on_bar(
                period, self._factor_manager.get_strategy_factor_values(i))
            pass
        pass
    pass


def generate_tick_second(engine: EngineOnline):
    while True:
        ts = int(time.time() * 1000)
        # tick = base_classes.DataTick(
        #     None, None, None, None, ts, None, None, None, None, None, None)
        tick = base_classes.DataTick.create_empty(None)
        tick.timestamp = ts
        engine._queue_datafeed.put(tick)
        time.sleep((1000 - ts % 1000 + 100)/1000)
        pass
    pass
