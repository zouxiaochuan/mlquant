

from engines import engine_online
from data_feeds import data_feed_tiger, data_feed_ib
from data_managers import data_manager_sqlite_online


if __name__ == '__main__':
    # datafeed = data_feed_tiger.DataFeedTiger('./tiger.json')
    datafeed = data_feed_ib.DataFeedIB(100)
    data_manager = data_manager_sqlite_online.DataManagerSqliteOnline('./data')
    engine = engine_online.EngineOnline(
        datafeed, data_manager, ['./strategies'])

    engine.start()

    pass
