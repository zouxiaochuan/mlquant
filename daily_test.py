import sys;
import cPickle as pickle;
from config import dataio;
import config;
import backtest;
import utils_common;
import pandas as pd;
import numpy as np;
import os;

def daily_test(feature,dts,index,initMoney,startDt,modelFile,strategy):
    idx = dts>=startDt;
    fea = feature[idx];
    cls = pickle.load(open(modelFile));
    #pred = np.squeeze(cls.predict_proba(fea)[:,cls.classes_==1]);
    pred = np.squeeze(cls.predict(fea));
    index = index[idx];
    dfDec = pd.DataFrame(pred,
                         index=pd.MultiIndex.from_tuples(index,
                                                         names=['secID','tradeDate']),
                         columns = ['DecFactor']
                         );

    dfDec = utils_common.shiftDtPost(dfDec);
    dfDec.reset_index(inplace=True);
    dfDec.sort_values(['tradeDate','DecFactor'],inplace=True,ascending=False);
    decFactor = utils_common.groupDt(dfDec);
    backtest.backtest(initMoney,startDt,'2019-01-01',strategy,decFactor);
    pass;

def main(modelPath,startDt,endDt,initMoney,strategy,reportPath,testStartDt):
    df = dataio.getLabelAndFeature(config.LABEL,config.FEATURE_SELECT);
    turnoverFilter = dataio.getTurnoverRankFilter();
    maxContinousCloseDayFilter = dataio.getMaxContinousCloseDayFilter();
    secFilter = turnoverFilter & maxContinousCloseDayFilter;
    idxFilter = np.asarray([True if st in secFilter else False \
                            for st in df.index]);

    df = df[idxFilter]
    
    feature = df[config.FEATURE_SELECT].values;
    dts = df.index.get_level_values('tradeDate');
    index = df.index.values;

    dt = startDt;
    while dt<=endDt:
        print(dt);
        filename = 'xgb_' + dt;
        stdout = sys.stdout;

        with open(os.path.join(reportPath,filename),'w') as fout:
            sys.stdout = fout;
            daily_test(feature,dts,index,initMoney,testStartDt,
                       os.path.join(modelPath,filename),
                       strategy);
            sys.stdout = stdout;
            pass;
        dt = utils_common.dtAdd(dt,1);
    pass;

if __name__=='__main__':
    modelPath = sys.argv[1];
    startDt = sys.argv[2];
    endDt = sys.argv[3];
    initMoney = float(sys.argv[4]);
    strategy = utils_common.getStrategy(sys.argv[5]);
    reportPath = sys.argv[6];
    testStartDt = sys.argv[7];
    main(modelPath,startDt,endDt,initMoney,strategy,reportPath,testStartDt);
    pass;
