import sys;
from config import dataio;
import config;
import xgboost as xgb;
import cPickle as pickle;
import numpy as np;
import utils_common;

def daily_train(feature,label,dts,dtEnd,savePath):    
    idx = (dts<dtEnd) & (dts>=utils_common.dtAdd(dtEnd,-config.TRAINING_DAYS));

    feature = feature[idx];
    label = label[idx];

    weight = utils_common.getWeight(dts[idx],config.WEIGHTER);

    cls = xgb.XGBClassifier(max_depth=4,learning_rate=0.1,n_estimators=150);
    print('training sample: {0}'.format(feature.shape));
    print(weight.shape);
    cls.fit(feature,label,sample_weight=weight);

    print('train end');
    pickle.dump(cls,open(savePath,'w'));
    pass;

def loadData():
    df = dataio.getLabelAndFeature(config.LABEL,config.FEATURE_SELECT);
    df = df[df[config.LABEL]>-1];
    df = dataio.joinTurnoverRank(df);

    dts = df.index.get_level_values('tradeDate');

    label = np.squeeze(df[[config.LABEL]].values);
    feature = df[config.FEATURE_SELECT].values;
    idxChoose = ((label<config.FILT_DOWN) | (label>=config.FILT_UP));
    label = label[idxChoose];
    feature = feature[idxChoose];
    dts = dts[idxChoose];
    labelBin = np.where(label>=config.FILT_UP,1,0);
    return labelBin,feature,dts;

def main(dtEnd,savePath):
    label,feature,dts = loadData();

    daily_train(feature,label,dts,dtEnd,savePath);

if __name__=='__main__':
    dtEnd = sys.argv[1];
    savePath = sys.argv[2];
    main(dtEnd,savePath);
    pass;
