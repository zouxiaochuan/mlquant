
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class FeaLastTurnoverValueGrad(object):
    def __init__(self):
        self.ndays_ = 10;
        pass;
    
    def extract(self):

        
        def process(secID,recs):
            val = [rec['turnoverValue'] for rec in recs];
            grad = utils_common.computeGrad(val);
            fea = np.zeros((len(recs),self.ndays_),dtype=np.float32);
            indices = [];
            
            for i,rec in enumerate(recs):
                
                secID = rec['secID'];
                tradeDate = rec['tradeDate'];

                indices.append((secID,tradeDate));
                
                for ii in range(self.ndays_):
                    pos = i-ii;
                    if pos<=0:
                        v = None;
                    elif val[pos-1]==0:
                        v = None;
                    else:
                        v = grad[pos]/val[pos-1];
                        pass;
                    fea[i,ii] = v;
                    pass;

                pass;

            columnNames = [];
            namePrefix = self.__class__.__name__;
            for ii in range(self.ndays_):
                columnNames.append(namePrefix+'_'+str(ii));
                pass;

            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=columnNames);
            return df;

        df = dataio.getdf('MktEqudAdjAfGet')[['turnoverValue']];
        
        secResults = dataio.forEachSecID(df,process);

        return pd.concat(secResults);
        pass;
