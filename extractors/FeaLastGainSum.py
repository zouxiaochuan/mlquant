
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class FeaLastGainSum(object):
    def __init__(self):
        self.ndays_ = [5,10,20,50,100,200];
        pass;
    
    def extract(self):
        def process(secID,recs):
            val = [rec['closePrice'] for rec in recs];
            fea = np.zeros((len(recs),len(self.ndays_)),dtype=np.float32);
            
            indices = [];
            
            for i,rec in enumerate(recs):    
                secID = rec['secID'];
                tradeDate = rec['tradeDate'];

                indices.append((secID,tradeDate));
                
                p = rec['closePrice'];
                for ii,nday in enumerate(self.ndays_):
                    pos = i-nday;
                    if pos<=0:
                        p1 = recs[0]['closePrice'];
                    else:
                        p1 = recs[pos]['closePrice'];
                        pass;
                    
                    fea[i,ii] = (p-p1)/p1
                    pass;

                pass;

            columnNames = [];
            namePrefix = self.__class__.__name__;
            for nday in self.ndays_:
                columnNames.append(namePrefix+'_'+str(nday));
                pass;

            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=columnNames);
            return df;

        df = dataio.getdf('MktEqudAdjAfGet')[['closePrice','isOpen']];
        df = df[(df[['isOpen']]==1).values]
        
        secResults = dataio.forEachSecID(df,process);

        return pd.concat(secResults);
        pass;
