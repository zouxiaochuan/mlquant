from typing import List
import copy


class DataBase(object):

    def __str__(self):
        return str(self.__dict__)

    @classmethod
    def columns(cls):
        raise NotImplementedError()

    def data(self):
        return tuple(self.__dict__['_'+col] for col in self.columns())

    def clone(self):
        return copy.copy(self)
    pass


class DataTick(DataBase):
    @classmethod
    def columns(cls):
        return (
            'symbol', 'price', 'volume', 'total_volume', 'timestamp',
            'seq_num', 'ask_price', 'ask_size', 'bid_price', 'bid_size',
            'server_time')

    def __init__(self, symbol, price, volume, total_volume, timestamp,
                 seq_num, ask_price, ask_size, bid_price, bid_size,
                 server_time):
        self._symbol = symbol
        self._price = price
        self._volume = volume
        self._total_volume = total_volume
        self._timestamp = timestamp
        self._seq_num = seq_num
        self._ask_price = ask_price
        self._ask_size = ask_size
        self._bid_price = bid_price
        self._bid_size = bid_size
        self._server_time = server_time
        pass

    pass


class DataBar(DataBase):
    @classmethod
    def columns(cls):
        return (
            'symbol', 'timestamp', 'period', 'first', 'last', 'high', 'low',
            'average', 'volume', 'total_volume')

    def __init__(self, symbol, timestamp, period, first, last, high, low,
                 average, volume,
                 total_volume):
        self._symbol = symbol
        self._timestamp = timestamp
        self._period = period
        self._first = first
        self._last = last
        self._high = high
        self._low = low
        self._average = average
        self._volume = volume
        self._total_volume = total_volume
        pass
    pass


class DataManagerBase(object):
    def __init__(self):
        self.cached_ticks = dict()
        pass

    def init_data(self):
        raise NotImplementedError()

    def init_connection(self):
        raise NotImplementedError()

    def put_tick(self, tick: DataTick):
        raise NotImplementedError()

    def put_bars(self, bars: List[DataBar]):
        raise NotImplementedError()

    def cache_tick(self, tick: DataTick):
        self.cached_ticks[tick._symbol] = tick
        pass

    def get_last_tick(self, symbol) -> DataTick:
        return self.cached_ticks.get(symbol)

    pass


class EngineBase(object):
    def __init__(self):
        pass

    def get_data_manager(self):
        raise NotImplementedError()
    pass


class DataFeedBase(object):
    def __init__(self):
        pass

    def subscribe(self, symbols: list):
        raise NotImplementedError()

    def unsubscribe(self, symbols):
        raise NotImplementedError()

    def set_on_tick(self, callback):
        raise NotImplementedError()

    pass


class FactorBase(object):
    def __init__(self, symbol, interval):
        self._symbol = symbol
        self._interval = interval
        pass

    def extract(self, data_manager: DataManagerBase,
                symbol, current, interval, inputs):
        raise NotImplementedError()

    def parents(self):
        raise NotImplementedError()

    def is_parallel(self):
        return False

    def __hash__(self):
        return hash((self._symbol, self._interval))

    def __eq__(self, other):
        return (self._symbol, self._interval) == (other._symbol,
                                                  other._interval)
    pass


class StrategyBase(object):
    def __init__(self):
        self._symbols = set(f._symbol for f in self.depended_factors())
        pass

    def on_tick(self, tick: DataTick, factor_values):
        pass

    def on_bar(self, period, factor_values):
        pass

    def depended_factors(self) -> FactorBase:
        raise NotImplementedError()
    pass


class TradeClientBase(object):
    pass
