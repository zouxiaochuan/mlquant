import weight_generator;

LOCAL_PATH_RAW='../raw';
LOCAL_PATH_FEA='../data/features';
LOCAL_PATH_DF='../data/df';


DATA_NAMES={
    'MktEqudGet': ['secID','tradeDate'],
    'MktEquFlowGet': ['secID','tradeDate'],
    'MktIdxdGet': ['indexID','tradeDate'],
    'SecSTGet': ['secID','tradeDate'],
    'MktEquFlowOrderGet': ['secID','tradeDate'],
    'MktEqudAdjAfGet': ['secID','tradeDate'],
    'MktFunddAdjGet': ['secID','tradeDate'],
    'FundETFConsGet': ['secID','tradeDate','consID']
};

BLACK_LIST=[
    '000033.XSHE'
];

WEIGHTER = weight_generator.Step();

CONN_STR='mongodb://0.0.0.0:27017';
DB_STR='quant_offline';

import dataio_csv as dataio;

FEATURE_SELECT = [
];

TRAINING_DAYS = 5*365;

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
];

LABEL = 'LabelEvery1DayTrade';

FILT_UP = 0.02;
FILT_DOWN = 0.01;

WEIGHTER = weight_generator.Step();
