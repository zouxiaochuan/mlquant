
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
import utils_stats;
import sys;

ndays_ = list(range(10));
__self__ = sys.modules[__name__];

def process(secID,recs):    
    turnoverValue = [rec['turnoverValue'] for rec in recs]
    turnoverVol = [rec['turnoverVol'] for rec in recs]

    average_price = [rec['turnoverValue']/rec['turnoverVol'] if rec['turnoverVol']>0 else 0 \
                     for rec in recs]

    grad = utils_common.computeGradRate(average_price)
    
    fea = []
    for i in range(len(grad)):
        f = []
        for nday in ndays_:
            pos = i - nday
            if pos<=0:
                f.append(-1)
            else:
                f.append(grad[pos])
                pass
            pass
        fea.append(f)
        pass
    
    
    indices = [];
    
    for i,rec in enumerate(recs):
        secID = rec['secID'];
        tradeDate = rec['tradeDate'];
        indices.append((secID,tradeDate));
        pass;
        
    return indices,fea;

class FeaAveragePriceGradRate(object):
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
        df = dataio.getdf('MktEqudAdjAfGet')[['turnoverVol', 'turnoverValue']];
        dfFea = dataio.forEachSecIDEx(df,process,self.getNames());

        return dfFea;
        pass;
