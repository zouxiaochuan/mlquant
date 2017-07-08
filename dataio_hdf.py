import utils_io;
import pandas as pd;
import config;
import os;
import pandas as pd;
import utils_stock;
import utils_parallel;
import utils_common;

def initdb():
    pass;

def getdb():
    return config.LOCAL_PATH_HDF;

def importdb(dataname):
    dstpath = os.path.join(getdb(),dataname['name']);
    path = os.path.join(config.LOCAL_PATH_RAW,dataname['name'] + '.csv');
    df = pd.read_csv(path,index_col=dataname['key']);
    utils_io.write_hdf(dstpath,df);

def forEachSecIDInternal(param):
    secID,df,func = param;
    recs = df.sort_values(['tradeDate']).to_dict('records');

    return func(secID,recs);
    
def forEachSecID(tablename,columnNames,func):
    cols = ['secID','tradeDate'] + columnNames;
    
    print('begin read');
    path = os.path.join(getdb(),tablename)
    print(path);
    df = pd.read_hdf(path,'data',columns=cols);
    print('end read');
    secIDs = df['secID'].unique();
    secIDs = [secID for secID in secIDs if utils_stock.filterSecID(secID)];

    return utils_parallel.parallel(forEachSecIDInternal,
                                   [(secID,df[df['secID']==secID],func) for secID in secIDs]);
    pass;

def save_df(df,name):
    utils_io.write_hdf(dstpath,df);

if __name__=='__main__':
    pass;

