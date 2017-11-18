
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
import utils_stats;
import sys;

ndays_ = [2,5,10,20,50,100,200,1000000];
funcs_ = utils_stats.allFunctions;
__self__ = sys.modules[__name__];

def process(secID,recs):
    
    val = [rec['closePrice'] for rec in recs];
    grad = utils_common.computeGradRate(val);
    grad = [0 if g is None else g for g in grad];
    
    windows = [];
    for nday in ndays_:
        for func in funcs_:
            windows.append(func(grad,nday));
            pass;
        pass;

    if (len(funcs_)==0):
        raise RuntimeError(secID);
    
    fea = np.array(windows).T;

    indices = [];
    
    for i,rec in enumerate(recs):
        secID = rec['secID'];
        tradeDate = rec['tradeDate'];
        indices.append((secID,tradeDate));
        pass;
        
    return indices,fea;

class FeaLastGainStats(object):
    def __init__(self):
        pass;

    def getNames(self):
        columnNames = [];
        namePrefix = __self__.__name__;
        for nday in ndays_:
            for func in funcs_:
                columnNames.append(namePrefix+'_'+func.__name__+'_'+str(nday));
                pass;
            pass;
        return columnNames;
    
    def extract(self):
        df = dataio.getdf('MktEqudAdjAfGet')[['closePrice']];
        dfFea = dataio.forEachSecIDEx(df,process,self.getNames());

        return dfFea;
        pass;
