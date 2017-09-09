
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class LabelFund300(object):
    def __init__(self):
        pass;

    def extract(self):
        df = dataio.getdf('MktFunddAdjGet')[['openPrice']];
        df = df[(df[['openPrice']]>0).values];

        df = df[df.index.get_level_values('secID')=='510300.XSHG'];

        def process(sec,recs):
            indices = [];
            values = [];

            n = len(recs);
            
            for i,rec in enumerate(recs):
                #stock must be listed for 100 days
                indices.append((rec['secID'],rec['tradeDate']));
                if (i+2)>=n:
                    values.append(-999);
                    continue;
                
                rec1 = recs[i+1];
                rec2 = recs[i+2];

                l = (rec2['openPrice']-rec1['openPrice'])/rec1['openPrice'];


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
                

                


