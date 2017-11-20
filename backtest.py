import utils_common;
import sys;
from config import dataio;

globalMarket = None;
globalTradingDays = None;

class BacktestTrader(object):
    def __init__(self,initMoney):
        global globalMarket,globalTradingDays;
        
        self.buyFee_ = 0.001;
        self.sellFee_ = 0.002;
        self.cache_ = initMoney;

        if globalMarket is None:
            records = dataio.getdf('MktEqudAdjAfGet').to_records();
            self.market_ = dict();

            self.tradingDays_ = set();
            for i,rec in enumerate(records):
                if i%10000==0:
                    #print(i);
                    pass;
                self.market_[(rec['secID'],rec['tradeDate'])] = rec;
                self.tradingDays_.add(rec['tradeDate']);
                pass;
            globalMarket = self.market_;
            globalTradingDays = self.tradingDays_;
            pass;
        else:
            self.market_ = globalMarket;
            self.tradingDays_ = globalTradingDays;

        self.position_ = [];
        pass;

    def isTradingDay(self,dt):
        return dt in self.tradingDays_;

    def reset(self,cache):
        self.cache_ = cache;
        self.position_ = [];
    
    def setTime(self,dt,time):
        if not self.isTradingDay(dt):
            return False;
        
        if time=='open':
            self.priceKey_ = 'openPrice';
        elif time=='close':
            self.priceKey_ = 'closePrice';
        else:
            raise RuntimeError('cannot recognize time:' + str(time));

        for pos in self.position_:
           p = self.market_[(pos['secID'],dt)][self.priceKey_];
           if p>0:
               pos['price'] = p;
               pass;

           if dt>self.currentDt_:
               pos['holdDays'] += 1;
               pass;
           pass;

        self.currentDt_ = dt
        return True;
    
    def getMarketValue(self):
        value = self.cache_;
        for pos in self.position_:
            value += pos['price'] * pos['amount'];
            pass;

        return value;

    def getPrice(self,secID):
        return self.market_[(secID,self.currentDt_)][self.priceKey_];

    def getPrices(self,secList):
        prices = [];

        for sec in secList:
            prices.append(self.getPrice(sec));
            pass;
        return prices;

    def getPreClosePrice(self,secID):
        return self.market_[(secID,self.currentDt_)]['preClosePrice'];

    def getPricesAndPreClosePrices(self,secList):
        prices = self.getPrices(secList)
        preClosePrices = [self.getPreClosePrice(sec) for sec in secList]

        return prices, preClosePrices
    
    def buyList(self,alist):
        sucList = [];
        for secID,amount,bprice in alist:
            price = self.getPrice(secID);
            if price<=0:
                continue;
            if (amount<=0) or ((amount%100)!=0):
                raise RuntimeError('amount invalid:' + str(amount));
                
            spend = price * amount * (1+self.buyFee_);
            if spend > self.cache_:
                continue;
            else:
                pos = dict();
                pos['secID'] = secID;
                pos['buyPrice'] = price;
                pos['amount'] = amount;
                pos['price'] = price;
                pos['holdDays'] = 0;
                pos['buyDt'] = self.currentDt_;
                self.position_.append(pos);
                sucList.append((secID,amount));
                self.cache_ -= spend;
                pass;
            pass;
        return sucList;

    def sellList(self,alist):
        dels = []
        for secID,amount,sprice in alist:
            if amount<=0:
                continue

            for i,pos in enumerate(self.position_):
                if pos['secID']==secID and pos['holdDays']>0:
                    price = self.getPrice(secID);
                    if price<=0:
                        continue
                    preClosePrice = self.getPreClosePrice(secID)
                    if (price-preClosePrice)/preClosePrice<=-0.099:
                        continue

                    if pos['amount']<=amount:
                        amount -= pos['amount']
                        sub_amount = pos['amount']
                        dels.append(i)
                        pos['secID']=''
                        pass
                    else:
                        pos['amount'] -= amount
                        sub_amount = amount
                        pass

                    self.cache_ += price * sub_amount * (1-self.sellFee_);
                    if amount==0:
                        break
                    pass
                pass
            pass

        for i in reversed(dels):
            self.position_.pop(i)
            pass
        pass
    
    def sellSec(self,aset):
        dels = [];
        for i,pos in enumerate(self.position_):
            if pos['secID'] in aset:
                price = self.getPrice(pos['secID']);
                if price<=0:
                    continue;
                if pos['holdDays']==0:
                    continue;
                preClosePrice = self.getPreClosePrice(pos['secID']);
                if (price-preClosePrice)/preClosePrice<=-0.099:
                    continue;
                
                self.cache_ += price * pos['amount'] * (1-self.sellFee_);
                dels.append(i);
                pass;
            pass;

        for i in reversed(dels):
            self.position_.pop(i);
            pass;
        pass;

    def getAvailable(self):
        ret = [];
        for pos in self.position_:
            if pos['holdDays']>0:
                ret.append(pos);
                pass;
            pass;
        return ret;

    def getBuyFee(self):
        return self.buyFee_;
    pass;


def backtest(initMoney,dtStart,dtEnd,strategy,decFactor):
    print('dt start: ' + dtStart + ', dt end:' + dtEnd);

    totals = [];
    gains = [];
    tReturns = [];

    trader = BacktestTrader(initMoney);
    
    totals.append(trader.getMarketValue());

    numDt = 0;
    dt = dtStart;
    dts = decFactor.keys();
    if '9999-99-99' in dts:
        dts.remove('9999-99-99');
        pass;
    
    maxDt = max(dts);
    dtEnd = min(dtEnd,maxDt);
    dt = max(dt,min(dts));
    while dt<=dtEnd:
        if not trader.isTradingDay(dt):
            dt = utils_common.dtAdd(dt,1);
            continue;

        decFactorDt = decFactor[dt] if dt in decFactor else None;
        trader.setTime(dt,'open');
        strategy.handle(dt,'open',trader,decFactorDt);

        #print(decFactorDt.shape);
        #print('open: ' + str(len(trader.getPositions())) + ', cache: ' + str(trader.cache_));
        trader.setTime(dt,'close');
        strategy.handle(dt,'close',trader,decFactorDt);
        # print('close: ' + str([pos['secID'] for pos in trader.position_]) + ', cache: ' + str(trader.cache_));
        # print('close: ' + str(trader.getPositions()) + ', cache: ' + str(trader.cache_));

        totals.append(trader.getMarketValue());
        gains.append((totals[-1]-totals[-2])/totals[-2]);
        tReturns.append((totals[-1]-totals[0])/totals[0]);

        print('dt: {0}, value: {1}, gains: {2}, sharp: {3}'.format(dt,totals[-1],gains[-1],
              utils_common.sharpRatio(tReturns,0.1/200)));
        
        dt = utils_common.dtAdd(dt,1);
        numDt+=1;
        pass;

    print('total value: ' + str(totals[-1]));
    print('max loss: ' + str(utils_common.minSumSubList(gains)));
    posDays = len([i for i in gains if i>0]);
    totalDays = numDt;
    print('posive days: {0}/{1}'.format(float(posDays)/totalDays,totalDays));
    print('sharp ratio : {0}'.format(utils_common.sharpRatio(tReturns,0.1/200)));
    print(totalDays);

    pass;

def main():
    dtStart = '2016-01-01';
    dtEnd = '2018-01-01';
    initMoney = 10000000;
    decFactorName = 'DecFactorPredictGainD1';

    strategy = utils_common.getStrategy(sys.argv[1]);
    decFactor = dataio.getDecFactor(decFactorName);
    decFactor.reset_index(inplace=True);
    decFactor.sort_values(['tradeDate',decFactorName],inplace=True,ascending=False);
    decFactor = utils_common.groupDt(decFactor);
    
    backtest(initMoney,dtStart,dtEnd,strategy,decFactor);
    pass;


if __name__=='__main__':
    main();
