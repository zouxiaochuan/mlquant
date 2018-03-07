
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
import utils_stats;
import sys;

ndays_ = [0,1,2,3,4,5];
__self__ = sys.modules[__name__];

def process(secID,recs):
    
    closePrice = [rec['closePrice'] for rec in recs];
    closeIndex = [rec['closeIndex'] for rec in recs];
    priceGrad = [v if v is not None else 0 for v in utils_common.computeGradRate(closePrice)];
    indexGrad = [v if v is not None else 0 for v in utils_common.computeGradRate(closeIndex)];

    val = [p * i * 10000 for p,i in zip(priceGrad,indexGrad)];
    
    feas = []
    for i in range(len(val)):
        f = []
        for nday in ndays_:
            pos = i - nday
            if pos<=0:
                f.append(0)
            else:
                f.append(val[pos])
                pass
            pass
        feas.append(f)
        pass

    indices = [];
    
    for i,rec in enumerate(recs):
        secID = rec['secID'];
        tradeDate = rec['tradeDate'];
        indices.append((secID,tradeDate));
        pass;
        
    return indices,feas;

class FeaGainMultiplyMarket(object):
    def __init__(self):
        pass;

    def getNames(self):
        columnNames = [];
        namePrefix = __self__.__name__;
        for nday in ndays_:
            columnNames.append(namePrefix+'_'+str(nday));
            pass;
        return columnNames;
    
    def extract(self):
        df = dataio.getdf('MktEqudAdjAfGet')[['closePrice']];
        dfIndex = dataio.getdf('MktIdxdGet')[['closeIndex','ticker']];

        dfIndex = dfIndex[dfIndex['ticker']=='000001']
        dfIndex.reset_index(inplace=True)
        dfIndex.set_index(['tradeDate'], inplace=True)

        df = df.join(dfIndex)
        
        dfFea = dataio.forEachSecIDEx(df,process,self.getNames());

        return dfFea;
        pass;
