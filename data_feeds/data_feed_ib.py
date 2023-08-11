from base_classes import DataFeedBase
import utils_ib
import threading
import time


class DataFeedIB(DataFeedBase):
    def __init__(self, client_id: int, ip='127.0.0.1', port=4001):
        super().__init__()
        self.client = utils_ib.IBClient()

        self.client_id = client_id
        self.ip = ip
        self.port = port

        self.loop_thread = threading.Thread(
            target=self.run_client,
            args=())
        self.loop_thread.start()

        while not self.client.isConnected():
            time.sleep(0.1)
            pass
        pass

    def run_client(self,):
        while True:
            self.client.connect(self.ip, self.port, self.client_id)
            self.client.run()

            self.client.disconnect()
            time.sleep(1)
            pass
        pass
    
    def subscribe(self, symbols: list):
        self.client.subscribe(symbols)
        pass

    def unsubscribe(self, symbols: list):
        self.client.unsubscribe(symbols)
        pass

    def set_on_tick(self, callback):
        self.client.set_on_tick(callback)
        pass


    
