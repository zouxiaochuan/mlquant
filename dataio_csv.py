import utils_io;
import pandas as pd;
import config;
import os;
import pandas as pd;
import utils_stock;
import utils_parallel;
import utils_common;
import numpy as np;
import utils_stock;
import glob;

def initdb():
    pass;

def getdb():
    return config.LOCAL_PATH_DF;

def importdb(dataname,keys):
    dstpath = os.path.join(getdb(),dataname);
    path = os.path.join(config.LOCAL_PATH_RAW,dataname + '.csv');
    df = pd.read_csv(path,index_col=keys);

    if df.index.names[0]==u'secID':
        df = df[df.index.map(lambda i:utils_stock.filterSecID(i[0])).get_values()];
        pass;

    df.to_csv(dstpath);

def getdf(name):
    return pd.read_csv(os.path.join(getdb(),name),index_col=config.DATA_NAMES[name]);

def forEachSecID(df,func):
    df.sort_index(inplace=True);

    secs = df.index.get_level_values('secID');
    start = 0;
    ranges = [];
    #print(df.shape);
    for i in range(df.shape[0]):
        if i>0:
            if secs[i]!=secs[i-1]:
                ranges.append((secs[i-1],start,i));
                start = i;
                pass;
            pass;
        pass;

    ranges.append((secs[i-1],start,i));

    ret = [];
    for i,(sec,start,end) in enumerate(ranges):
        if i%400==0:
            print(i);
            pass;
        recs = df[start:end].to_records();
        ret.append(func(sec,recs));
        pass;

    return ret;

def save_df(df,name):
    dstpath = os.path.join(getdb(),name);
    df.to_csv(dstpath,float_format='%g');
    pass;

def getFeatureInternal(names):
    filenameMap = scanColumnName('Fea*',names);

    dfs = [];
    for filename,columns in filenameMap:
        dfs.append(pd.read_csv(filename,index_col=['secID','tradeDate'],
                               usecols=(['secID','tradeDate']+columns)));
        pass;

    return dfs;
    pass;

def getLabel(name):
    filenameMap = scanColumnName('Label*',[name]);
    filename,column = filenameMap[0];
    return pd.read_csv(filename,index_col=['secID','tradeDate'],
                       usecols=(['secID','tradeDate']+column));

def getLabelAndFeature(labelName,featureNames):
    features = getFeatureInternal(featureNames);
    label = getLabel(labelName);

    return label.join(features,how='left');

def scanColumnName(pattern,columns):
    dataPath = getdb();
    
    files = glob.glob(dataPath + '/' + pattern);

    results = list();
    for f in files:
        with open(f) as fin:
            cols = fin.next().strip().split(',');
            cols = [c for c in cols if c in columns];
            if len(cols)>0:
                print('{0}:{1}'.format(f,','.join(cols)));
                results.append((f,cols));
                pass;
            pass;
        pass;

    return results;

    

