import numpy as np;
import config;
from config import dataio;
import xgboost as xgb;
import utils_common;
import pandas as pd;

class BasePredictGain(object):
    def __init__(self,interval,labelName):
        self.iterval_ = interval;
        self.labelName_ = labelName;
        pass;

    def trainTestReg(self,labelTrain,featureTrain,featureTest):
        cls = xgb.XGBRegressor(max_depth=4,learning_rate=0.1,n_estimators=150);
        print('training sample: {0}'.format(featureTrain.shape[0]));
        cls.fit(featureTrain,labelTrain);
        pred = np.squeeze(cls.predict(featureTest));
        return pred;
        pass;
    def trainTest(self,labelTrain,featureTrain,featureTest,weight):
        idxChoose = ((labelTrain<config.FILT_DOWN) | (labelTrain>=config.FILT_UP));
        labelTrain = labelTrain[idxChoose];
        #print(idxChoose.shape);
        #print(featureTrain.shape);
        featureTrain = featureTrain[idxChoose,:];
        weight = weight[idxChoose];
        labelTrainBin = np.where(labelTrain>=config.FILT_UP,1,0);

        cls = xgb.XGBClassifier(max_depth=4,learning_rate=0.1,n_estimators=150);
        print('training sample: {0}'.format(featureTrain.shape[0]));
        cls.fit(featureTrain,labelTrainBin,sample_weight=weight);
        pred = np.squeeze(cls.predict_proba(featureTest)[:,cls.classes_==1]);
        return pred;
    
    def extract(self):
        df = dataio.getLabelAndFeature(self.labelName_,config.FEATURE_SELECT);
        df = df[df[self.labelName_]>-1];

        df = dataio.joinTurnoverRank(df);
        dt = '2015-01-01';

        dts = df.index.get_level_values('tradeDate');
        indices = df.index.values;
        label = np.squeeze(df[[self.labelName_]].values);
        feature = df[config.FEATURE_SELECT].values;

        #dtMax = '2016-01-01';
        dtMax = np.max(dts.values);
        prs = [];
        while dt<=dtMax:
            dtStart = dt;
            dtEnd = utils_common.dtAdd(dtStart,self.iterval_);

            print('start: {0}, end: {1}'.format(dtStart,dtEnd));

            idxTrain = (dts<dtStart) & (dts>=utils_common.dtAdd(dtStart,-config.TRAINING_DAYS));
            idxTest = (dts>=dtStart) & (dts<=dtEnd);

            labelTrain = label[idxTrain];
            featureTrain = feature[idxTrain];
            featureTest = feature[idxTest];
            weight = utils_common.getWeight(dts[idxTrain],config.WEIGHTER);

            pred = self.trainTest(labelTrain,featureTrain,featureTest,weight);
            #print(utils_common.topNPosRate(dts[idxTest],label[idxTest],pred,5));
            
            df = pd.DataFrame(pred,
                              index=pd.MultiIndex.from_tuples(indices[idxTest],
                                                              names=['secID','tradeDate']),
                              columns=[self.__class__.__name__]
                              );
            prs.append(df);
            dt = utils_common.dtAdd(dtEnd,1);
            
        df = pd.concat(prs);

        udt = np.sort(np.unique(df.index.get_level_values('tradeDate').values));
        dtMap = {udt[i]:udt[i+1] for i in range(udt.shape[0]-1)};
        maxDt = np.max(udt);

        df.reset_index(inplace=True);

        arr = df.values;
        idxDt = df.columns.get_loc('tradeDate');

        print(df.shape);
        for i in range(df.shape[0]):
            dt = arr[i,idxDt];
            if dt==maxDt:
                arr[i,idxDt] = '9999-99-99'
            else:
                arr[i,idxDt] = dtMap[dt];
                pass;
            pass;

        df = pd.DataFrame(arr,columns=df.columns);
        df.set_index(['secID','tradeDate'],inplace=True);
        return df;
    pass;
