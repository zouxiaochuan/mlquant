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


def create_ticks(dbfile):
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


# symbol           time  price  avg_price  pre_close  volume trading_session
# UGAZ  1571040000000  13.11   13.11000      13.11       0      pre_market
# UGAZ  1571040060000  13.11   13.11000      13.11       0      pre_market
# UGAZ  1571040120000  13.67   13.67000      13.11     139      pre_market
# UGAZ  1571040180000  13.64   13.64366      13.11    1000      pre_market
# UGAZ  1571040240000  13.65   13.64483      13.11     257      pre_market
# UGAZ  1571040300000  13.62   13.64096      13.11     456      pre_market

def create_stock_minutes(dbfile):
    conn = sqlite3.connect(dbfile)
    conn.executescript('''
    DROP TABLE IF EXISTS stock_minutes;
    CREATE TABLE stock_minutes(
      symbol TEXT,
      time INTEGER,
      price REAL,
      avg_price REAL,
      pre_close REAL,
      volume INTEGER,
      trading_session TEXT,
      dt TEXT,
      UNIQUE(symbol, time)
    );
    CREATE INDEX index_stock_minutes ON
      stock_minutes(symbol, time)
    ''')
    conn.commit()
    pass


# identifier,time,latest_time,open,high,low,close,settlement,volume,open_interest
# NGmain,1571198580000,1571198588000,2.339,2.339,2.339,2.339,0.0,1,0
# NGmain,1571198520000,1571198561000,2.34,2.34,2.34,2.34,0.0,3,0

def create_future_minutes(dbfile):
    conn = sqlite3.connect(dbfile)
    conn.executescript('''
    DROP TABLE IF EXISTS future_minutes;
    CREATE TABLE future_minutes(
      identifier TEXT,
      time INTEGER,
      latest_time INTEGER,
      open REAL,
      high REAL,
      low REAL,
      close REAL,
      settlement REAL,
      volume INTEGER,
      open_interest INTEGER,
      dt TEXT,
      UNIQUE(identifier, time)
    );
    CREATE INDEX index_future_minutes ON
      future_minutes(identifier, time)
    ''')
    conn.commit()
    pass


if __name__ == '__main__':
    create_future_minutes('sqlite.db')
    pass
