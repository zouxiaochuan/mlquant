import sys;
import cPickle as pickle;
from config import dataio;
import config;
import utils_common;
import numpy as np;
import pandas as pd;

def main(modelPath,outpath):
    df = dataio.getLabelAndFeature(config.LABEL,config.FEATURE_SELECT);

    df = dataio.joinTurnoverRank(df);
    dts = df.index.get_level_values('tradeDate').values;
    maxDt = np.max(dts);
    df = df[dts==maxDt];

    feature = df[config.FEATURE_SELECT].values;
    cls = pickle.load(open(modelPath));
    pred = np.squeeze(cls.predict_proba(feature)[:,cls.classes_==1]);

    dfout = pd.DataFrame(pred,
                         index=df.index,
                         columns = ['score']
                         );

    dfout.to_csv(outpath,float_format='%g');
    pass;


if __name__=='__main__':
    main(sys.argv[1],sys.argv[2]);
    pass;
