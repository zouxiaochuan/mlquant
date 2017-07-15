import config;
from config import dataio;
import bson.json_util

if __name__=='__main__':
    dataio.initdb();

    for dataname,keys in config.DATA_NAMES.items():
        print(dataname);
        dataio.importdb(dataname,keys);
        pass;
    pass;

