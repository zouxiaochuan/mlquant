
from config import dataio;
import pandas as pd;
import time;
import talib;
import sys;
import numpy as np;
import utils_common;
#import easyquotation;
import config;

def testFunctionName():
    funcNames = talib.get_functions();

    fname = funcNames[0];
    print(talib.abstract.Function(sys.argv[1]).input_names);
    print(talib.abstract.Function(sys.argv[1]));
    print(talib.abstract.Function(sys.argv[1]).input_arrays);
    f = talib.abstract.Function(sys.argv[1]);
    print(f.parameters);
    print(f.output_names);
    print(f.input_names.items());
    pass;

def testFeature():
    df = pd.read_csv('../data/df/FeaTalib',index_col=['secID','tradeDate']);
    df = df.tail(5);

    with open('test.txt','w') as fout:
        
        for name in df.columns:
            fout.write(name);
            fout.write(':');
            fout.write(','.join([str(i) for i in np.squeeze(df[[name]].values).tolist()]));
            fout.write('\n');
            pass;
        pass;
    pass;

def testQuotation():
    print(quotation.market_snapshot(prefix=True));
    pass;

def testIndex():
    df300 = dataio.getdf('FundETFConsGet');
    df300 = df300[df300.index.get_level_values('secID')=='510300.XSHG'];
    df300.reset_index(inplace=True);
    df300.drop('secID', axis=1, inplace=True);
    df300.rename(columns = {'consID':'secID'}, inplace=True);
    df300.set_index(['secID','tradeDate'],inplace=True);
    print(df300);
    pass;

def testIntegrity():
    dfadj = dataio.getdf('MktEqudAdjAfGet');
    df = dataio.getdf('MktEqudGet');

    dfset = set(df.index.values.tolist());

    for sec,dt in dfadj.index.values:
        if (sec,dt) not in dfset:
            print('{0},{1}'.format(sec,dt));
            pass;
        pass;
    pass;

def testDecFactor():
    df = dataio.getDecFactor('DecFactorPredictGainD1');
    df = utils_common.shiftDtPre(df);
    dfl = dataio.getLabel('LabelEvery1DayTrade');
    df = df.join(dfl,how='inner');
    
    df = df[df.index.get_level_values('tradeDate')>'2017'];

    print(utils_common.topNacc(df.index.get_level_values('tradeDate'),
                               np.squeeze(df['LabelEvery1DayTrade'].values),
                               np.squeeze(df['DecFactorPredictGainD1'].values),5));
    pass;

def testFeatureSize():
    features = dataio.getFeature(config.FEATURE_SELECT);
    label = dataio.getLabel(config.LABEL);

    df = label.join(features,how='left');
    print(df.shape);
    df = df[pd.notnull(df[config.LABEL])];
    print(df.shape);
    pass;
if __name__=='__main__':
    #print(dataio.getdb()['MktEqudAdjAfGet'].distinct('secID'));
    #df = pd.read_csv('../raw/MktEqudAdjAfGet.csv',index_col=['secID','tradeDate']);
    s = time.time();
    #df.to_hdf('x.hdf','x');
    #df = pd.read_hdf('x.hdf','x');
    #df.to_hdf('x2.hdf');

    #import BaseLabelEveryNDayTrade;
    #x = BaseLabelEveryNDayTrade.BaseLabelEveryNDayTrade(10);
    #x.extract();

    #testFunctionName();
    #testFeature();
    #testQuotation();
    #testIndex();
    #testIntegrity();
    #testDecFactor();
    testFeatureSize();

