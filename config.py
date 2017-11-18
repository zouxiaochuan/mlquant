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
    'FundETFConsGet': ['secID','tradeDate','consID'],
    'MarginDetails': ['secID','tradeDate']
};

TUSHARE_DATA_NAME = {'MarginDetails'};

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

FEATURE_SELECT_OLD = [
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
    'FeaHighLowRateSum_min_10',
    #'FeaHighLowRateSum_max_20'
    #,'FeaHighLowRateSum_min_20',
    'FeaFlowRate_1'
    #,'FeaFlowRate_5',
    #'FeaFlowRate_10'
    #,'FeaFlowRate_20'
    #,'FeaLastTurnoverValueMA_5'
    #,'FeaLastTurnoverValueMA_10'
    #,'FeaLastTurnoverValueMA_20'
    #,'FeaLastGainMA_5'
    #,'FeaLastGainMA_10'
    #,'FeaLastGainMA_20'

];

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
    #'FeaTalib_MA_5',
    #'FeaTalib_MA_10',
    #'FeaTalib_MA_20',
    #'FeaTalib_DEMA_10',
    #'FeaTalib_DEMA_20',
    #'FeaTalib_EMA_10',
    #'FeaTalib_EMA_20'
];


LABEL = 'LabelEvery1DayTrade';

FILT_UP = 0.02;
FILT_DOWN = 0.015;

WEIGHTER = weight_generator.Step();
