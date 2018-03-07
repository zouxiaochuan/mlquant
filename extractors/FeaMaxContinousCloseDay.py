
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
import utils_stats;
import sys;

ndays_ = [2,5,10,20,50,100,200];
__self__ = sys.modules[__name__];

def process(secID,recs):
    
    is_open = [rec['isOpen'] for rec in recs];

    wins = []
    for nday in ndays_:
        wins.append(utils_common.slideWindowMaxContinuous(is_open, nday, lambda x:x==0))
        pass

    
    feas = np.asarray(wins).T
    
    indices = [];
    
    for i,rec in enumerate(recs):
        secID = rec['secID'];
        tradeDate = rec['tradeDate'];
        indices.append((secID,tradeDate));
        pass;
        
    return indices,feas;

class FeaMaxContinousCloseDay(object):
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
        df = dataio.getdf('MktEqudAdjAfGet')[['isOpen']];
        dfFea = dataio.forEachSecIDEx(df,process,self.getNames());

        return dfFea;
        pass;
