import json
from collections import defaultdict

import base_classes
import utils_tiger


assignment_keys = {'ask_size', 'ask_price', 'bid_size', 'bid_price'}

class DataFeedTiger(base_classes.DataFeedBase):
    def __init__(self, config_file):
        super().__init__()
        with open(config_file) as fin:
            utils_tiger.set_config(json.load(fin))
            pass

        self._push_client = utils_tiger.get_push_client()
        self._day_order = defaultdict(int)
        self._last_volume = defaultdict(int)
        pass


    def subscribe(self, symbols: list):
        self._push_client.subscribe_quote(
            symbols,
            utils_tiger.tiger_consts.QuoteKeyType.ALL)
        pass

    def unsubscribe(self, symbols: list):
        self._push_client.unsubscribe_quote(symbols)
        pass


    def set_on_tick(self, callback):
        self._push_client.quote_changed = self.on_quote_change
        self._on_tick = callback
        pass


    def on_quote_change(self, *args):
        symbol = args[0]
        data = args[1]
        is_prepost = args[2]

        day_order = self._day_order[symbol]
        self._day_order[symbol] += 1

        tick = base_classes.DataTick(symbol, -1, -1, -1, -1, day_order, -1, -1, -1, -1)
        
        for desc, value in data:            
            if desc == 'latest_price':
                tick._price = value
                pass
            elif desc == 'timestamp':
                tick._timestamp = int(value)
                pass
            elif desc in assignment_keys:
                setattr(tick, '_' + desc, value)
                pass
            elif desc == 'volume':
                last_vol = self._last_volume[symbol]
                if last_vol == 0:
                    # first entry, maybe middle of the day
                    tick._volume = value - last_vol                    
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
