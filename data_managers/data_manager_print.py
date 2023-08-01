from typing import List
import time

import base_classes


class DataManagerPrint(base_classes.DataManagerBase):
    def init(self):
        pass

    def put_tick(self, tick: base_classes.DataTick):
        print('{0},{1}'.format(time.time(), tick))

    def put_bars(self, bars: List[base_classes.DataBar]):
        for bar in bars:
            print(bar)
            pass
        pass
    pass
