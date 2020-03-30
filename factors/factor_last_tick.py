import base_classes
import numpy as np

class FactorLastTick(base_classes.FactorBase):
    def __init__(self, symbol, interval):
        super().__init__(symbol, interval)
        self._interval = (0, 0)
        pass

    def parents(self):
        return []


    def extract(self, data_manager: base_classes.DataManagerBase,
                symbol, current, interval, inputs):
        tick = data_manager.get_last_tick(symbol)

        value = np.zeros(8)
        if tick is not None:
            value[0] = tick._price
            value[1] = tick._volume
            value[2] = tick._total_volume
            value[3] = tick._timestamp / 1000
            value[4] = tick._ask_price
            value[5] = tick._ask_size
            value[6] = tick._bid_price
            value[7] = tick._bid_size
            pass

        return value
    pass
