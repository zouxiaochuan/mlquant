import os;
import uuid;
import datetime;
import pandas as pd;
import numpy as np;
from collections import defaultdict;
from collections import deque;
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
    return datetime.datetime.strftime(datetime.datetime.now(),'%Y-%m-%d');

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

def records2dict(recs):
    names = {k.encode('utf8') for rec in recs for k in rec.dtype.names};

    ret = dict();
    for name in names:
        ret[name] = list();
        pass;

    for rec in recs:
        for name in names:
            ret[name].append(rec[name]);
            pass;
        pass;

    for name in names:
        ret[name] = np.array(ret[name]);
        pass;
    return ret;

def readCsvLocalPath(path):
    filenames = os.listdir(path);
    data = None;
    for f in sorted(filenames):
        fullpath = os.path.join(path,f);
        print(fullpath);
        df = pd.read_csv(fullpath);
        if data is None:
            data = df;
        else:
            data = data.append(df);
            pass;
        pass;
    return data;

def mergeCsvLocal(path,mergeName):
    df = readCsvLocalPath(path);
    df.to_csv(mergeName,index=False);
    pass;

def getWeight(dt,WEIGHTER):
    udt = sorted(np.unique(dt).tolist(),reverse=True);
    uw = WEIGHTER.get(len(udt));
    wdict = {udt[i]:uw[i] for i in range(len(udt))};

    op = np.vectorize(lambda x:wdict[x]);
    return op(dt);

def topNacc(dt,label,pred,n):
    udt = sorted(np.unique(dt).tolist());

    def process(idt):
        idx = (dt==idt);
        cl = label[idx];
        cp = pred[idx];

        acc = np.mean(cl[np.argsort(cp)[::-1][:n]]);
        return acc;

    accs = [process(idt) for idt in udt];

    return np.mean(accs);

def topNPosRate(dt,label,pred,n):
    udt = sorted(np.unique(dt).tolist());

    def process(idt):
        idx = (dt==idt);
        cl = label[idx];
        cp = pred[idx];

        acc = np.mean(cl[np.argsort(cp)[::-1][:n]]);
        return 1 if acc>=0 else 0;

    accs = [process(idt) for idt in udt];

    return np.mean(accs);


def shiftDtPre(df):
    udt = np.sort(np.unique(df.index.get_level_values('tradeDate').values));
    dtMap = {udt[i]:udt[i-1] for i in range(1,udt.shape[0])};
    minDt = np.min(udt);

    df = df.reset_index();

    arr = df.values;
    idxDt = df.columns.get_loc('tradeDate');
    
    for i in range(df.shape[0]):
        dt = arr[i,idxDt];
        if dt==minDt:
            arr[i,idxDt] = '0000-00-00'
        else:
            arr[i,idxDt] = dtMap[dt];
            pass;
        pass;

    df = pd.DataFrame(arr,columns=df.columns);
    df.set_index(['secID','tradeDate'],inplace=True);
    return df;

def shiftDtPost(df):
    udt = np.sort(np.unique(df.index.get_level_values('tradeDate').values));
    dtMap = {udt[i]:udt[i+1] for i in range(udt.shape[0]-1)};
    maxDt = np.max(udt);

    df = df.reset_index();

    arr = df.values;
    idxDt = df.columns.get_loc('tradeDate');
    
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

def slideWindowMaximum(values,windowSize):
    q = deque();

    ret = [];
    for i in range(len(values)):
        while len(q)>0 and values[i]>values[q[-1]]:
            q.pop();
            pass;
        q.append(i);
        if q[0]<=(i-windowSize):
            q.popleft();
            pass;
        
        ret.append(values[q[0]]);
        pass;

    return ret;

if __name__=='__main__':
    print(slideWindowMaximum([4,5,8,7,6,2,1,9],4));
