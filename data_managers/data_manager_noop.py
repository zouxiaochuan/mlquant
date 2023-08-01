from typing import List

import base_classes

class DataManagerNoop(base_classes.DataManagerBase):
    def init(self):
        pass

    def put_tick(self, tick: base_classes.DataTick):
        pass

    def put_bars(self, bars: List[base_classes.DataBar]):
        pass
    pass
