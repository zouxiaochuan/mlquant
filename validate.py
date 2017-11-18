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
import weight_generator;


FEATURE_SELECT = [
    'FeaLastGainSingle_0',
    'FeaLastGainSingle_1',
    'FeaLastGainSingle_2',
    'FeaLastGainSingle_3',
    'FeaLastGainSingle_4',
    'FeaLastGainSum_5',
    'FeaLastGainSum_10',
    'FeaLastGainSum_20',
    'FeaLastGainSum_50',
    'FeaLastOneDayRate_OpenClose_0',
    'FeaLastOneDayRate_OpenClose_1',
    'FeaLastOneDayRate_High_0',
    'FeaLastOneDayRate_High_1',
    'FeaLastOneDayRate_Low_0',
    'FeaLastOneDayRate_Low_1',
    'FeaLastTurnoverValueGrad_0',
    'FeaLastTurnoverValueGrad_1',
    'FeaLastTurnoverValueGrad_2',
    'FeaLastTurnoverValueGrad_3',
    'FeaHighLowRateSum_max_5',
    'FeaHighLowRateSum_min_5',
    'FeaHighLowRateSum_max_10',
    'FeaHighLowRateSum_min_10'
    ,'FeaHighLowRateSum_max_20'
    ,'FeaHighLowRateSum_min_20'
    ,'FeaFlowRate_1'
    ,'FeaFlowRate_5'
    ,'FeaFlowRate_10'
    ,'FeaFlowRate_20'
    ,'FeaLastTurnoverValueMA_5'
    ,'FeaLastTurnoverValueMA_10'
    ,'FeaLastTurnoverValueMA_20'
    ,'FeaLastGainMA_5'
    ,'FeaLastGainMA_10'
    ,'FeaLastGainMA_20'
    #,'FeaFlowGradRate_moneyInflow_1'
    #,'FeaFlowGradRate_moneyOutflow_1'
    ,'FeaFlowGradRate_netMoneyInflow_1'
    #,'FeaFlowOrderRate_inflowS_1'
    #,'FeaFlowOrderRate_outflowS_1'
    ,'FeaLastGainStats_MaxSumSubList_200'
    ,'FeaLastGainStats_MinSumSubList_200'
    ,'FeaLastGainStats_PositiveRate_50'
    ,'FeaLastGainStats_NegativeRate_50'
    ,'FeaLastGainStats_PositiveRate_5'
    #,'FeaIndexSZZZGainSum_1'
    ,'FeaLastMarginRate_rzye_0'
    ,'FeaLastMarginRate_rzye_1'
    ,'FeaLastMarginRate_rzye_2'
    ,'FeaLastMarginRate_rzye_3'
    #'FeaTalib_MA_5',
    #'FeaTalib_MA_10',
    #'FeaTalib_MA_20',
    #'FeaTalib_DEMA_10',
    #'FeaTalib_DEMA_20',
    #'FeaTalib_EMA_10',
    #'FeaTalib_EMA_20'
];

LABEL = 'LabelEvery1DayTrade';

YEARS = [
    #'2014'
    '2015'
    ,'2016'
    ,'2017'
    ,'2018'];

FILT_UP = 0.02;
FILT_DOWN = 0.015;
WEIGHTER = weight_generator.Step();
FEATURE_NUM = 80;

def validateReg(labelTrain,labelTest,featureTrain,featureTest,dtTest,weightTrain):
    #cls = xgb.XGBClassifier(max_depth=4,learning_rate=0.1,n_estimators=150);
    cls = xgb.XGBRegressor(max_depth=4,learning_rate=0.09,n_estimators=150);
    #print(featureTrain.shape);
    #print(featureTest.shape);
    #print(labelTest);
    print('training sample: {0}'.format(featureTrain.shape[0]));
    cls.fit(featureTrain,labelTrain,
            sample_weight=weightTrain,
            eval_set=[(featureTrain,labelTrain),
                      (featureTest,labelTest)]
            );

    pred = np.squeeze(cls.predict(featureTest));
    print('{0}:{1},{2},{3},{4},{5}'.format(year,
                                           topNacc(dtTest,labelTest,pred,5),
                                           topNexp(dtTest,labelTest,5),
                                           topNacc(dtTest,labelTest,pred,10),
                                           topNacc(dtTest,labelTest,pred,100),
                                           'haha'
    ));
    
    pass;


def validate(labelTrain,labelTest,featureTrain,featureTest,dtTest,weightTrain):
    idxChoose = ((labelTrain<FILT_DOWN) | (labelTrain>=FILT_UP));
    labelTrain = labelTrain[idxChoose];
    featureTrain = featureTrain[idxChoose,:];

    labelBin = np.where(labelTrain>=FILT_UP,1,0);
    labelTestBin = np.where(labelTest>=FILT_UP,1,0);

    cls = xgb.XGBClassifier(max_depth=4,learning_rate=0.1,n_estimators=150);
    #cls = xgb.XGBRegressor(max_depth=4,learning_rate=0.1,n_estimators=150);
    #print(featureTrain.shape);
    #print(featureTest.shape);
    #print(labelTest);
    print('training sample: {0}'.format(featureTrain.shape[0]));
    print(len(weightTrain));
    weightTrain = weightTrain[idxChoose];
    #w2 = np.ones(labelTrain.shape);
    #w2[labelTrain<-0.05] = 3.0;
    #weightTrain = weightTrain * w2;
    
    cls.fit(featureTrain,labelBin,eval_metric='auc',sample_weight=weightTrain,
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

def getFeatureNames(n=30):
    names = [];
    with open('feature_importance.txt') as fin:
        for i,line in enumerate(fin):
            if i>=n:
                break;
            fname = line.strip().split(',')[0];
            names.append(fname);
            pass;
        pass
    return names;
            

def getWeight(dt):
    udt = sorted(np.unique(dt).tolist(),reverse=True);
    uw = WEIGHTER.get(len(udt));
    wdict = {udt[i]:uw[i] for i in range(len(udt))};

    op = np.vectorize(lambda x:wdict[x]);
    return op(dt);


if __name__=='__main__':
    print('load data...');
    #FEATURE_SELECT = getFeatureNames(FEATURE_NUM);
    #FEATURE_SELECT = dataio.getAllFeatureNames();
    print('feature length: ' + str(len(FEATURE_SELECT)));
    
    df = dataio.getLabelAndFeature(LABEL,FEATURE_SELECT);
    df = df[df[LABEL]>-1];

    print(df.shape[0]);
    #df = dataio.joinHS300(df);
    df = dataio.joinTurnoverRank(df);
    print(df.shape[0]);
    
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
        dtTrain = dt[idxTrain];
        weightTrain = getWeight(dtTrain);
        
        validate(labelTrain,labelTest,featureTrain,featureTest,dtTest,weightTrain);
        pass;
    
    pass;


