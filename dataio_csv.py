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

def updatedb(dataname,keys,filterSecID=True):
    dstpath = os.path.join(getdb(),dataname);
    dfOrigin = pd.read_csv(dstpath,index_col=keys);
    
    path = os.path.join(config.LOCAL_PATH_RAW,dataname + '.csv');
    dfAppend = pd.read_csv(path,index_col=keys);

    if dfAppend.index.names[0]==u'secID' and filterSecID:
        dfAppend = dfAppend[dfAppend.index.map(lambda i:utils_stock.filterSecID(i[0]))\
                            .get_values()];
        
        pass;

    df = dfOrigin.append(dfAppend);
    df = df[~df.index.duplicated(keep='last')];
    df.to_csv(dstpath);
    
    pass;

def importdb(dataname,keys,filterSecID=True):
    dstpath = os.path.join(getdb(),dataname);
    path = os.path.join(config.LOCAL_PATH_RAW,dataname + '.csv');
    df = pd.read_csv(path,index_col=keys);

    if df.index.names[0]==u'secID' and filterSecID:
        df = df[df.index.map(lambda i:utils_stock.filterSecID(i[0])).get_values()];
        pass;

    df.to_csv(dstpath);

def getdf(name):
    return pd.read_csv(os.path.join(getdb(),name),index_col=config.DATA_NAMES[name]);

def getDecFactor(name):
    return pd.read_csv(os.path.join(getdb(),name),index_col=['secID','tradeDate']);

def completeFundETFConsGet():
    df = getdf('FundETFConsGet');
    dfMarket = getdf('MktEqudAdjAfGet');

    udtMarket = np.unique(dfMarket.index.get_level_values('tradeDate').values);
    dts = df.index.get_level_values('tradeDate').values;
    udtFund = np.unique(dts);
    minDt = np.min(dts);
    missDt = {dt for dt in udtMarket if dt not in udtFund and dt>=minDt};

    print(missDt);
    completeDtMap = dict();
    dfComp = df.copy();
    for dt in missDt:
        for i in range(20):
            preDt = utils_common.dtAdd(dt,-i);
            if preDt in udtFund:
                break;
            pass;
        if preDt not in udtFund:
            raise RuntimeError('cannot find previous date');
        addDf = df[dts==preDt];
        addDf.reset_index(inplace=True);
        addDf.loc[:,'tradeDate'] = dt;
        addDf.set_index(config.DATA_NAMES['FundETFConsGet'],inplace=True);

        dfComp = dfComp.append(addDf);
        pass;

    dfComp.to_csv(os.path.join(getdb(),'FundETFConsGet'));
    pass;

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

def forEachTradeDate(df):
    df.groupby('tradeDate');
    pass;
def save_df(df,name):
    dstpath = os.path.join(getdb(),name);
    df.to_csv(dstpath,float_format='%g');
    pass;

def getFeature(names):
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
    features = getFeature(featureNames);
    label = getLabel(labelName);

    df = label.join(features,how='inner');
    return df;
    

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

def getAllFeatureNames():
    names = set();
    files = glob.glob(getdb() + '/Fea*' );
    for f in files:
        with open(f) as fin:
            cols = fin.next().strip().split(',');
            names.update(cols);
            pass;
        pass;
    names.remove('secID');
    names.remove('tradeDate');
    return list(names);

def joinHS300(df):
    df300 = getdf('FundETFConsGet')[['quantity']];
    df300 = df300[df300.index.get_level_values('secID')=='510300.XSHG'];
    df300.reset_index(inplace=True);
    df300.drop('secID', axis=1, inplace=True);
    df300.rename(columns = {'consID':'secID'}, inplace=True);
    df300.set_index(['secID','tradeDate'],inplace=True);

    return df.join(df300,how='inner');

def joinTurnoverRank(df,num=500):
    dfRank = getFeature(['FeaLastTurnoverRank'])[0];
    dfRank = dfRank[dfRank['FeaLastTurnoverRank']<=500];
    df = df.join(dfRank,how='inner');
    df.drop('FeaLastTurnoverRank',axis=1,inplace=True);
    return df;
    
if __name__=='__main__':
    print(getAllFeatureNames());

    

