
import sys

from engine_online import EngineOnline


self_module = sys.modules[__name__]


def register_class(cls):
    self_module.__dict__[cls.__name__] = cls
    pass

