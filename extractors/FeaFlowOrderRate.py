
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
import sklearn.preprocessing;

class FeaFlowOrderRate(object):
    def __init__(self):
        self.ndays_ = [1,2,5,10];
        self.keynames_ = ['inflowS','inflowM','inflowL','inflowXl','outflowS','outflowM',\
                          'outflowL','outflowXl'];
        pass;
    
    def extract(self):
        def process(secID,recs):
            windows = [];

            for nday in self.ndays_:
                win = np.zeros((len(self.keynames_),len(recs)));
                for i,key in enumerate(self.keynames_):
                    origin = [abs(rec[key]) for rec in recs];
                    win[i,:]= utils_common.slideWindowAverage(origin,nday);
                    pass;

                win = sklearn.preprocessing.normalize(win,norm='l1',axis=0);
                
                windows.append(win);
                pass;
                        
            fea = np.zeros((len(recs),len(self.ndays_)*len(self.keynames_)),dtype=np.float32);
            indices = [];
            
            for i,rec in enumerate(recs):                
                secID = rec['secID'];
                tradeDate = rec['tradeDate'];

                indices.append((secID,tradeDate));
                
                for ii in range(len(self.ndays_)):
                    for iii,key in enumerate(self.keynames_):                        
                        fea[i,ii*len(self.keynames_)+iii] = windows[ii][iii,i];
                        pass;
                    pass;
                pass;

            columnNames = [];
            namePrefix = self.__class__.__name__;
            for ii in range(len(self.ndays_)):
                for iii,key in enumerate(self.keynames_):
                    columnNames.append(namePrefix+'_'+key+'_'+str(self.ndays_[ii]));
                pass;

            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=columnNames);
            return df;

        df = dataio.getdf('MktEquFlowOrderGet')[self.keynames_];
        
        secResults = dataio.forEachSecID(df,process);

        return pd.concat(secResults);
        pass;
