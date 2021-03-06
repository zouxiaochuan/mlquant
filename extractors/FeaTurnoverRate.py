
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
import utils_stats;
import sys;

ndays_ = [0,1,2,3,4,5];
__self__ = sys.modules[__name__];

def process(secID,recs):
    
    val = [rec['turnoverRate'] for rec in recs];

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

class FeaTurnoverRate(object):
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
        df = dataio.getdf('MktEqudAdjAfGet')[['turnoverRate']];
        dfFea = dataio.forEachSecIDEx(df,process,self.getNames());

        return dfFea;
        pass;
