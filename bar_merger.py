from typing import List
import collections
import time
from base_classes import DataTick, DataBar


class BarMerger(object):
    def __init__(self):
        self._on_tick = None
        self._on_bar = None

        self._merge_periods = [1000, 5000, 60*1000]
        self._buffers = [collections.defaultdict(list) for _ in self._merge_periods]
        self._last_ts = int(time.time())
        pass


    def put_tick(self, tick: DataTick):
        ts = tick._timestamp

        bars_list = []
        for ibuf, (period, buf) in enumerate(zip(self._merge_periods, self._buffers)):
            ts_bar = (ts // period) * period
            ts_bar_last = (self._last_ts // period) * period

            bars = []
            # print('ts_bar:{0},ts_bar_last:{1}'.format(ts_bar, ts_bar_last))
            if  ts_bar > ts_bar_last:
                for symbol, buffered_bars in buf.items():
                    bar = self.merge_bars(ts_bar, period, buffered_bars)
                    if bar is not None:
                        buffered_bars.clear()
                        bars.append(bar)
                        if ibuf < (len(self._merge_periods) - 1):
                            self._buffers[ibuf+1][symbol].append(bar)
                            pass
                        pass
                    pass
                bars_list.append(bars)
                pass
            pass
        

        if tick._symbol is not None:
            self._buffers[0][tick._symbol].append(self.tick2bar(tick))
            pass

        # triger event
        self._on_tick(tick)

        for period, bars in zip(self._merge_periods, bars_list):
            if len(bars) > 0:
                self._on_bar(period, bars)
                pass
            pass

        self._last_ts = ts
        pass

    def tick2bar(self, tick: DataTick) -> DataBar:
        return DataBar(tick._symbol, tick._timestamp, -1, tick._price, tick._price,
                       tick._price, tick._price, tick._price, tick._volume, tick._total_volume)

    def merge_bars(self, timestamp, period, bars: List[DataBar]) -> DataBar:
        if len(bars) == 0:
            return None
        
        symbol = bars[0]._symbol
        first = bars[0]._first
        last = bars[-1]._last
        high = max(b._high for b in bars)
        low = min(b._low for b in bars)
        trade_money = sum(b._average * b._volume for b in bars)
        volume = sum(b._volume for b in bars)
        total_volume = bars[-1]._total_volume
        average = trade_money / volume if volume > 0 else first

        return DataBar(symbol, timestamp, period, first, last, high, low,
                       average, volume, total_volume)
    
    def set_on_tick(self, callback):
        self._on_tick = callback

    def set_on_bar(self, callback):
        self._on_bar = callback
