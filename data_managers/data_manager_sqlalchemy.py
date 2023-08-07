import os
import time
import sqlite3
from typing import List
import base_classes
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy import (
    Column, Integer, Text, DateTime, UniqueConstraint, REAL, text,
    Index
)

DeclarativeBase = declarative_base()


class Tick(DeclarativeBase):
    __tablename__ = 'tb_tick'

    symbol = Column(Text, primary_key=True)
    price = Column(REAL, nullable=True)
    volume = Column(Integer, nullable=True)
    total_volume = Column(Integer, nullable=True)
    timestamp = Column(REAL, nullable=True)
    seq_num = Column(Integer, nullable=True)
    ask_price = Column(REAL, nullable=True)
    ask_size = Column(Integer, nullable=True)
    bid_price = Column(REAL, nullable=True)
    bid_size = Column(Integer, nullable=True)
    server_time = Column(Integer, nullable=True)

    __table_args__ = (
        Index('idx_tick_symbol_timestamp', symbol, timestamp.desc()),
        {})
    pass


class Bar(DeclarativeBase):
    __tablename__ = 'tb_bar'

    symbol = Column(Text, primary_key=True)
    timestamp = Column(REAL, primary_key=True)
    period = Column(Integer, primary_key=True)
    first = Column(REAL, nullable=True)
    last = Column(REAL, nullable=True)
    high = Column(REAL, nullable=True)
    low = Column(REAL, nullable=True)
    average = Column(REAL, nullable=True)
    volume = Column(Integer, nullable=True)
    total_volume = Column(Integer, nullable=True)

    __table_args__ = (
        Index('idx_bar_symbol_timestamp', symbol, timestamp.desc()),
        {})
    pass


class DataManagerSQLAlchemy(base_classes.DataManagerBase):
    def __init__(self, url: str):
        super().__init__()
        self.url = url

        self.init_connection()
        self.init_data()

        tick_columns = base_classes.DataTick.columns()
        bar_columns = base_classes.DataBar.columns()

        self.sql_insert_tick = '''
        INSERT INTO table_tick({0}) VALUES({1})
        '''.format(','.join(tick_columns),
                   ','.join([f':{c}' for c in tick_columns]))
        self.sql_insert_bar = '''
        INSERT INTO table_bar({0}) VALUES({1})
        '''.format(','.join(bar_columns),
                   ','.join([f':{c}' for c in bar_columns]))
        pass

    def init_connection(self):
        self.engine = create_engine(self.url, future=True)
        pass

    def init_data(self):
        DeclarativeBase.metadata.create_all(self.engine)
        pass

    def put_tick(self, tick: base_classes.DataTick):
        with self.engine.begin() as conn:
            conn.execute(
                self.sql_insert_tick,
                tick.data_dict()
            )
            conn.commit()
        pass

    def put_bars(self, bars: List[base_classes.DataBar]):
        with self.engine.begin() as conn:
            conn.execute(self.sql_insert_bar, [bar.data_dict() for bar in bars])
            conn.commit()
        pass
    pass
