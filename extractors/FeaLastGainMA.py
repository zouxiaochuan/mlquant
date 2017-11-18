
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class FeaLastGainMA(object):
    def __init__(self):
        self.ndays_ = [2,5,10,20,50,100];
        pass;
    
    def extract(self):
        
        def process(secID,recs):
            val = [rec['closePrice'] for rec in recs];
            windows = [];
            for nday in self.ndays_:
                windows.append(utils_common.slideWindowAverage(val,nday));
                pass;

            windows = np.array(windows).T;
            fea = np.zeros(windows.shape);

            for i in range(fea.shape[0]):
                if i==0:
                    fea[i,:] = 1;
                    pass;
                else:
                    for j in range(fea.shape[1]):
                        if windows[i-1,j]==0:
                            fea[i,j] = 0;
                        else:
                            fea[i,j] = val[i]/windows[i-1,j]
                            pass;
                        pass;
                    pass;
                pass;
            
            indices = [];
            
            for i,rec in enumerate(recs):
                secID = rec['secID'];
                tradeDate = rec['tradeDate'];
                indices.append((secID,tradeDate));
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

        df = dataio.getdf('MktEqudAdjAfGet')[['closePrice']];
        
        secResults = dataio.forEachSecID(df,process);

        return pd.concat(secResults);
        pass;
