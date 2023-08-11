from typing import List
import collections
import time
from base_classes import DataTick, DataBar


class BarMerger(object):
    def __init__(self):
        self._on_tick = None
        self._on_bar = None

        self._merge_periods = [1000, 5000, 60*1000]
        self._buffers = [collections.defaultdict(list) for _ in
                         self._merge_periods]
        self._last_ts = int(time.time() * 1000)
        pass

    def put_tick(self, tick: DataTick):
        ts = tick.timestamp
        last_ts = self._last_ts

        bars_list = []
        for ibuf, (period, buf) in enumerate(
                zip(self._merge_periods, self._buffers)):
            ts_bar_current = (ts // period) * period
            ts_bar = (last_ts // period + 1) * period

            if ts_bar_current >= ts_bar:
                bars = []
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
                if len(bars) > 0:
                    bars_list.append((period, bars))
                    pass
                pass
            pass

        if tick.symbol is not None:
            if tick.volume > 0:
                self._buffers[0][tick.symbol].append(self.tick2bar(tick))
                pass

            # triger event
            self._on_tick(tick)
            pass

        for period, bars in bars_list:
            self._on_bar(period, bars)
            pass

        self._last_ts = ts
        pass

    def tick2bar(self, tick: DataTick) -> DataBar:
        return DataBar(tick.symbol, tick.timestamp, -1, tick.price,
                       tick.price, tick.price, tick.price, tick.price,
                       tick.volume, tick.total_volume)

    def merge_bars(self, timestamp, period, bars: List[DataBar]) -> DataBar:
        if len(bars) == 0:
            return None

        # print([b.__dict__ for b in bars])
        symbol = bars[0].symbol
        first = bars[0].first
        last = bars[-1].last
        high = max(b.high for b in bars)
        low = min(b.low for b in bars)
        trade_money = sum(b.average * b.volume for b in bars)
        volume = sum(b.volume for b in bars)
        total_volume = bars[-1].total_volume
        average = trade_money / volume if volume > 0 else first

        return DataBar(symbol, timestamp, period, first, last, high, low,
                       average, volume, total_volume)

    def set_on_tick(self, callback):
        self._on_tick = callback

    def set_on_bar(self, callback):
        self._on_bar = callback
