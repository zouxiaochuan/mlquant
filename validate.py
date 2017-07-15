from config import dataio;
import config;
import xgboost as xgb;
import sklearn;
import sklearn.metrics;
import sklearn.svm;
import sklearn.calibration;
import sklearn.preprocessing;
import numpy as np;
import utils_common;


FEATURE_SELECT = [
    'FeaLastGainSingle_0',
    'FeaLastGainSingle_1',
    'FeaLastGainSingle_2',
    'FeaLastGainSum_5',
    'FeaLastGainSum_10',
    'FeaLastGainSum_50',
    'FeaLastOneDayRate_OpenClose_0',
#    'FeaLastOneDayRate_High_0',
    'FeaLastOneDayRate_Low_0',
    'FeaLastTurnoverValueGrad_0'
];

LABEL = 'LabelEvery1DayTrade';

YEARS = ['2014','2015','2016','2017','2018'];

FILT_UP = 0.02;
FILT_DOWN = 0.01;

def validate(labelTrain,labelTest,featureTrain,featureTest,dtTest):
    idxChoose = ((labelTrain<FILT_DOWN) | (labelTrain>=FILT_UP));
    labelTrain = labelTrain[idxChoose];
    featureTrain = featureTrain[idxChoose,:];

    labelBin = np.where(labelTrain>=FILT_UP,1,0);
    labelTestBin = np.where(labelTest>=FILT_UP,1,0);

    cls = xgb.XGBClassifier(max_depth=2,learning_rate=0.3,n_estimators=150);
    #print(featureTrain.shape);
    #print(featureTest.shape);
    #print(labelTest);
    print('training sample: {0}'.format(featureTrain.shape[0]));
    cls.fit(featureTrain,labelBin,eval_metric='auc',
            eval_set=[(featureTrain,labelBin),
                      (featureTest,labelTestBin)]
            );

    pred = np.squeeze(cls.predict_proba(featureTest)[:,cls.classes_==1]);
    print('{0}:{1},{2},{3},{4},{5}'.format(year,
                                           topNacc(dtTest,labelTest,pred,5),
                                           topNexp(dtTest,labelTest,5),
                                           topNacc(dtTest,labelTest,pred,10),
                                           topNacc(dtTest,labelTest,pred,100),
                                           sklearn.metrics.roc_auc_score(labelTestBin,pred)));
    
    pass;

def topNacc(dt,label,pred,n):
    udt = sorted(np.unique(dt).tolist());

    def process(idt):
        idx = (dt==idt);
        cl = label[idx];
        cp = pred[idx];

        return np.mean(cl[np.argsort(cp)[::-1][:n]]);

    accs = [process(idt) for idt in udt];

    return np.mean(accs);

def topNexp(dt,label,n):
    udt = sorted(np.unique(dt).tolist());

    accs = [];
    for idt in udt:
        idx = (dt==idt);
        cl = label[idx];

        accs.append(np.mean(cl));
        pass;

    return np.mean(accs);

if __name__=='__main__':
    print('load data...');
    df = dataio.getLabelAndFeature(LABEL,FEATURE_SELECT);
    df = df[df[LABEL]>-1];
    
    print('prepare...');
    dt = df.index.get_level_values('tradeDate');

    label = np.squeeze(df[[LABEL]].values);
    feature = df[FEATURE_SELECT].values;

    print('begin');
    for iy,year in enumerate(YEARS[:-1]):
        dtTrainStart = utils_common.dtAdd(year+'-01-01',-config.TRAINING_DAYS);
        idxTrain = (dt<year)&(dt>=dtTrainStart);
        idxTest = (dt>=year)&(dt<YEARS[iy+1]);
        labelTrain = label[idxTrain];
        labelTest = label[idxTest];
        featureTrain = feature[idxTrain];
        featureTest = feature[idxTest];
        dtTest = dt[idxTest];
        validate(labelTrain,labelTest,featureTrain,featureTest,dtTest);
        pass;
    
    pass;


