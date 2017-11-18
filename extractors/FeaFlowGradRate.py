
from config import dataio;
import utils_common;
import pandas as pd;
import numpy as np;
from copy import copy;

class FeaFlowGradRate(object):
    def __init__(self):
        self.ndays_ = [1,2,5,10,20];
        self.keynames_ = ['moneyInflow','moneyOutflow','netMoneyInflow'];
        pass;
    
    def extract(self):
        def process(secID,recs):
            values = [];

            for key in self.keynames_:
                values.append([rec[key] for rec in recs]);
                pass;

            grads = [];
            for nday in self.ndays_:
                for i in range(len(self.keynames_)):
                    win = utils_common.slideWindowAverage(values[i],nday);
                    grad = utils_common.computeGradRate(win);
                    grads.append(grad);
                    pass;
                pass;
                        
            fea = np.zeros((len(recs),len(self.ndays_)*len(self.keynames_)),dtype=np.float32);
            indices = [];

            fea = np.array(grads).T;
            for i,rec in enumerate(recs):                
                secID = rec['secID'];
                tradeDate = rec['tradeDate'];

                indices.append((secID,tradeDate));
                
                #for j in range(len(self.ndays_)):
                #    for k in range(len(self.keynames)):
                #        l = j*len(self.keynames_) + k;
                #        fea[i,l] = grads[l][i];
                #        pass;
                #    pass;
                #pass;

            columnNames = [];
            namePrefix = self.__class__.__name__;
            for j in range(len(self.ndays_)):
                for k in range(len(self.keynames_)):
                    columnNames.append(namePrefix+'_'+self.keynames_[k] + '_' \
                                       + str(self.ndays_[j]));
                    pass;
                pass;

            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=columnNames);
            return df;

        df = dataio.getdf('MktEquFlowGet')[self.keynames_];
        
        secResults = dataio.forEachSecID(df,process);

        return pd.concat(secResults);
        pass;
