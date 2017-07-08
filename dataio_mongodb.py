import pymongo;
import config;
import pandas as pd;
import os;
import utils_stock;
import utils_parallel;

def initMktEqudGet(db):
    db['MktEqudGet'].create_index([('secID', pymongo.ASCENDING),
                                   ('tradeDate',pymongo.ASCENDING)],
                                  unique=True);
    pass;

def initMktEquFlowGet(db):
    db['MktEquFlowGet'].create_index([('secID',pymongo.ASCENDING),
                                      ('tradeDate',pymongo.ASCENDING)],unique=True);
    pass;

def initMktIdxdGet(db):
    db['MktIdxdGet'].create_index([('tradeDate',pymongo.ASCENDING)],unique=True);
    pass;

def initSecSTGet(db):
    db['SecSTGet'].create_index([('secID',pymongo.ASCENDING),
                                 ('tradeDate',pymongo.ASCENDING)],unique=True);
    pass;

def initMktEquFlowOrderGet(db):
    db['MktEquFlowOrderGet'].create_index([('secID',pymongo.ASCENDING),
                                           ('tradeDate',pymongo.ASCENDING)],unique=True);
    pass;

def initEqudAdjAfGet(db):
    db['MktEqudAdjAfGet'].create_index([('secID',pymongo.ASCENDING),
                                        ('tradeDate',pymongo.ASCENDING)],unique=True);
    pass;

def getdb():
    db = pymongo.MongoClient(config.CONN_STR)[config.DB_STR];
    return db;

def getclient():
    return pymongo.MongoClient(config.CONN_STR);

def initdb():
    client = getclient();
    client.drop_database(config.DB_STR);
    
    db = getdb();
    for dataname in config.DATA_NAMES:
        db[dataname['name']].create_index([(i,pymongo.ASCENDING) for i in dataname['key']],
                                          unique=True);
        pass;

    #custom indices
    pass;


def updateRecords(table,recs,keynames):
    for i,rec in enumerate(recs):
        table.update(
            {k:rec[k] for k in keynames},
            rec,
            upsert=True
        );

        if i%100000==0:
            print(i);
        pass;
    pass;

def importdb(dataname):
    db = getdb();
    path = os.path.join(config.LOCAL_PATH_RAW,dataname['name'] + '.csv');
    data = pd.read_csv(path).to_dict(orient='records');
    updateRecords(db[dataname['name']],data,dataname['key']);
    pass;

def forEachSecIDInternal(param):
    secID,tablename,func = param;

    db = getdb();
    recs = list(db[tablename].find({'secID':secID}).sort('tradeDate'));
    db.client.close();
    return func(secID,recs);
        
def forEachSecID(tablename,func):
    db = getdb();
    secIDs = db[tablename].distinct('secID');
    print(len(secIDs));
    secIDs = [secID for secID in secIDs if utils_stock.filterSecID(secID)];

    return utils_parallel.parallel_debug(forEachSecIDInternal,
                                   [(secID,tablename,func) for secID in secIDs]);
