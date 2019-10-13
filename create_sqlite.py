import sqlite3

# stock
# symbol,index,time,price,volume,direction
# UGAZ,4698,1570632712300,13.47,154,+
# UGAZ,4699,1570632713100,13.477,500,+

# future
# identifier,index,time,price,volume
# NGmain,5001,1570800029000,2.219,2
# NGmain,5002,1570800035000,2.218,1
# NGmain,5003,1570800036000,2.218,2


def create_sqlite(dbfile):
    conn = sqlite3.connect(dbfile)
    conn.executescript('''
    DROP TABLE IF EXISTS stock_ticks;
    CREATE TABLE stock_ticks(
      symbol TEXT,
      idx INTEGER,
      time INTEGER,
      price REAL,
      volume INTEGER,
      direction TEXT,
      dt TEXT,
      UNIQUE(dt, symbol, idx)
    );
    CREATE INDEX index_stock_ticks ON
      stock_ticks(dt, symbol, idx)
    ''')
    conn.commit()
    conn.executescript('''
    DROP TABLE IF EXISTS future_ticks;
    CREATE TABLE future_ticks(
      identifier TEXT,
      idx INTEGER,
      time INTEGER,
      price REAL,
      volume INTEGER,
      dt TEXT,
      UNIQUE(dt, identifier, idx)
    );
    CREATE INDEX index_future_ticks ON
      future_ticks(dt, identifier, idx)
    ''')
    conn.commit()
    pass


if __name__ == '__main__':
    create_sqlite('sqlite.db')
    pass
