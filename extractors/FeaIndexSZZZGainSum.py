
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

ndays_ = [1,2,5,10,20,50,100,200,1000000];

class FeaIndexSZZZGainSum(object):
    def __init__(self):
        pass;

    def extract(self):
        df = dataio.getdf('MktIdxdGet')[['closeIndex']];

        df = df[df.index.get_level_values('indexID')=='000001.ZICN'];

        values = np.squeeze(df[['closeIndex']].values);
        fea = utils_common.computeGradRateIntervals(values,ndays_);
        fea = np.array(fea).T;

        columnNames = [];
        namePrefix = self.getName();
        for nday in ndays_:
            columnNames.append(namePrefix+'_'+str(nday));
            pass;

        df = pd.DataFrame(fea,
                          index=pd.Index(df.index.get_level_values('tradeDate'),
                                         name='tradeDate'),
                          columns=columnNames);

        dfMkt = dataio.getdf('MktEqudGet')[['closePrice']];

        df = dfMkt.join(df)[columnNames];
        return df;
    
    def getName(self):
        return self.__class__.__name__;
