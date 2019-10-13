import sqlite3
from typing import Type
import pandas as pd


def insert_data(
        df: Type[pd.DataFrame],
        table: str,
        conn: Type[sqlite3.Connection]):

    num_cols = df.shape[1]
    conn.executemany(
        '''
    INSERT OR REPLACE INTO {1}
      VALUES({0});
        '''.format(','.join(['?' for _ in range(num_cols)]), table),
        (tuple(r) for r in df.values)
    )
    conn.commit()
    pass
