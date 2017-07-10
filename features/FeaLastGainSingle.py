
from BaseFeaSingleStock import BaseFeaSingleStock;
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class FeaLastGainSingle(BaseFeaSingleStock):
    def __init__(self):
        self.ndays_ = 10;
        pass;
    
    def extract(self):

        
        def process(secID,recs):
            val = [rec['closePrice'] for rec in recs];
            grad = utils_common.computeGrad(val);
            fea = np.zeros((len(recs),self.ndays_));
            indices = [];
            
            for i,rec in enumerate(recs):
                
                secID = rec['secID'];
                tradeDate = rec['tradeDate'];

                indices.append((secID,tradeDate));
                
                for ii in range(self.ndays_):
                    pos = i-ii;
                    if pos<=0:
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

            return pd.DataFrame(fea,index=indices,columns=columnNames);
        
        secResults = dataio.forEachSecID('MktEqudAdjAfGet',['closePrice'],process);

        return pd.concat(secResults);
        pass;
