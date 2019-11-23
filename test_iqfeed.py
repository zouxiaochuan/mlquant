import utils_iqfeed
import pandas as pd


if __name__ == '__main__':
    df: pd.DataFrame
    sock = utils_iqfeed.get_conn()

    df = utils_iqfeed.get_future_tick_dt(
        'QNG#',
        '2019-11-22',
        sock)

    print(df.head(10))
    df.to_csv('x.csv', header=False, index=False)
    sock.close()
    pass
