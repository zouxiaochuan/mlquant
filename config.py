LOCAL_PATH_RAW='../raw';
LOCAL_PATH_FEA='../data/features';
LOCAL_PATH_DF='../data/df';


DATA_NAMES={
    'MktEqudGet': ['secID','tradeDate'],
    'MktEquFlowGet': ['secID','tradeDate'],
    'MktIdxdGet': ['indexID','tradeDate'],
    'SecSTGet': ['secID','tradeDate'],
    'MktEquFlowOrderGet': ['secID','tradeDate'],
    'MktEqudAdjAfGet': ['secID','tradeDate']
};

BLACK_LIST=[
    '000033.XSHE'
];


CONN_STR='mongodb://0.0.0.0:27017';
DB_STR='quant_offline';

import dataio_csv as dataio;

FEATURE_SELECT = [
];

TRAINING_DAYS = 5*365;
