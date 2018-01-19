import math;

class StrategyEvery1DayTrade():
    def __init__(self):
        pass;

    def calculateAmount(self,preClosePrices,minSpend,maxSpend,buyFee):
        spend = 0.0;
        amounts = [];

        for preClosePrice in preClosePrices:
            orderPrice = preClosePrice*1.098;
            amount = math.ceil(minSpend/orderPrice/100)*100;
            cspend = orderPrice * amount * (1+buyFee);

            if (spend+cspend)> maxSpend:
                amounts.append((0,0));
                continue;
            else:
                spend += cspend;
                amounts.append((amount,orderPrice));
                pass;
            pass;
        return amounts;
        pass;
    
    def handle(self,dt,t,trader,decFactor):
        if t=='close':
            selled = set();
            for pos in trader.getAvailable():
                sec = pos['secID'];
                amount = pos['amount'];
                preClosePrice = trader.getPreClosePrice(sec);
                price = trader.getPrice(sec);

                if (price-preClosePrice)/preClosePrice>=0.098:
                    continue;
                else:
                    sell_price = preClosePrice * 0.902
                    selled.add(sec);
                    pass;
                pass;

            trader.sellSec(selled);
            pass;

        if decFactor is None:
            return;
        #decFactor.sort_values([c for c in decFactor.columns if c!='secID' and c!='tradeDate'],
        #                      inplace=True,ascending=False);
        if t=='open':
            selected = []
            for i in range(min(100,decFactor.shape[0])):
                if decFactor.values[i,1]>0.0:
                    sec = decFactor.values[i,0];
                    preClosePrice = trader.getPreClosePrice(sec);
                    price = trader.getPrice(sec);

                    if price<=0:
                        continue;
                    
                    if (price-preClosePrice)/price<=-0.11:
                        continue;
                    else:
                        selected.append(decFactor.values[i,0]);
                        pass;
                    pass;
                pass;

            maxSpend = 0.5 * trader.getMarketValue();
            minSpend = max(5000,maxSpend*0.168);
            prices,preClosePrices = trader.getPricesAndPreClosePrices(selected);
            amounts = self.calculateAmount(preClosePrices,minSpend,maxSpend,
                                           trader.getBuyFee());

            buyList = [(sec,amount,price) for sec,(amount,price) in zip(selected,amounts) \
                       if amount>0];

            trader.buyList(buyList);
            pass;
        pass;
    
