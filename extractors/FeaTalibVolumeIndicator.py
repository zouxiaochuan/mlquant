
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
import talib;

class FeaTalibVolumeIndicator(object):
    def __init__(self):
        pass;
    
    def extract(self):

        def process(secID,recs):
            indices = [(rec['secID'],rec['tradeDate']) for rec in recs];

            high = np.array([rec['highestPrice'] for rec in recs]);
            low = np.array([rec['lowestPrice'] for rec in recs]);
            close = np.array([rec['closePrice'] for rec in recs]);
            volume = np.array([rec['turnoverRate'] for rec in recs]);
            ad = talib.AD(high, low, close, volume)
            adosc = talib.ADOSC(high, low, close, volume);
            obv = talib.OBV(close, volume);

            fea = np.vstack((ad,adosc,obv)).T;
            
            columnNames = [];
            namePrefix = self.__class__.__name__;

            columnNames.append(namePrefix+'_AD');
            columnNames.append(namePrefix+'_ADOSC');
            columnNames.append(namePrefix+'_OBV');
            
            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=columnNames);
            return df;

        df = dataio.getdf('MktEqudAdjAfGet')[['closePrice','isOpen',
                                              'highestPrice','lowestPrice',
                                              'turnoverRate']];
        df = df[df['isOpen']==1];
        
        secResults = dataio.forEachSecID(df,process);

        return pd.concat(secResults);
        pass;
