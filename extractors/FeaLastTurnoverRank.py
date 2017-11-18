from config import dataio
import pandas as pd
import numpy as np


class FeaLastTurnoverRank(object):
    def __init__(self):
        self.ndays_ = 180
        pass

    def extract(self):
        def lastTurnoverMedian(secID, recs):
            val = [rec['turnoverValue'] for rec in recs]
            fea = np.zeros((len(recs), 1), dtype=np.float32)
            indices = []
            for i, rec in enumerate(recs):
                secID = rec['secID']
                tradeDate = rec['tradeDate']
                indices.append((secID, tradeDate))
                idxStart = max(0, i - self.ndays_)
                if idxStart == i:
                    fea[i, 0] = val[i]
                else:
                    fea[i, 0] = np.min(val[idxStart:i])
                    pass
                pass

            df = pd.DataFrame(fea,
                              index=pd.MultiIndex.from_tuples(indices,
                                                              names=['secID','tradeDate']),
                              columns=['turnoverMedian']);
            return df;

        df = dataio.getdf('MktEqudAdjAfGet')[['turnoverValue']]

        df = df[df['turnoverValue'] > 0]
        
        medians = dataio.forEachSecID(df, lastTurnoverMedian)
        dfMedian = pd.concat(medians)

        def ranker(dfDt):
            rank = dfDt.shape[0]-(np.argsort(np.squeeze(dfDt.values))).argsort()-1;

            dfRet = dfDt.copy();
            dfRet['FeaLastTurnoverRank'] = rank;
            dfRet.drop('turnoverMedian', axis=1,inplace=True);
            return dfRet;
        
        df = dfMedian.groupby('tradeDate',group_keys=False).apply(ranker)
        return df;
