# -*- coding: utf-8 -*-

import sys;
sys.path.append('..');
import easytrader;
import easyquotation;
import time;
from apscheduler.schedulers.background import BackgroundScheduler;
import urllib.request as urllib2;
import json;
import pandas as pd;
import utils_common;

class YHClientTrader(object):
    def __init__(self,username,passwd,exe_path):
        self.username_ = username;
        self.password_ = passwd;
        self.exePath_ = exe_path;
        self.quotation_ = easyquotation.use('sina');
        
    def __enter__(self):
        self.user_ = easytrader.use('yh_client');
        self.user_.prepare(user=self.username_, password=self.password_, exe_path=self.exePath_);
        time.sleep(2);
        return self;

    def __exit__(self, exc_type, exc_value, traceback):
        self.user_.exit();
        pass;

    def getRecords(self,secList):
        if len(secList)==0:
            return [];

        recs = self.quotation_.stocks(secList);
        while secList[0] not in recs:
            time.sleep(2);
            recs = self.quotation_.stocks(secList);
            pass;
        return recs;
    
    def getMarketValue(self):
        mkv =  self.user_.balance[0]['总资产'];
        time.sleep(2);
        return mkv;

    def getPrices(self,secList):
        recs = self.getRecords(secList);
        
        return [recs[sec]['now'] for sec in secList];
        pass;
    
    def getPrice(self,secID):
        return self.getPrices([secID])[0];
    
    def getPreClosePrice(self,secID):
        return self.getRecords([secID])[secID]['close'];
    
    def buyList(self,alist):
        print(alist);
        sucList = [];
        secList = [i[0] for i in alist];
        prices = self.getPrices(secList);
        for i,(secID,amount) in enumerate(alist):
            price = self.roundPrice(prices[i]+0.1);
            self.user_.buy(secID,price=price,amount=amount);
            time.sleep(1);
            sucList.append((secID,amount));
            pass;
        pass;

    def roundPrice(self,price):
        return (int(price*100))*0.01;
    
    def sellSec(self,secSet):
        for rec in self.user_.position:
            secID = rec['证券代码'];
            if secID not in secSet:
                continue;
            available = rec['可用余额'];
            price = rec['参考市价']-0.1;
            price = self.roundPrice(max(price,(self.getPreClosePrice(secID)*0.9)));
            if available>0:
                self.user_.sell(secID,price=price,amount=available);
                time.sleep(1);
                pass;
            pass;
        pass;

    def getAvailable(self):
        ret = [];
        for rec in self.user_.position:
            available = rec['可用余额'];
            if available>0:
                pos = dict();
                pos['secID'] = rec['证券代码'];
                pos['amount'] = available;
                pos['price'] = rec['参考市价'];
                ret.append(pos);
                pass;
            pass;
        time.sleep(2);
        return ret;

    def getBuyFee(self):
        return 0.001;
    pass;

strategy = None;

def getDecFactor():
    jsonstr = urllib2.urlopen('http://47.52.101.241:18000/queryScore',timeout=10).read();
    records = json.loads(jsonstr)['data'];
    for rec in records:
        rec['secID'] = rec['secID'].split('.')[0];
        pass;
    dfDec = pd.DataFrame().from_records(records);
    dfDec.drop('tradeDate', axis=1, inplace=True);
    dfDec = dfDec[['secID','score']];
    return dfDec;

def getTrader():
    return YHClientTrader('225300024455','842613', 'D:\ext_c\中国银河证券双子星3.2\Binarystar.exe');

def onOpen():
    global strategy;

    with getTrader() as trader:
        dfDec = getDecFactor();
        strategy.handle(utils_common.getCurrentDt(),'open',trader,dfDec);
        pass;
    pass;

def onClose():
    global strategy;

    with getTrader() as trader:
        defDec = getDecFactor();
        strategy.handle(utils_common.getCurrentDt(),'close',trader,dfDec);
        pass;
    pass;

def main():
    scheduler = BackgroundScheduler();
    scheduler.add_job(onOpen,'cron',hour=9, minute=30);
    scheduler.add_job(onClose,'cron',hour=14, minute=58);

    scheduler.start();

    while True:
        time.sleep(1);
        pass;

    scheduler.shutdown();
    pass;

if __name__=='__main__':
    strategy = utils_common.getStrategy(sys.argv[1]);
    main();
    pass;

