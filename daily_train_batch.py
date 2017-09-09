import daily_train;
import sys;
import utils_common;
import os;
import config;
from config import dataio;

def main(dtStart,dtEnd,savePath):
    label,feature,dts = daily_train.loadData();
    
    dt = dtStart;

    while dt<=dtEnd:
        filename = 'xgb_' + dt;
        print(dt);
        daily_train.daily_train(feature,label,dts,dt,os.path.join(savePath,filename));
        dt = utils_common.dtAdd(dt,1);
        pass;
    pass;

if __name__=='__main__':
    dtStart = sys.argv[1];
    dtEnd = sys.argv[2];
    savePath = sys.argv[3];
    main(dtStart,dtEnd,savePath);
    pass;
