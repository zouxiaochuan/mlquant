import utils_tiger
import utils_sqlite
import utils_log
import pandas as pd
import utils_common
import sqlite3
from typing import Type
import time
import logging

logger = utils_log.console


def download_stock_ticks(
        symbols: list,
        conn: Type[sqlite3.Connection]):

    for ss in (symbols[i:i+50] for i in range(0, len(symbols), 50)):
        df: pd.DataFrame = utils_tiger.get_trade_ticks(
            ss,
            limit=1000)

        if not isinstance(df, pd.DataFrame):
            continue

        df['dt'] = df['time'].map(utils_common.ms2dt_us_market)

        logger.debug('download stock ticks: ' + str(df.shape[0]))

        utils_sqlite.insert_data(df, 'stock_ticks', conn)
        pass
    pass


def get_future_tick_last_index(
        symbol: str,
        dt: str,
        conn: sqlite3.Connection):
    row = conn.execute(
        '''
        select max(idx) from future_ticks
        where identifier=? and dt=?
        ''',
        (symbol, dt)).fetchone()

    if row is None or row[0] is None:
        return 0
    else:
        return row[0]
    pass


def download_future_ticks(
        symbols: list,
        conn: Type[sqlite3.Connection]):

    cdt = utils_common.get_current_dt_us()
    print(cdt)

    for s in symbols:
        last_index = get_future_tick_last_index(
            s,
            cdt,
            conn)

        begin_index = max(0, last_index - 500)
        end_index = begin_index + 1000

        logger.debug('future: {0}, begin_index: {1}, end_index: {2}'.format(
            s, begin_index, end_index))

        df: pd.DataFrame = utils_tiger.get_future_trade_ticks(
            s,
            begin_index,
            end_index,
            end_index - begin_index)

        if not isinstance(df, pd.DataFrame):
            continue

        df['dt'] = df['time'].map(utils_common.ms2dt_us_market)

        logger.debug('download future tick:' + str(df.shape[0]))

        utils_sqlite.insert_data(
            df,
            'future_ticks',
            conn)
        pass
    pass


def download_loop():
    stocks = utils_common.file2list('stocks.txt')
    futures = utils_common.file2list('futures.txt')
    conn = sqlite3.connect('sqlite.db')
    config = utils_common.load_json('./tiger.json')
    utils_tiger.set_config(config)

    while True:
        download_stock_ticks(
            stocks, conn)
        download_future_ticks(
            futures, conn)
        time.sleep(1)
        pass
    pass


if __name__ == '__main__':
    utils_log.setLevel(logging.DEBUG)
    download_loop()
    pass
