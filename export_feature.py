from config import dataio;
import config;
import numpy as np;
import pandas as pd;
import sys;

if __name__=='__main__':
    df = dataio.getLabelAndFeature(config.LABEL,config.FEATURE_SELECT);
    df = df[df[config.LABEL]>-1];
    turnoverFilter = dataio.getTurnoverRankFilter();
    maxContinousCloseDayFilter = dataio.getMaxContinousCloseDayFilter();
    secFilter = turnoverFilter & maxContinousCloseDayFilter;
    idxFilter = np.asarray([True if st in secFilter else False \
                            for st in df.index]);

    df.rename(columns = {config.LABEL:'label'}, inplace=True);
    #df = df[idxFilter]

    df.to_csv(sys.argv[1]);
    pass;
