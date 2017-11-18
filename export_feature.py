from config import dataio;
import config;
import numpy as np;
import pandas as pd;
import sys;

if __name__=='__main__':
    df = dataio.getLabelAndFeature(config.LABEL,config.FEATURE_SELECT);
    df = df[df[config.LABEL]>-1];
    df = dataio.joinTurnoverRank(df);
    label = np.squeeze(df[[config.LABEL]].values);
    idxChoose = ((label<config.FILT_DOWN) | (label>=config.FILT_UP));
    df = df[idxChoose];
    label = label[idxChoose];
    labelBin = np.where(label>=config.FILT_UP,1,0);
    df['label'] = pd.Series(labelBin, index=df.index);
    df.drop(config.LABEL, axis=1, inplace=True);
    df.to_csv(sys.argv[1]);
    pass;
