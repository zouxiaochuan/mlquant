import urllib2;
import sys;
import pandas as pd;
import json;
import utils_common;

ip = '47.52.101.241'

def getDataFrame(dt,trimSec=False):
    queryStr = json.dumps({'tradeDate':dt});
    jsonstr = urllib2.urlopen('http://47.52.101.241:18000/queryScore',
                              data=queryStr,timeout=10).read();
    records = json.loads(jsonstr)['data'];
    if len(records)>0:
        for rec in records:
            if trimSec:
                rec['secID'] = rec['secID'].split('.')[0];
                pass;
            pass;
    
        return pd.DataFrame().from_records(records);
    else:
        return None;

def getDecFactorSingle(dt,trimSec=False):
    dfDec = getDataFrame(dt,trimSec);
    if dfDec is None:
        return None;
    dfDec.drop('tradeDate', axis=1, inplace=True);
    dfDec = dfDec[['secID','score']];
    return dfDec;

def getDecFactors(dtStart,dtEnd):
    ret = dict();

    decFactors = dict();
    dt = utils_common.dtAdd(dtStart,-7);

    while dt<=dtEnd:
        decFactor = getDecFactorSingle(dt);
        if decFactor is not None:
            decFactors[dt] = decFactor;
            pass;
        dt = utils_common.dtAdd(dt,1);
        pass;

    # shift dt
    sortedDt = sorted(list(decFactors.keys()));
    mapDt = {sortedDt[i]:sortedDt[i+1] for i in range(len(sortedDt)-1)};

    for k,v in mapDt.items():
        ret[v] = decFactors[k];
        pass;
    
    return ret;
