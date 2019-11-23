import sys
import utils_common
import utils_iqfeed
import os
import time


if __name__ == '__main__':
    rootpath = sys.argv[1]
    start_dt = sys.argv[2]
    end_dt = sys.argv[3]

    symbols = []

    stocks = utils_common.file2list(os.path.join(rootpath, 'stocks.txt'))
    futures = utils_common.file2list(os.path.join(rootpath, 'futures.txt'))

    symbols = stocks + futures
    is_futures = [False for _ in stocks] + [True for _ in futures]

    dt = end_dt
    conn = utils_iqfeed.get_conn()

    while dt >= start_dt:
        for symbol,is_future in zip(symbols, is_futures):
            filedir = os.path.join(rootpath, symbol)
            if not os.path.exists(filedir):
                os.makedirs(filedir)
                time.sleep(1)
                pass

            filepath = os.path.join(rootpath, symbol, dt+'.csv')
            print(filepath)
            
            if os.path.exists(filepath):
                continue

            if not is_future:
                df = utils_iqfeed.get_stock_tick_dt(symbol, dt, conn)
            else:
                df = utils_iqfeed.get_future_tick_dt(symbol, dt, conn)
                pass

            if df is None:
                continue
            
            df.to_csv(filepath, header=False, index=False)
            pass

        dt = utils_common.dt_add(dt, -1)
        pass
    pass
