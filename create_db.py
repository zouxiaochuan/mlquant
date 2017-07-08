import config;
from config import dataio;
import bson.json_util

if __name__=='__main__':
    dataio.initdb();

    for dataname in config.DATA_NAMES:
        print(dataname['name']);
        dataio.importdb(dataname);
        pass;
    pass;

