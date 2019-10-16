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


def download_future_minutes(
        symbols: list,
        conn: Type[sqlite3.Connection]):

    for ss in (symbols[i:i+50] for i in range(0, len(symbols), 50)):
        df: pd.DataFrame = utils_tiger.get_future_bars_minute(
            ss)

        if not isinstance(df, pd.DataFrame):
            continue

        df['dt'] = df['time'].map(utils_common.ms2dt_us_future)

        logger.debug('download future minutes: ' + str(df.shape[0]))

        utils_sqlite.insert_data(df, 'future_minutes', conn)
        pass
    pass


def download_loop():
    stocks = utils_common.file2list('stocks.txt')
    futures = utils_common.file2list('futures.txt')
    conn = sqlite3.connect('sqlite.db')
    config = utils_common.load_json('./tiger.json')
    utils_tiger.set_config(config)

    while True:
        download_future_minutes(
            futures, conn)
        time.sleep(1)
        pass
    pass


if __name__ == '__main__':
    utils_log.setLevel(logging.DEBUG)
    download_loop()
    pass
