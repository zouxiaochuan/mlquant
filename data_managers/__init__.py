import sys


from data_manager_noop import DataManagerNoop
from data_manager_sqlalchemy import DataManagerSQLAlchemy
from data_manager_print import DataManagerPrint
from data_manager_sqlite_online import DataManagerSQLiteOnline


self_module = sys.modules[__name__]

def register_class(cls):
    self_module.__dict__[cls.__name__] = cls
    pass


