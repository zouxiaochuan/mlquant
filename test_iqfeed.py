import utils_iqfeed
import pandas as pd
import sys

if __name__ == '__main__':
    df: pd.DataFrame
    sock = utils_iqfeed.get_conn()

    df = utils_iqfeed.get_stock_bar_dt(
        'QCL#',
        '2020-04-22',
        60,
        sock)

    # df = utils_iqfeed.get_daily(
    #     'QCLK20',
    #     '2008-01-01',
    #     '2020-05-01',
    #     sock)
    

    # cmd = 'CEO,SPX,cp,,4,0,,,,\r\n'
    # sock.sendall(cmd.encode('ascii'))
    # 
    # print(sock.makefile().readline())
    # exit(1)
    print(df)
    df.to_csv('x.csv', header=False, index=False)
    sock.sendall(b'S,DISCONNECT\r\n')
    sock.close()
    pass
