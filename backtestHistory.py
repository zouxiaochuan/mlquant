import sys;
from config import dataio;
import config;
import backtest;
import utils_common;
import pandas as pd;
import numpy as np;
import os;
import utils_server;

def main(strategy, startDt,endDt,initMoney):
    decFactor = utils_server.getDecFactors(startDt,endDt);
    backtest.backtest(initMoney,startDt,endDt,strategy,decFactor);
    pass;

if __name__=='__main__':
    strategy = utils_common.getStrategy(sys.argv[1]);
    startDt = sys.argv[2];
    endDt = sys.argv[3];
    initMoney = float(sys.argv[4]);

    main(strategy,startDt,endDt,initMoney);
    pass;
