
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;

class FeaLastOneDayRate(object):
    def __init__(self):
        self.ndays_ = 10;
        pass;
    
    def extract(self):

        
        def process(secID,recs):
            values = dict();
            values['OpenClose'] = [(rec['closePrice']-rec['openPrice'])/rec['openPrice'] \
                                   if rec['openPrice']>0 else None for rec in recs];
            values['Open'] = [(rec['openPrice']-rec['preClosePrice'])/rec['preClosePrice'] \
                              if rec['preClosePrice']>0 else None for rec in recs];
            values['High'] = [(rec['highestPrice']-rec['openPrice'])/rec['openPrice'] \
                              if rec['openPrice']>0 else None for rec in recs];
            values['Low'] = [(rec['lowestPrice']-rec['openPrice'])/rec['openPrice'] \
                             if rec['openPrice']>0 else None for rec in recs];
            values = values.items();

            fea = np.zeros((len(recs),self.ndays_*len(values)),dtype=np.float32);
            indices = [];
            
            for i,rec in enumerate(recs):
                secID = rec['secID'];
                tradeDate = rec['tradeDate'];

                indices.append((secID,tradeDate));
                
                for ii in range(self.ndays_):
                    pos = i-ii;
                    for iii in range(len(values)):
                        colIdx = ii*len(values)+iii;
                        if pos<0:
                            v = None;
                        else:
                            v = values[iii][1][pos];
                            pass;
                        fea[i,colIdx] = v;
                        pass;
                    pass;
                pass;

            columnNames = [];
            namePrefix = self.__class__.__name__;
            
            for ii in range(self.ndays_):
                for iii in range(len(values)):
                    columnNames.append(namePrefix+'_'+values[iii][0]+'_'+str(ii));
                    pass;
                pass;

            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=columnNames);
            return df;

        df = dataio.getdf('MktEqudAdjAfGet')[['openPrice','closePrice','isOpen','preClosePrice',
                                              'highestPrice','lowestPrice']];
        df = df[df['isOpen']==1];
        
        secResults = dataio.forEachSecID(df,process);

        return pd.concat(secResults);
        pass;
