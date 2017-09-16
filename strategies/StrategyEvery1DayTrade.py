import math;

class StrategyEvery1DayTrade():
    def __init__(self):
        pass;

    def calculateAmount(self,prices,minSpend,maxSpend,buyFee):
        spend = 0.0;
        amounts = [];

        for price in prices:
            amount = math.ceil(minSpend/price/100)*100;
            cspend = (price+0.05) * amount * (1+buyFee);

            if (spend+cspend)> maxSpend:
                amounts.append(0);
                continue;
            else:
                spend += cspend;
                amounts.append(amount);
                pass;
            pass;
        return amounts;
        pass;
    
    def handle(self,dt,t,trader,decFactor):
        if t=='close':
            selled = set();
            for pos in trader.getAvailable():
                sec = pos['secID'];
                preClosePrice = trader.getPreClosePrice(sec);
                price = trader.getPrice(sec);

                if (price-preClosePrice)/preClosePrice>=0.098:
                    continue;
                else:
                    selled.add(sec);
                    pass;
                pass;

            trader.sellSec(selled);
            pass;

        if decFactor is None:
            return;
        decFactor.sort_values([c for c in decFactor.columns if c!='secID' and c!='tradeDate'],
                              inplace=True,ascending=False);
        if t=='open':
            selected = []
            for i in range(100):
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
            minSpend = max(5000,maxSpend*0.2);
            prices = trader.getPrices(selected);
            amounts = self.calculateAmount(prices,minSpend,maxSpend,trader.getBuyFee());

            buyList = [(sec,amount) for sec,amount in zip(selected,amounts) if amount>0];

            trader.buyList(buyList);
            pass;
        pass;
    
