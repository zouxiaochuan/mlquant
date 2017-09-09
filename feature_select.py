from config import dataio;
import config;
import xgboost as xgb;
import sklearn;
import sklearn.metrics;
import sklearn.svm;
import sklearn.ensemble;
import sklearn.calibration;
import sklearn.preprocessing;
import numpy as np;
import utils_common;
import weight_generator;
from functools import partial;
import pandas as pd;
import common_proc;

LABEL = 'LabelEvery1DayTrade';
NUMBER = 30;


FILT_UP = 0.02;
FILT_DOWN = 0.01;

if __name__=='__main__':
    print('load data...');
    FEATURE_SELECT = dataio.getAllFeatureNames();
    print('feature length: ' + str(len(FEATURE_SELECT)));
    
    df = dataio.getLabelAndFeature(LABEL,FEATURE_SELECT);
    df = df[df[LABEL]>-1];

    #df = df.apply(partial(pd.to_numeric, errors='coerse'));
    
    print('prepare...');
    dt = df.index.get_level_values('tradeDate');

    label = np.squeeze(df[[LABEL]].values);
    feature = df[FEATURE_SELECT].values;

    #feature[np.isnan(feature)] = 0;
    idxChoose = ((label<FILT_DOWN) | (label>=FILT_UP));
    label = label[idxChoose];
    feature = feature[idxChoose,:];
    weight = common_proc.getWeight(dt);

    labelBin = np.where(label>=FILT_UP,1,0);
    #cls = sklearn.ensemble.RandomForestClassifier(n_estimators=200,n_jobs=-1,max_depth=10);
    cls = xgb.XGBClassifier(max_depth=2,learning_rate=0.3,n_estimators=150);

    print('begin...');
    cls.fit(feature,labelBin,sample_weight=weight);
    importances = cls.feature_importances_
    indices = np.argsort(importances)[::-1];
    
    with open('feature_importance.txt','w') as fout:
        for ind in indices:
            fout.write('{0},{1}\n'.format(df.columns[ind],importances[ind]));
            pass;
        pass;
    

    

