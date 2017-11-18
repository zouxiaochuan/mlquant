
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class FeaFlowRate(object):
    def __init__(self):
        self.ndays_ = [1,5,10,20,50];
        pass;
    
    def extract(self):
        def process(secID,recs):
            inflowOrigin = [rec['moneyInflow'] for rec in recs];
            outflowOrigin = [rec['moneyOutflow'] for rec in recs];
            
            inflows = [];
            outflows = [];

            for nday in self.ndays_:
                inflows.append(utils_common.slideWindowAverage(inflowOrigin,nday));
                outflows.append(utils_common.slideWindowAverage(outflowOrigin,nday));
                pass;
            
            fea = np.zeros((len(recs),len(self.ndays_)),dtype=np.float32);
            indices = [];
            
            for i,rec in enumerate(recs):                
                secID = rec['secID'];
                tradeDate = rec['tradeDate'];

                indices.append((secID,tradeDate));
                
                for ii in range(len(self.ndays_)):
                    inf = inflows[ii][i];
                    outf = outflows[ii][i];

                    
                    fea[i,ii] = inf/(inf+outf) if (inf+outf)>0 else 0;
                    pass;
                pass;

            columnNames = [];
            namePrefix = self.__class__.__name__;
            for ii in range(len(self.ndays_)):
                columnNames.append(namePrefix+'_'+str(self.ndays_[ii]));
                pass;

            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=columnNames);
            return df;

        df = dataio.getdf('MktEquFlowGet')[['moneyInflow','moneyOutflow']];
        
        secResults = dataio.forEachSecID(df,process);

        return pd.concat(secResults);
        pass;
