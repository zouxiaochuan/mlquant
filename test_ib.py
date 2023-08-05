from typing import List
import time
from queue import Queue


from ibapi.wrapper import EWrapper
from ibapi.client import EClient
from ibapi.utils import iswrapper
from ibapi.contract import ContractDescription, Contract, ContractDetails
from ibapi.ticktype import TickTypeEnum
from ibapi.common import TickAttrib
from ibapi.common import TickAttribLast

ignore_prefix = {'BID', 'ASK'}
ignore_prefix = {}


class IBWrapper(EWrapper):
    def __init__(self):
        super().__init__()
        pass

    @iswrapper
    def symbolSamples(
            self,
            reqId: int,
            contractDescriptions: List[ContractDescription]):
        print(reqId)

        for cd in contractDescriptions:
            print(cd.contract.__dict__)
            pass
        pass

    @iswrapper
    def tickPrice(
            self, reqId: int ,
            tickType: int,
            price: float,
            attrib: TickAttrib):
        super().tickPrice(reqId, tickType, price, attrib)

        tickType = TickTypeEnum.to_str(tickType)

        for pf in ignore_prefix:
            if tickType.startswith(pf):
                return
            pass
        
        print('{0},{1},{2},{3},{4}'.format(time.time(), reqId, 'tickPrice', tickType,
                                       price))
        pass
    
    @iswrapper
    def tickSize(
            self, reqId,
            tickType: int,
            size: int):
        super().tickSize(reqId, tickType, size)
        tickType = TickTypeEnum.to_str(tickType)

        for pf in ignore_prefix:
            if tickType.startswith(pf):
                return
            pass
        
        print('{0},{1},{2},{3},{4}'.format(time.time(), reqId, 'tickSize', tickType, size))        
        pass
    
    @iswrapper
    def tickString(
            self, reqId: int, tickType: int, value: str):
        super().tickString(reqId, tickType, value)
        tickType = TickTypeEnum.to_str(tickType)

        for pf in ignore_prefix:
            if tickType.startswith(pf):
                return
            pass

        print('{0},{1},{2},{3}'.format('tickString', reqId, tickType, value))
        pass

    @iswrapper
    def tickByTickAllLast(self, reqId: int, tickType: int, time: int, price: float,
                          size: int, tickAttribLast: TickAttribLast,
                          exchange: str,
                          specialConditions: str):
        super().tickByTickAllLast(reqId, tickType, time, price, size, tickAttribLast,
                                  exchange, specialConditions)
        
        tickType = TickTypeEnum.to_str(tickType)
        # print('{0}\t{1}\t{2}\t{3}\t{4}\t{5}'.format(
        #     tickType, time, price, size, exchange, specialConditions))
        pass

    @iswrapper
    def contractDetails(self, reqId:int, contractDetails:ContractDetails):
        print(contractDetails.__dict__)
        pass
    pass


class IBClient(EClient):
    def __init__(self, wrapper):
        super().__init__(wrapper)
        pass
    pass


if __name__ == '__main__':
    wrapper = IBWrapper()
    client = IBClient(wrapper)

    client.connect('127.0.0.1', 4001, 1)
    # client.reqMatchingSymbols(211, 'CL')
    contract = Contract()
    contract.symbol = 'BABA'
    contract.currency = 'USD'
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    # contract.primaryExchange = 'ARCA'

    contract2 = Contract()
    contract2.symbol = 'PDD'
    contract2.currency = 'USD'
    contract2.secType = 'STK'
    contract2.exchange = 'SMART'
    # contract2.primaryExchange = 'ARCA'

    contract3 = Contract()
    contract3.symbol = 'BIDU'
    contract3.currency = 'USD'
    contract3.secType = 'STK'
    contract3.exchange = 'SMART'
    # contract3.lastTradeDateOrContractMonth = '202006'

    contract4 = Contract()
    contract4.symbol = "JD"
    contract4.currency = "USD"
    contract4.secType = "STK"
    contract4.exchange = "SMART"
    
    client.reqMarketDataType(1)
    client.reqMktData(1001, contract, '', False, False, [])
    client.reqMktData(1002, contract2, '', False, False, [])
    client.reqMktData(1003, contract3, '', False, False, [])
    client.reqMktData(1004, contract4, '', False, False, [])
    # client.reqTickByTickData(1003, contract, 'Last', 0, False)
    # client.reqContractDetails(10, contract)
    client.run()

    print('come to an end')
    pass
