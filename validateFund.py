from config import dataio;
import config;
import xgboost as xgb;
import sklearn;
import sklearn.metrics;
import sklearn.svm;
import sklearn.calibration;
import sklearn.preprocessing;
import sklearn.linear_model;
import numpy as np;
import utils_common;
import weight_generator;
import utils_parallel;
import random;
import sgd;


FEATURE_SELECT = [
    ('FeaFund300LastGainSingle_0', 0)
    ,('FeaFund300LastGainSingle_1', 1)
    ,('FeaFund300LastGainSingle_2', 2)
    ,('FeaFund300LastGainSingle_3', 3)
    #,('FeaFund300LastGainSingle_4', 4)
    #,('FeaFund300LastGainSingle_5', 5)
    #,('FeaFund300LastGainSingle_6', 6)
    #,('FeaFund300LastGainSingle_7', 7)    
];

LABEL = 'LabelFund300';

feaNames = [i[0] for i in FEATURE_SELECT];
feaRank = [i[1] for i in FEATURE_SELECT];


FILT_UP = 0.00001;
FILT_DOWN = -0.00001;
THRESHOLD = 0;

TEST_DAYS = 365;

def calcScore(l,p):
    psort = np.argsort(p);

    #print(p);
    return sum(l[psort[:(len(l)/10)]]);
    

def validate(labelTrain,labelTest,featureTrain,featureTest,param):
    labelBin = np.where(labelTrain>=THRESHOLD,1,0);
    labelTestBin = np.where(labelTest>=THRESHOLD,1,0);

    cls = sklearn.linear_model.LogisticRegression(C=param);
    #cls = sgd.SGDSolver(sgd.LinearTimeSeries(feaRank,param));

    #print('training sample: {0}'.format(featureTrain.shape[0]));
    cls.fit(featureTrain,labelBin);

    pred = cls.predict_proba(featureTest.reshape(1,-1))[:,cls.classes_==1][0][0];
    #pred = cls.predict_proba(featureTest.reshape(1,-1))[0];
    #print((labelTest,pred));
    #print(featureTest.reshape(1,-1));
    
    return labelTest,pred;

if __name__=='__main__':
    print('load data...');
    print('feature length: ' + str(len(FEATURE_SELECT)));


    print(feaNames);
    df = dataio.getLabelAndFeature(LABEL,feaNames);
    df = df[df[LABEL]>-1];
    
    print('prepare...');
    dt = df.index.get_level_values('tradeDate');

    label = np.squeeze(df[[LABEL]].values);
    feature = df[feaNames].values;

    idxChoose = ((label<FILT_DOWN) | (label>=FILT_UP)) & (~np.any(np.isnan(feature),axis=1));
    label = label[idxChoose];
    feature = feature[idxChoose];

    print('begin');

    for C in [1e-5,1e-4,1e-3,1e-2,1e-1,1,10,100,1000,10000,1e5]:
    #for C in [1e-7,1e-6,1e-5,1e-4,1e-3,1e-2,1e-1]:
        def test(testn):
            featureTrain = feature[:-testn];
            featureTest = feature[-testn,:];
            labelTrain = label[:-testn];
            labelTest = label[-testn];
            return validate(labelTrain,labelTest,featureTrain,featureTest,C);
        
        results = utils_parallel.parallel(test,list(range(1,TEST_DAYS+1)));

        #l = np.array([0 if r[0]<0 else 1 for r in results]);
        l = np.array([r[0] for r in results]);
        p = np.array([r[1] for r in results]);
        #print(len([0 for i in l if i==0]));
        #print(len(l));
        #auc = sklearn.metrics.roc_auc_score(l,p);
        score = calcScore(l,p);
        print('{0}:{1}'.format(C,score));
        pass;
    pass;


