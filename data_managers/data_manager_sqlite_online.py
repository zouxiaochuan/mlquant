import os
import time
import sqlite3
from typing import List
import base_classes


class DataManagerSqliteOnline(base_classes.DataManagerBase):
    def __init__(self, data_path):
        super().__init__()
        self._data_path = data_path
        os.makedirs(data_path, exist_ok=True)

        self._path_tick = os.path.join(self._data_path, 'table_tick.sqlite')
        self._path_bar = os.path.join(self._data_path, 'table_bar.sqlite')

        self.init_connection()
        self.init_data()

        tick_columns = base_classes.DataTick.columns()
        bar_columns = base_classes.DataBar.columns()

        self._sql_insert_tick = '''
        INSERT INTO table_tick({0}) VALUES({1})
        '''.format(','.join(tick_columns),
                   ','.join(['?' for _ in tick_columns]))
        self._sql_insert_bar = '''
        INSERT INTO table_bar({0}) VALUES({1})
        '''.format(','.join(bar_columns),
                   ','.join(['?' for _ in bar_columns]))
        pass

    def init_connection(self):
        self._conn_tick = sqlite3.connect(self._path_tick)
        self._conn_bar = sqlite3.connect(self._path_bar)
        pass

    def init_data(self):
        sqlcmd = '''
        CREATE TABLE IF NOT EXISTS table_tick(
          symbol TEXT,
          timestamp BIGINT,
          seq_num BIGINT,
          price REAL,
          volume BIGINT,
          total_volume BIGINT,
          ask_price REAL,
          ask_size BIGINT,
          bid_price REAL,
          bid_size BIGINT,
          server_time BIGINT,
          UNIQUE(symbol, timestamp, seq_num)
        );
        '''
        self._conn_tick.execute(sqlcmd)
        self._conn_tick.commit()

        sqlcmd = '''
        CREATE TABLE IF NOT EXISTS table_bar(
          symbol TEXT,
          timestamp BIGINT,
          period BIGINT,
          first REAL,
          last REAL,
          high REAL,
          low REAL,
          average REAL,
          volume BIGINT,
          total_volume BIGINT,
          UNIQUE(symbol, timestamp, period)
        );
        '''
        self._conn_bar.execute(sqlcmd)
        self._conn_bar.commit()
        pass

    def put_tick(self, tick: base_classes.DataTick):
        self._conn_tick.execute(
            self._sql_insert_tick,
            tick.data())
        self._conn_tick.commit()
        pass

    def put_bars(self, bars: List[base_classes.DataBar]):
        self._conn_bar.executemany(
            self._sql_insert_bar,
            (bar.data() for bar in bars))
        self._conn_bar.commit()
        pass
    pass
