import config;
from config import dataio;
import bson.json_util

if __name__=='__main__':
    dataio.initdb();

    datanames = config.DATA_NAMES;
    datanames = {'MarginDetails': ['secID','tradeDate']};
    for dataname,keys in datanames.items():
        print(dataname);
        if dataname=='MktFunddAdjGet' or dataname=='FundETFConsGet':
            flt = False;
        else:
            flt = True;
            pass;
        dataio.importdb(dataname,keys,filterSecID=flt);
        pass;
    pass;

