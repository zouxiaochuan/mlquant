import json
import stomp
import time
import os

import base_classes
import utils_tiger
import utils_common
import constants


assignment_keys = {'ask_size', 'ask_price', 'bid_size', 'bid_price'}


class DataFeedTiger(base_classes.DataFeedBase):
    def __init__(self, config_file):
        super().__init__()
        with open(config_file) as fin:
            utils_tiger.set_config(json.load(fin))
            pass

        self._push_client = self.connect()
        self._seq_num = 0
        self._last_volume = dict()
        self._on_tick = None
        self._symbols = None

        self._filename_bad_record = os.path.join(
            constants.data_path, 'tiger_bad_record.txt')
        pass

    def connect(self):
        while True:
            try:
                push_client = utils_tiger.get_push_client()
                push_client.disconnect_callback = self.on_disconnected
                return push_client
            except stomp.exception.ConnectFailedException:
                print('cannot connect to tiger push client')
                continue
            pass
        pass

    def on_disconnected(self):
        print('disconnect from tiger server, reconnecting...')

        self._push_client = self.connect()
        if self._symbols is not None:
            self.subscribe(self._symbols)
            self._push_client.quote_changed = self.on_quote_change
            pass
        pass

    def subscribe(self, symbols: list):
        self._symbols = symbols
        self._push_client.subscribe_quote(
            symbols,
            utils_tiger.tiger_consts.QuoteKeyType.ALL)
        pass

    def unsubscribe(self, symbols: list):
        self._push_client.unsubscribe_quote(symbols)
        self._symbols = None
        pass

    def set_on_tick(self, callback):
        self._push_client.quote_changed = self.on_quote_change
        self._on_tick = callback
        pass

    def is_future(self, symbol: str):
        return symbol.endswith('main')

    def write_bad_record(self, s: str):
        with open(self._filename_bad_record, 'a') as fout:
            fout.write(s + '\n')
            pass
        pass

    def on_quote_change(self, *args):
        symbol = args[0]
        data = args[1]

        ts = int(time.time() * 1000)
        us_datetime = utils_common.ms2datetime_us(ts)

        if self.is_future(symbol):
            if us_datetime.hour >= 17 and us_datetime.hour < 18:
                if us_datetime.minute > 1:
                    self.write_bad_record(str(ts) + '\t' + str(args))
                    return
                pass
            pass
        else:
            if us_datetime.hour >= 20 or us_datetime.hour < 4:
                if us_datetime.hour == 20 and us_datetime.minute <= 1:
                    pass
                else:
                    self.write_bad_record(str(ts) + '\t' + str(args))
                    return
                pass
            pass

        tick = base_classes.DataTick(
            symbol, -1, -1, -1, ts, self._seq_num, -1, -1, -1, -1, -1)
        self._seq_num += 1

        for desc, value in data:
            if desc == 'latest_price':
                tick._price = value
                pass
            elif desc == 'timestamp':
                tick._server_time = int(value)
                pass
            elif desc in assignment_keys:
                setattr(tick, '_' + desc, value)
                pass
            elif desc == 'volume':
                last_vol = self._last_volume.get(symbol)
                if last_vol is None:
                    # first entry, maybe middle of the day
                    tick._volume = 1
                    pass
                elif last_vol > value:
                    if value / last_vol > 0.9:
                        self.write_bad_record(str(ts) + '\t' + str(args))
                        return
                    tick._volume = value
                    pass
                else:
                    tick._volume = value - last_vol
                    pass
                tick._total_volume = value
                self._last_volume[symbol] = value
                pass
            pass

        self._on_tick(tick)
        pass
    pass
