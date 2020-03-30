

import unittest
import multiprocessing as mp
import time

from engines import engine_online
from data_feeds import data_feed_tiger
from data_managers import data_manager_noop


if __name__ == '__main__':
    datafeed = data_feed_tiger.DataFeedTiger('./tiger.json')
    data_manager = data_manager_noop.DataManagerNoop()
    engine = engine_online.EngineOnline(
        datafeed, data_manager, ['./strategies'])

    engine.start()

    pass
