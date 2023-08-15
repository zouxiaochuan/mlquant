import logging
import sys
from config import Config
from base_classes import DataManagerBase, DataFeedBase, EngineBase
import data_managers
import data_feeds
import engines


config: Config = None
logger: logging.Logger = None


def init_logger():
    global logger

    logger = logging.getLogger('mlquant')

    if len(logger.handlers) > 0:
        return
    
    ch = logging.StreamHandler(sys.stdout)
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    logger.setLevel(logging.INFO)
    # logger.info('-----------------------comehere')
    pass

def init():
    global config
    config = Config()

    init_logger()
    pass


def create_data_manager() -> DataManagerBase:
    data_manager_class_name = config.data_manager_class_name
    data_manager_params = config.data_manager_params
    data_manager_class = getattr(data_managers, data_manager_class_name)
    data_manager = data_manager_class(*data_manager_params)
    return data_manager


def create_data_feed() -> DataFeedBase:
    data_feed_class_name = config.data_feed_class_name
    data_feed_params = config.data_feed_params
    data_feed_class = getattr(data_feeds, data_feed_class_name)
    data_feed = data_feed_class(*data_feed_params)
    return data_feed

def create_engine(data_feed, data_manager) -> EngineBase:
    engine_class_name = config.engine_class_name
    engine_params = config.engine_params
    engine_class = getattr(engines, engine_class_name)
    engine = engine_class(data_feed, data_manager, *engine_params)
    return engine
