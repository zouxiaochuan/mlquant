import os;
import uuid;
import datetime;
import pandas as pd;
import numpy as np;
from collections import defaultdict;
import glob;
import importlib;
import sys;
import inspect;
import imp;


def system(cmd,ignoreError=False):
    logger.debug('excute commoand: ' + cmd);

    p = subprocqess.Popen(cmd, shell=True, stdin=subprocess.PIPE,
                          stdout=subprocess.PIPE,
                          stderr=subprocess.STDOUT,close_fds=True);

    p.stdin.close();
    ret = '';
    
    while True:
        line = p.stdout.readline();
        if not line:
            break;
        if type(line)==unicode:
            line = line.encode('utf8');
            pass;
        line = trimLine(line);
        logger.debug(line);
        ret += line+'\n';
        pass;
    
    retcd = p.wait();
    if (not ignoreError) and (retcd!=0):
        raise RuntimeError('error in exec cmd: {0}'.format(cmd));
    
    return ret;
                                                                                                                                    
def system(cmd):
    retcd = os.system(cmd);
    if retcd != 0:
        raise RuntimeError('error in excute: {0}'.format(cmd));
    pass;

def getTempName():
    return 'zztemp_' + str(uuid.uuid4()).replace('-','_');

def tempName():
    return getTempName();

def file2list(filename):
    ret = [];
    with open(filename) as fin:
        for line in fin:
            ret.append(line.strip());
            pass;
        pass;
    return ret;

def dtAdd(dt,days):
    return datetime.datetime.strftime(datetime.datetime.strptime(dt,'%Y-%m-%d')\
                                      +datetime.timedelta(days=days),'%Y-%m-%d');

def dt2str(date):
    return datetime.datetime.strftime(date,'%Y-%m-%d');

def dtDiff(dt1,dt2):
    date1 = datetime.datetime.strptime(dt1,'%Y-%m-%d');
    date2 = datetime.datetime.strptime(dt2,'%Y-%m-%d');
    return (date1-date2).days;

def getCurrentDt():
    return datetime.datetime.strftime(datetime.datetime(),'%Y-%m-%d');

def getStrategy():
    pass;

def getTradeDates():
    return np.squeeze(pd.read_csv('tradeDates.csv').values);

def groupDt(df):
    d = defaultdict(list);
    idxDt = df.columns.get_loc('tradeDate');
    arr = df.values;

    dfSub = df[[c for c in df.columns if c!='tradeDate']];
    arrSub = dfSub.values;

    for i in range(len(arr)):
        d[arr[i,idxDt]].append(arrSub[i]);
        pass;

    ret = dict();
    for dt,recList in d.items():
        df = pd.DataFrame(data=np.vstack(recList),columns=dfSub.columns);
        for c,d in zip(dfSub.columns,dfSub.dtypes):
            df[c] = df[c].astype(d);
            pass;
        if isinstance(dt, unicode):
            dt = dt.encode('utf8');
        ret[dt] = df;
        pass;

    return ret;

def getStrategy(filename):
    name = filename.split('/')[-1][:-3];
    m = imp.load_source(name,filename);
    cls = getattr(m,name);

    return cls();

def minSumSubList(alist):
    best = cur = 0;
    for v in alist:
        cur = min(cur + v, 0);
        best = min(best, cur);
        pass;
    return best;

def computeGrad(vlist):
    rlist = [];
    for i in range(len(vlist)):
        if i==0:
            rlist.append(None);
        else:
            rlist.append(vlist[i]-vlist[i-1]);
            pass;
        pass;
    return rlist;

def bucketValue(val,blist):

    buckets = blist + [-i for i in blist] + [0];
    buckets = sorted(list(set(buckets)));
            
    for i in range(len(buckets)):
        if val<=buckets[i]:
            return i;
        pass;

    return len(buckets);


