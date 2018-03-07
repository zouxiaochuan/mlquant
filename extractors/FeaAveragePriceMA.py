
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
import utils_stats;
import sys;

ndays_ = [2,5,10,20,50,100];
__self__ = sys.modules[__name__];

def process(secID,recs):    
    turnoverValue = [rec['turnoverValue'] for rec in recs]
    turnoverVol = [rec['turnoverVol'] for rec in recs]

    windowsValue = []
    windowsVol = []
    for nday in ndays_:
        windowsValue.append(utils_common.slideWindowAverage(turnoverValue, nday))
        windowsVol.append(utils_common.slideWindowAverage(turnoverVol, nday))
        pass
    
    fea = np.zeros((len(turnoverVol), len(ndays_)))
    
    for i in range(len(turnoverVol)):
        for j in range(len(ndays_)):
            if i==0:
                avg_price = 0
            elif windowsVol[j][i-1]==0:
                avg_price = 0
            else:
                avg_price = windowsValue[j][i-1]/windowsVol[j][i-1]
                pass
        
            if turnoverVol[i] == 0:
                fea[i, j] = 0;
            else:
                fea[i, j] = avg_price/(turnoverValue[i]/turnoverVol[i])
            pass
        pass
    
    indices = [];
    
    for i,rec in enumerate(recs):
        secID = rec['secID'];
        tradeDate = rec['tradeDate'];
        indices.append((secID,tradeDate));
        pass;
        
    return indices,fea;

class FeaAveragePriceMA(object):
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
