import threading
import time
from collections import defaultdict
from queue import Queue
from typing import List, Dict, Tuple

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import TickAttrib
from ibapi.contract import Contract, ContractDetails
from ibapi.utils import iswrapper
from ibapi.ticktype import TickTypeEnum

from base_classes import DataTick

map_tick_type = {
    TickTypeEnum.BID_SIZE: '_bid_size',
    TickTypeEnum.BID: '_bid_price',
    TickTypeEnum.ASK_SIZE: '_ask_size',
    TickTypeEnum.ASK: '_ask_price',
    TickTypeEnum.LAST: '_price',
    TickTypeEnum.VOLUME: '_total_volume',
    TickTypeEnum.LAST_SIZE: '_volume',
    TickTypeEnum.LAST_TIMESTAMP: '_server_time'
    }

needed_tick_type = set(map_tick_type.keys())

triger_tick_type = {
    # TickTypeEnum.BID_SIZE,
    # TickTypeEnum.BID,
    # TickTypeEnum.ASK_SIZE,
    # TickTypeEnum.ASK,
    TickTypeEnum.VOLUME
    }


class IBWrapper(EWrapper):
    def __init__(self):
        super().__init__()
        self._tick_buffer: Dict[int, DataTick] = dict()
        self._last_tick: Dict[int, DataTick] = dict()
        self._req_id = 10000
        self._sync_queues = defaultdict(Queue)
        self._on_tick = None
        self._queue_msg_req_id = Queue()
        self._queue_msg_data: Dict[int, Tuple] = dict()
        self._seq_num = 0
        
        pass

    @iswrapper
    def tickPrice(
            self, reqId: int ,
            tickType: int,
            price: float,
            attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)

        # print('tickPrice: {0}'.format(TickTypeEnum.to_str(tickType)))

        if tickType in needed_tick_type:
            self.put_msg_queue(reqId, tickType, price)
            pass
        pass
    
    @iswrapper
    def tickSize(
            self, reqId,
            tickType: int,
            size: int):
        super().tickSize(reqId, tickType, size)

        # print('tickSize: {0}'.format(TickTypeEnum.to_str(tickType)))        
        if tickType in needed_tick_type:
            self.put_msg_queue(reqId, tickType, size)
            pass
        pass
    
    @iswrapper
    def tickString(
            self, reqId: int, tickType: int, value: str):
        super().tickString(reqId, tickType, value)

        if tickType == TickTypeEnum.LAST_TIMESTAMP:
            v = int(value) * 1000
            self.put_msg_queue(reqId, tickType, v)
            pass
        pass

    def put_msg_queue(self, req_id, tick_type, value):
        q = self._queue_msg_data.get(req_id)
        if q is not None:
            q.put((time.time(), tick_type, value))
            self._queue_msg_req_id.put(req_id)
            # print(q.qsize())
            # print(self._thread.is_alive())
            pass
        pass

    @iswrapper
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)

        # print(contractDetails.__dict__)
        que = self._sync_queues.get(reqId)

        if que is not None:
            que.put(contractDetails)
            pass
        pass
        
    def set_on_tick(self, callback):
        print('set on tick called')
        self._on_tick = callback
        pass

    def add_subscribe(self, symbol):
        tick = DataTick(symbol, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1)
        req_id = self.get_req_id()
        self._tick_buffer[req_id] = tick
        self._queue_msg_data[req_id] = Queue()
        return req_id

    def remove_subscribe(self, symbol):
        rm_req_id = None
        for req_id, tick in self._tick_buffer.items():
            if tick._symbol == symbol:
                rm_req_id = req_id
                break
            pass

        if rm_req_id is not None:
            self._tick_buffer.pop(rm_req_id)
            self._queue_msg_data.pop(req_id)
            if rm_req_id in self._last_tick:
                self._last_tick.pop(rm_req_id)
                pass
            pass
        
        return rm_req_id

    def subscribe_size(self):
        return len(self._tick_buffer)

    def reset_queue(self, req_id):
        self._sync_queues[req_id].queue.clear()
        pass

    def clear_queue(self, req_id):
        self._sync_queues.pop(req_id)
        pass

    def get_queue_result(self, req_id):
        que  = self._sync_queues.get(req_id)
        if que is None:
            raise RuntimeError('queue not exist: {0}'.format(req_id))

        return que.get()
        pass

    def get_req_id(self):
        self._req_id += 1
        return self._req_id

    def on_tick_pre(self, req_id: int, tick_type: int):
        tick = self._tick_buffer[req_id]
        last_tick = self._last_tick.get(req_id)
        
        if last_tick is None:
            pass
        else:
            tick._volume = tick._total_volume - last_tick._total_volume
            pass

        tick._seq_num = self._seq_num
        self._seq_num += 1
        tick = tick.clone()
        # print(str(tick))
        if tick._price > 0 and tick._ask_price > 0 and tick._ask_size > 0 and \
           tick._bid_price > 0 and tick._bid_size > 0 and \
           last_tick is not None and last_tick._total_volume > 0:
            self._on_tick(tick)
            pass
        self._last_tick[req_id] = tick
        pass

    
class IBClient(EClient):
    def __init__(self, wrapper):
        super().__init__(wrapper)
        self._is_close = False
        
        pass

    def close(self):
        self._is_close = True
    
        self.disconnect()
        pass

    def run(self):
        self._thread_msg_queue = threading.Thread(
            target=process_msg_queue, args=(self,))
        self._thread_msg_queue.start()

        super().run()

        print('wait for thread message queue to end...')
        self.wrapper._queue_msg_req_id.put(None)
        self._thread_msg_queue.join()
        print('thread message queue ended')
        
        pass
    
    def set_on_tick(self, callback):
        self.wrapper.set_on_tick(callback)
        pass

    def reqContractDetailsSync(self, req_id, contract) -> ContractDetails:
        # print('{0},{1}'.format(req_id, contract.__dict__))
        return self.sync_call(self.reqContractDetails, req_id, contract)

    def sync_call(self, func, req_id, *params):
        self.wrapper.reset_queue(req_id)
        func(req_id, *params)
        res = self.wrapper.get_queue_result(req_id)
        self.wrapper.clear_queue(req_id)
        return res
    
    def subscribe(self, symbols: list):
        for symbol in symbols:
            contract = self.symbol2contract(symbol)
            req_id = self.wrapper.add_subscribe(symbol)
            # print('{0},{1}'.format(req_id, contract.__dict__))
            self.reqMktData(req_id, contract, '', False, False, [])
            pass
        pass

    def unsubscribe(self, symbols: list):
        for symbol in symbols:
            req_id = self.wrapper.remove_subscribe(symbol)
            if req_id is not None:
                self.cancelMktData(req_id)
                pass
            pass
        pass

    def subscribed_symbols(self):
        return [tick._symbol for _, tick in self.wrapper._tick_buffer.items()]
    
    def symbol2contract(self, symbol: str):
        if self.is_future(symbol):
            contract = Contract()
            contract.symbol = symbol[:2]
            contract.currency = 'USD'
            contract.secType = 'CONTFUT'

            contractDetail = self.reqContractDetailsSync(
                self.wrapper.get_req_id(), contract)
            contract.secType = 'FUT'
            contract.exchange = contractDetail.contract.exchange
            contract.lastTradeDateOrContractMonth = \
                contractDetail.contractMonth
            contract.localSymbol = contractDetail.contract.localSymbol
            return contract
        else:
            contract = Contract()
            contract.symbol = symbol
            contract.currency = 'USD'
            contract.secType = 'STK'
            contract.exchange = 'SMART'

            return contract
        pass
    
    def is_future(self, symbol: str):
        if symbol.endswith('main'):
            return True

        return False
    pass


def check_price_in_queue(ts, q):
    for its, itype, ivalue in q.queue:
        if its - ts >= 0.002:
            break
        else:
            if itype == TickTypeEnum.LAST:
                return ivalue
            pass
        pass

    return None


def process_msg_queue(client: IBClient):
    wrapper = client.wrapper
    
    while client.isConnected():
        req_id = wrapper._queue_msg_req_id.get()
        if req_id is None:
            break
        
        q = wrapper._queue_msg_data.get(req_id)
        if q is None:
            raise RuntimeError('message data queue not exists: {0}'.format(
                req_id))
        
        ts, tick_type, value = q.get()

        # print(TickTypeEnum.to_str(tick_type))
        tick = wrapper._tick_buffer.get(req_id)
        
        if tick is not None:
            attr = map_tick_type.get(tick_type)
            
            if attr is not None:
                last_val = getattr(tick, attr)
                if last_val == value:
                    continue
                
                setattr(tick, attr, value)

                # check if triger tick event
                if tick_type in triger_tick_type:
                    timestamp = time.time()
                    if tick_type == TickTypeEnum.VOLUME:
                        ts_diff = timestamp - ts
                        if ts_diff < 0.002:
                            # time.sleep(0.002 - ts_diff)
                            pass

                        cprice = check_price_in_queue(ts, q)
                        if cprice is not None:
                            tick._price = cprice
                            pass
                        pass

                    tick._timestamp = int(ts * 1000)
                    wrapper.on_tick_pre(req_id, tick_type)
                    pass
                pass
            pass
        pass
    pass


def message_loop_func(client: IBClient, client_id, ip, port):
    symbols = None
    
    while True:
        client.reset()
        client.connect(ip, port, client_id)

        if client.isConnected():
            if symbols is not None:
                threading.Thread(
                    target=client.subscribe, args=(symbols,)).start()
                # client.subscribe(symbols)
                pass

            client.run()
            
            symbols = client.subscribed_symbols()
            client.unsubscribe(symbols)
            pass
        
        if client._is_close:
            break
        
        time.sleep(1)
        print('reconnecting to ib client')
        pass
    pass


def connect_client(client_id: int,
                   ip: str = '127.0.0.1',
                   port: int = 4001) -> IBClient:
    wrapper = IBWrapper()
    client = IBClient(wrapper)
    threading.Thread(target=message_loop_func,
                     args=(client, client_id, ip, port)).start()
    while not client.isConnected():
        time.sleep(1)
        pass
    
    return client


if __name__ == '__main__':
    client = connect_client(0)
    contract = client.symbol2contract('NGmain')
    print(contract.__dict__)
    client.close()
    pass
