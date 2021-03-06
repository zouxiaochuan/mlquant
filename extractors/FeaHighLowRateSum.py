
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class FeaHighLowRateSum(object):
    def __init__(self):
        self.ndays_ = [1,2,5,10,20,50,100,200];
        pass;
    
    def extract(self):
        def process(secID,recs):
            fea = np.zeros((len(recs),len(self.ndays_)*2),dtype=np.float32);

            close = [rec['closePrice'] for rec in recs];
            high = [rec['highestPrice'] for rec in recs];
            low = [rec['lowestPrice'] for rec in recs];
            low = [99999 if i==0 else i for i in low];

            ndayHigh = [];
            ndayLow = [];

            for nday in self.ndays_:
                ndayHigh.append(utils_common.slideWindowMaximum(high,nday));
                ndayLow.append(utils_common.slideWindowMinimum(low,nday));
                pass;
            
            indices = [];
            
            for i,rec in enumerate(recs):    
                secID = rec['secID'];
                tradeDate = rec['tradeDate'];

                indices.append((secID,tradeDate));

                for ii,nday in enumerate(self.ndays_):
                    maxp = ndayHigh[ii][i];
                    minp = ndayLow[ii][i];
                                        
                    fea[i,ii*2] = (close[i]-maxp)/maxp if maxp!=0 else 0;
                    fea[i,ii*2+1] = (close[i]-minp)/minp if minp!=0 else 0;
                    pass;

                pass;

            columnNames = [];
            namePrefix = self.__class__.__name__;
            for nday in self.ndays_:
                columnNames.append(namePrefix+'_max_'+str(nday));
                columnNames.append(namePrefix+'_min_'+str(nday));
                pass;

            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=columnNames);
            return df;

        df = dataio.getdf('MktEqudAdjAfGet')[['highestPrice','lowestPrice','closePrice','isOpen']];
        df = df[(df[['isOpen']]==1).values];
        
        secResults = dataio.forEachSecID(df,process);

        return pd.concat(secResults);
        pass;
