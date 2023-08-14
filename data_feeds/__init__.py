import sys


from .data_feed_ib import DataFeedIB
from .data_feed_tiger import DataFeedTiger


self_module = sys.modules[__name__]

def register_class(cls):
    self_module.__dict__[cls.__name__] = cls
    pass


