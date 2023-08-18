import threading
import time
from collections import defaultdict
from queue import Queue
from typing import List, Dict, Tuple
import logging
import random

from ibapi.client import EClient
from ibapi.wrapper import EWrapper
from ibapi.common import TickAttrib
from ibapi.contract import Contract, ContractDetails
from ibapi.utils import iswrapper
from ibapi.ticktype import TickTypeEnum

from base_classes import DataTick

logger = logging.getLogger('mlquant')

map_tick_type = {
    TickTypeEnum.BID_SIZE: 'bid_size',
    TickTypeEnum.BID: 'bid_price',
    TickTypeEnum.ASK_SIZE: 'ask_size',
    TickTypeEnum.ASK: 'ask_price',
    TickTypeEnum.LAST: 'price',
    TickTypeEnum.VOLUME: 'total_volume',
    TickTypeEnum.LAST_SIZE: 'volume',
    TickTypeEnum.LAST_TIMESTAMP: 'server_time'
    }

needed_tick_type = set(map_tick_type.keys())

triger_tick_type = {
    # TickTypeEnum.BID_SIZE,
    # TickTypeEnum.BID,
    # TickTypeEnum.ASK_SIZE,
    # TickTypeEnum.ASK,
    TickTypeEnum.VOLUME
    }


def check_volume_valid(last_volume, volume):
    if last_volume is None:
        return True
    
    if volume / last_volume > 5:
        return False
    
    # if volume < last_volume:
    #     return False
    
    return True


class IBWrapper(EWrapper):
    def __init__(self, client: EClient):
        super().__init__()
        self.tick_buffer: Dict[int, DataTick] = dict()
        self.req_id = 10000
        self.sync_queues = defaultdict(Queue)
        self.on_tick = None
        self.queue_msg_req_id = Queue()
        self.queue_msg_data: Dict[int, Tuple] = dict()
        self.seq_num = 0
        self.connect_event = threading.Event()
        self.client = client
        pass

    @iswrapper
    def tickPrice(
            self, reqId: int ,
            tickType: int,
            price: float,
            attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)

        tick_buf = self.tick_buffer.get(reqId)
        if tick_buf is None:
            raise RuntimeError('tick buffer is None')
        
        attribute = map_tick_type.get(tickType)
        if attribute is not None:
            setattr(tick_buf, attribute, price)
            pass
        pass
    
    @iswrapper
    def tickSize(
            self, reqId,
            tickType: int,
            size: int):
        super().tickSize(reqId, tickType, size)
       
        if tickType == TickTypeEnum.VOLUME:
            tick_data = self.tick_buffer.get(reqId)

            size = size * 100
            current_ts = int(time.time()*1000)
            
            if not check_volume_valid(tick_data.total_volume, size):
                logger.warning(
                    f'volume is not valid, symbol: {tick_data.symbol} last: {tick_data.total_volume}, current: {size}')
                return

            if tick_data.total_volume is None:
                tick_data.total_volume = size
                pass
            elif tick_data.total_volume > size:
                # volume reset
                logger.warning(f'volume reset, symbol: {tick_data.symbol}, old: {tick_data.total_volume}, new: {size}')
                tick_data.total_volume = size
                pass
            else:
                if size > tick_data.total_volume:
                    if current_ts > tick_data.timestamp:
                        # we should emit tick data
                        tick_data.volume = size - tick_data.total_volume
                        tick_data.total_volume = size
        
                        if self.on_tick is not None and tick_data.price is not None:
                            tick_data.timestamp = current_ts
                            self.on_tick(tick_data)
                            pass
                        pass
                    pass
                pass
            tick_data.timestamp = current_ts
            pass
        pass
    
    @iswrapper
    def tickString(
            self, reqId: int, tickType: int, value: str):
        super().tickString(reqId, tickType, value)

        pass


    @iswrapper
    def contractDetails(self, reqId: int, contractDetails: ContractDetails):
        super().contractDetails(reqId, contractDetails)

        # print(contractDetails.__dict__)
        que = self.sync_queues.get(reqId)

        if que is not None:
            que.put(contractDetails)
            pass
        pass

    @iswrapper
    def connectAck(self):
        super().connectAck()
        self.connect_event.set()

        for req_id, tick in self.tick_buffer.items():
            logger.info(f'reconnect subscribe: {tick.symbol}')
            contract = self.client.symbol2contract(tick.symbol)
            self.client.reqMktData(req_id, contract, '', False, False, [])
            tick.total_volume = None
            tick.price = None
            tick.timestamp = None
            pass
        pass
        
    def set_on_tick(self, callback):
        self.on_tick = callback
        pass

    def add_subscribe(self, symbol):
        tick = DataTick.create_empty(symbol)
        req_id = self.get_req_id()
        self.tick_buffer[req_id] = tick
        return req_id

    def remove_subscribe(self, symbol):
        rm_req_id = None
        for req_id, tick in self.tick_buffer.items():
            if tick.symbol == symbol:
                rm_req_id = req_id
                break
            pass

        if rm_req_id is not None:
            self.tick_buffer.pop(rm_req_id)
            pass
        
        return rm_req_id

    def subscribe_size(self):
        return len(self._tick_buffer)

    def reset_queue(self, req_id):
        self.sync_queues[req_id].queue.clear()
        pass

    def clear_queue(self, req_id):
        self.sync_queues.pop(req_id)
        pass

    def get_queue_result(self, req_id):
        que  = self.sync_queues.get(req_id)
        if que is None:
            raise RuntimeError('queue not exist: {0}'.format(req_id))

        return que.get()
        pass

    def get_req_id(self):
        self.req_id += 1
        return self.req_id
        pass

    
class IBClient(EClient):

    def __init__(self, ):
        wrapper = IBWrapper(self)
        super().__init__(wrapper)
        self.is_close = True
        
        pass

    def close(self):
        self.is_close = True
    
        self.disconnect()
        pass

    def run(self, ):
        super().run()
        pass
    
    def set_on_tick(self, callback):
        self.wrapper.set_on_tick(callback)
        pass

    def reqContractDetailsSync(self, contract) -> ContractDetails:
        req_id = self.wrapper.get_req_id()
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

    def get_subscribed_symbols(self):
        return [tick.symbol for _, tick in self.wrapper.tick_buffer.items()]
    
    def symbol2contract(self, symbol: str):
        if self.is_future(symbol):
            contract = Contract()
            contract.symbol = symbol[:2]
            contract.currency = 'USD'
            contract.secType = 'CONTFUT'

            contractDetail = self.reqContractDetailsSync(contract)
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
    pass



if __name__ == '__main__':
    client = IBClient()
    client.connect('127.0.0.1', port=4001, clientId=1)
    contract = client.symbol2contract('NGmain')
    print(contract.__dict__)
    client.close()
    pass
