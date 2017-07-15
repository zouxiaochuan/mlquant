
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class BaseLabelEveryNDayTrade(object):
    def __init__(self,nday,buy_price='openPrice',sell_price='closePrice'):
        self.nday_ = nday;
        self.buyPrice_ = buy_price;
        self.sellPrice_ = sell_price;
        pass;

    def extract(self):
        priceKeys = {self.buyPrice_,self.sellPrice_};
        dfMkt = dataio.getdf('MktEqudAdjAfGet')[list(priceKeys) + ['isOpen']];
        dfFlow = dataio.getdf('MktEquFlowGet');
        dfFlow = dfFlow[['moneyInflow','moneyOutflow']];
        dfSt = dataio.getdf('SecSTGet')[['STflg']];
        df = dfMkt.join(dfFlow);
        df = df.join(dfSt,how='left');
        df = df[pd.isnull(df[['STflg']]).values];
        df = df[(df[['isOpen']]==1).values];
        df = df[(df[[self.buyPrice_]]>0).values];
        df = df[(df[[self.sellPrice_]]>0).values];

        def process(sec,recs):
            indices = [];
            values = [];

            n = len(recs);
            
            for i,rec in enumerate(recs):
                #stock must be listed for 100 days
                if i<=100:
                    continue;
                if i>=(n-self.nday_-1):
                    indices.append((rec['secID'],rec['tradeDate']));
                    values.append(-999);
                    continue;

                rec1 = recs[i+1];
                rec2 = recs[i+1+self.nday_];

                if rec1['moneyOutflow']<1000000 or rec1['moneyInflow']<1000000:
                    continue;
                if (rec1['moneyInflow']/rec1['moneyOutflow'])>100:
                    continue;

                l = (rec2[self.sellPrice_]-rec1[self.buyPrice_])/rec1[self.buyPrice_];
                indices.append((rec['secID'],rec['tradeDate']));
                values.append(l);
                pass;

            return pd.DataFrame(values,
                                index=pd.MultiIndex.from_tuples(indices,
                                                                names=['secID','tradeDate']),
                                columns=[self.getName()],
                                );
        
        dfs = dataio.forEachSecID(df,process);
        return pd.concat(dfs);
    def getName(self):
        return self.__class__.__name__;
                

                


