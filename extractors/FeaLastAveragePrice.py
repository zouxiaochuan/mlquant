
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
import utils_stats;
import sys;

ndays_ = list(range(10));
__self__ = sys.modules[__name__];

def process(secID,recs):    
    closePrice = [rec['closePrice'] for rec in recs];
    averagePrice = [rec['turnoverValue']/rec['turnoverVol'] if rec['turnoverVol']!=0 else 0 for rec in recs];

    
    val = [ap/cp if cp!=0 else 0 for ap,cp in zip(averagePrice, closePrice)];
    
    feas = []
    for i in range(len(val)):
        f = []
        for nday in ndays_:
            pos = i - nday
            if pos<=0:
                f.append(-1)
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

class FeaLastAveragePrice(object):
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
        df = dataio.getdf('MktEqudAdjAfGet')[['turnoverVol', 'turnoverValue', 'closePrice']];        
        dfFea = dataio.forEachSecIDEx(df,process,self.getNames());

        return dfFea;
        pass;
