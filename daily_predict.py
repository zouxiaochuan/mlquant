import sys;
import cPickle as pickle;
from config import dataio;
import config;
import utils_common;
import numpy as np;
import pandas as pd;

def main(modelPath,outpath,dt=None):
    df = dataio.getLabelAndFeature(config.LABEL,config.FEATURE_SELECT);
    turnoverFilter = dataio.getTurnoverRankFilter();
    maxContinousCloseDayFilter = dataio.getMaxContinousCloseDayFilter();
    secFilter = turnoverFilter & maxContinousCloseDayFilter;
    idxFilter = np.asarray([True if st in secFilter else False \
                            for st in df.index]);

    df = df[idxFilter]

    
    dts = df.index.get_level_values('tradeDate').values;
    if dt is None:
        dt = np.max(dts);
        pass;
    
    df = df[dts==dt];


    feature = df[config.FEATURE_SELECT].values;
    cls = pickle.load(open(modelPath));
    #pred = np.squeeze(cls.predict_proba(feature)[:,cls.classes_==1]);
    pred = np.squeeze(cls.predict(feature));

    dfout = pd.DataFrame(pred,
                         index=df.index,
                         columns = ['score']);
    
    dfout = dfout[dfout.index.map(lambda i:i[0] not in config.BLACK_LIST).get_values()]
    dfout.sort_values(['score'],inplace=True,ascending=False);

    dfout.to_csv(outpath,float_format='%g');
    pass;


if __name__=='__main__':
    main(sys.argv[1],sys.argv[2],sys.argv[3]);
    pass;
