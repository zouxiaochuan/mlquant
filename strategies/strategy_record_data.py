
import time
import base_classes
from factors import factor_last_tick


symbols = [
    'CLmain',
    'NGmain',
#     'GCmain',
    'UNG',
    'UGAZ',
    'DGAZ',
    'USO',
    'UCO',
    'SCO',
    'SPY',
    'TVIX',
    'TSLA',
    'NUGT',
    'DUST',
    'AAPL',
    'BA',
    'UPRO',
    'SPXU',
    'NVDA',
    'NTES',
    'BILI',
    'USL'
]


class StrategySimple(base_classes.StrategyBase):

    def on_tick(self, tick: base_classes.DataTick, factor_values):
        # print('{0},{1}'.format(time.time(), tick))
        pass

    def on_bar(self, period, factor_values):
        # print(factor_values)
        pass

    def depended_factors(self):
        return [
            factor_last_tick.FactorLastTick(s, (0, 0)) for s in symbols
        ]
