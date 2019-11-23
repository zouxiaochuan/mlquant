import sys
import utils_common
import utils_iqfeed
import os
import time


if __name__ == '__main__':
    start_dt = sys.argv[1]
    end_dt = sys.argv[2]

    symbols = []

    with open('symbols.txt') as fin:
        for line in fin:
            symbols.append(line.strip())
            pass
        pass

    dt = end_dt
    conn = utils_iqfeed.get_conn()

    while dt >= start_dt:
        for symbol in symbols:
            if not os.path.exists(symbol):
                os.makedirs(symbol)
                time.sleep(1)
                pass

            filepath = os.path.join(symbol, dt+'.csv')
            print(filepath)
            
            if os.path.exists(filepath):
                continue

            df = utils_iqfeed.get_tick_dt(symbol, dt, conn)

            if df is None:
                continue
            
            df.to_csv(filepath, header=False, index=False)
            pass

        dt = utils_common.dt_add(dt, -1)
        pass
    pass
