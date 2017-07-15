
import dataio_mongodb as dataio;
import pandas as pd;
import time;

if __name__=='__main__':
    #print(dataio.getdb()['MktEqudAdjAfGet'].distinct('secID'));
    #df = pd.read_csv('../raw/MktEqudAdjAfGet.csv',index_col=['secID','tradeDate']);
    s = time.time();
    #df.to_hdf('x.hdf','x');
    #df = pd.read_hdf('x.hdf','x');
    #df.to_hdf('x2.hdf');

    import BaseLabelEveryNDayTrade;
    x = BaseLabelEveryNDayTrade.BaseLabelEveryNDayTrade(10);
    x.extract();

