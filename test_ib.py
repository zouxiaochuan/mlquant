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

        if tickType != 'LAST':
            return
        
        print('{0},{1},{2},{3}'.format(time.time(), 'tickPrice', tickType,
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
        
        print('{0},{1},{2},{3}'.format(time.time(), 'tickSize', tickType, size))        
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

        # print('{0},{1},{2}'.format('tickString', tickType, value))
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
    contract.symbol = 'USO'
    contract.currency = 'USD'
    contract.secType = 'STK'
    contract.exchange = 'SMART'
    # contract.primaryExchange = 'ARCA'

    contract2 = Contract()
    contract2.symbol = 'SPY'
    contract2.currency = 'USD'
    contract2.secType = 'STK'
    contract2.exchange = 'SMART'
    contract2.primaryExchange = 'ARCA'

    contract3 = Contract()
    contract3.symbol = 'CL'
    contract3.currency = 'USD'
    contract3.secType = 'CONTFUT'
    contract3.exchange = 'NYMEX'
    # contract3.lastTradeDateOrContractMonth = '202005'

    contract4 = Contract()
    contract4.symbol = "EUR"
    contract4.secType = "CASH"
    contract4.currency = "GBP"
    contract4.exchange = "IDEALPRO"
    
    # client.reqMktData(1001, contract3, '', False, False, [])
    # client.reqMktData(1002, contract2, '', False, False, [])
    # client.reqTickByTickData(1003, contract, 'Last', 0, False)
    client.reqContractDetails(1004, contract3)
    client.run()

    print('come to an end')
    pass
