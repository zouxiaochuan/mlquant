import sys
import utils_common
import utils_iqfeed
import os
import time
from datetime import datetime
import socket


if __name__ == '__main__':
    rootpath = sys.argv[1]
    end_dt = sys.argv[2]
    num_day = int(sys.argv[3])

    start_dt = utils_common.dt_add(end_dt, -num_day)

    symbols = []

    stocks = utils_common.file2list(os.path.join(rootpath, 'stocks.txt'))
    futures = utils_common.file2list(os.path.join(rootpath, 'futures.txt'))

    symbols = stocks + futures
    is_futures = [False for _ in stocks] + [True for _ in futures]

    dt = end_dt
    conn = utils_iqfeed.get_conn()

    while dt >= start_dt:
        if datetime.strptime(dt, '%Y-%m-%d').weekday() < 5:
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

                try_num = 3
                for itry in range(try_num):
                    if itry > 0:
                        print('retry number: {0}'.format(itry))
                        pass
                    try:
                        if not is_future:
                            df = utils_iqfeed.get_stock_tick_dt(symbol, dt, conn)
                        else:
                            df = utils_iqfeed.get_future_tick_dt(symbol, dt, conn)
                            pass
                        break
                    except (RuntimeError, socket.timeout) as e:
                        if itry == (try_num - 1):
                            raise e

                        if isinstance(e, socket.timeout):
                            conn.close()
                            conn = utils_iqfeed.get_conn()
                            continue

                        if isinstance(e, RuntimeError):
                            msg = str(e)
                            if 'Unknown Server Error code 0' in msg:
                                continue
                            pass

                        raise e
                    pass

                
                if df is None:
                    continue
                
                df.to_csv(filepath, header=False, index=False)
                pass
            pass

        dt = utils_common.dt_add(dt, -1)
        pass
    pass
