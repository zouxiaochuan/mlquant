LOCAL_PATH_RAW='../raw';
LOCAL_PATH_FEA='../data/features';
LOCAL_PATH_DF='../data/df';


DATA_NAMES=[
    {
        'name':'MktEqudGet',
        'key': ['secID','tradeDate']
    },
    {
        'name':'MktEquFlowGet',
        'key': ['secID','tradeDate']
    },
    {
        'name':'MktIdxdGet',
        'key': ['indexID','tradeDate']
    },
    {
        'name':'SecSTGet',
        'key': ['secID','tradeDate']
    },
    {
        'name':'MktEquFlowOrderGet',
        'key': ['secID','tradeDate']
    },
    {
        'name':'MktEqudAdjAfGet',
        'key': ['secID','tradeDate']
    }
];

BLACK_LIST=[
    '000033.XSHE'
];


CONN_STR='mongodb://0.0.0.0:27017';
DB_STR='quant_offline';

import dataio_df as dataio;
