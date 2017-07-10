import utils_io;
import pandas as pd;
import config;
import os;
import pandas as pd;
import utils_stock;
import utils_parallel;
import utils_common;
import numpy as np;

def initdb():
    pass;

def getdb():
    return config.LOCAL_PATH_DF;

def importdb(dataname):
    dstpath = os.path.join(getdb(),dataname['name']);
    path = os.path.join(config.LOCAL_PATH_RAW,dataname['name'] + '.csv');
    df = pd.read_csv(path,index_col=dataname['key']);
    utils_io.write_df(dstpath,df);

def forEachSecIDInternal(param):
    secID,df,func = param;
    df = df[df.index.get_level_values('secID')==secID];
    recs = df.sort_index().to_records();
    return func(secID,recs);

def forEachSecID(tablename,columnNames,func):
    cols = ['secID','tradeDate'] + columnNames;
    
    path = os.path.join(getdb(),tablename)
    df = pd.read_hdf(path,'data');
    df = df[columnNames];
    df = df[df.index.map(lambda i:utils_stock.filterSecID(i[0])).get_values()];
    df.sort_index(inplace=True);

    secs = df.index.get_level_values('secID');

    start = 0;
    ranges = [];
    for i in range(df.shape[0]):
        if i>0:
            if secs[i]!=secs[i-1] and utils_stock.filterSecID(secs[i-1]):
                ranges.append((secs[i-1],start,i));
                start = i;
                pass;
            pass;
        pass;

    if utils_stock.filterSecID(secs[i-1]):
        ranges.append((secs[i-1],start,i));
        pass;
    
    
    return utils_parallel.parallel_debug(forEachSecIDInternal,
                                         [(sec,df[start:end],func) for sec,start,end in ranges],nProc=4);
    pass;

def save_df(df,name):
    dstpath = os.path.join(getdb(),name);
    utils_io.write_df(dstpath,df);

if __name__=='__main__':
    pass;

