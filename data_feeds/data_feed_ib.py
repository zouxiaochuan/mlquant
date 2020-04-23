from base_classes import DataFeedBase
import utils_ib


class DataFeedIB(DataFeedBase):
    def __init__(self, client_id: int, ip='127.0.0.1', port=4001):
        super().__init__()
        self._client = utils_ib.connect_client(client_id, ip, port)
        pass

    def subscribe(self, symbols: list):
        self._client.subscribe(symbols)
        pass

    def unsubscribe(self, symbols: list):
        self._client.unsubscribe(symbols)
        pass

    def set_on_tick(self, callback):
        self._client.set_on_tick(callback)
        pass


    
