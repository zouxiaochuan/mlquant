import tushare as ts;
from config import dataio;
import config;
import utils_common;
import os;

gTicker2SecID = dataio.getStockCode2SecID();

def MarginDetails(tradeDate):
    selectedCol = ['stockCode','opDate','rzye','rzmre','rqyl','rqmcl'];
    
    df = ts.sh_margin_details(start=tradeDate,end=tradeDate);
    if df.shape[0]>0:
        df = df[selectedCol];
        pass;
    
    dfSz = ts.sz_margin_details(date=tradeDate);
    if dfSz.shape[0]>0:
        df = df.append(dfSz[selectedCol]);
        pass;

    if df.shape[0]==0:
        return df;
    df.rename(columns = {'opDate':'tradeDate'}, inplace=True);
    
    df['secID'] = df['stockCode'].apply(lambda x: gTicker2SecID[x] if x in gTicker2SecID else None);
    df = df[df['secID'].map(lambda x:x is not None)];
    df.drop('stockCode',axis=1,inplace=True);
    #df.set_index(['secID','tradeDate'],inplace=True);
    return df;

DATA_NAMES = ['MarginDetails'];

def download(startDt,endDt):
    dt = startDt;

    filenames = [os.path.join(config.LOCAL_PATH_RAW,dn + '.csv') for dn in DATA_NAMES];
    cntDt = 0;
    lastMon = '';
    while dt<=endDt:
        for dataname,filename in zip(DATA_NAMES,filenames):
            if dt[:7]!=lastMon:
                lastMon = dt[:7];
                print(lastMon);
                pass;
            
            df = eval(dataname + '(dt)');

            if df.shape[0]>0:
                if cntDt>0:
                    fmode = 'a';
                    wheader = False;
                else:
                    fmode = 'w';
                    wheader = True;
                    pass;
                
                df.to_csv(filename,mode=fmode,header=wheader,index=False);
                cntDt+=1;
                pass;
            pass;
        dt = utils_common.dtAdd(dt,1);
        pass;
    pass;

if __name__=='__main__':
    #print(margin_details('2017-11-01'));
    download('2008-01-01',utils_common.getCurrentDt());
    pass;
