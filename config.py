import os
import json


class Config(object):
    def __init__(self):
        self.data_manager_class_name = 'DataManagerSQLAlchemy'
        self.data_manager_params = ['postgresql+psycopg2://stock:stock@localhost/stock']
        self.data_feed_class_name = 'DataFeedIB'
        self.data_feed_params = [10001]
        self.engine_class_name = 'EngineOnline'
        self.engine_params = ['./strategies']

        if os.path.exists('config.json'):
            with open('config.json') as fin:
                config_dict = json.load(fin)
                pass
            for k, v in config_dict.items():
                setattr(self, k, v)
                pass
            pass
        pass
    pass



