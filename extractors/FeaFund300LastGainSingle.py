
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class FeaFund300LastGainSingle(object):
    def __init__(self):
        self.ndays_  = 10;
        pass;

    def extract(self):
        df = dataio.getdf('MktFunddAdjGet')[['closePrice']];
        df = df[(df[['closePrice']]>0).values];

        df = df[df.index.get_level_values('secID')=='510300.XSHG'];

        def process(sec,recs):
            indices = [];
            values = [];

            n = len(recs);
            val = [rec['closePrice'] for rec in recs];
            fea = np.zeros((len(recs),self.ndays_),dtype=np.float32);

            for i,rec in enumerate(recs):
                #stock must be listed for 100 days

                secID = rec['secID'];
                tradeDate = rec['tradeDate'];

                for ii in range(self.ndays_):
                    pos = i-ii;
                    if pos<=0:
                        v = None;
                    else:
                        v = (val[pos]-val[pos-1])/val[pos-1];
                        pass;
                    fea[i,ii] = v;
                    pass;

                indices.append((secID,tradeDate));
                pass;

            columnNames = [];
            namePrefix = self.getName();
            for ii in range(self.ndays_):
                columnNames.append(namePrefix+'_'+str(ii));
                pass;

            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=columnNames);
            return df;

        dfs = dataio.forEachSecID(df,process);
        return pd.concat(dfs);
    
    def getName(self):
        return self.__class__.__name__;
