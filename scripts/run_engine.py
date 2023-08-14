
import context

from engines import engine_online
from data_feeds import data_feed_tiger, data_feed_ib
from data_managers import data_manager_sqlite_online, data_manager_print, data_manager_sqlalchemy


if __name__ == '__main__':
    context.init()
    datafeed = context.create_data_feed()
    data_manager = context.create_data_manager()
    engine = context.create_engine(datafeed, data_manager)

    engine.start()

    pass
