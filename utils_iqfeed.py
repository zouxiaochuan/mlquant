import asyncio
from datetime import datetime
import pytz
from io import BytesIO
import pandas as pd
from typing import Type, Tuple
import socket
import utils_common


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 9100


def get_conn() -> Type[socket.socket]:
    sock: socket.socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((DEFAULT_HOST, DEFAULT_PORT))
    sock.settimeout(60)
    return sock


def get_df(
        command: str,
        sock: socket.socket) -> Type[pd.DataFrame]:

    sock.sendall(command)

    outfile = BytesIO()
    with sock.makefile(mode='rb') as fin:
        for line in fin:
            if line.startswith(b'E'):
                if b'!NO_DATA!' in line:
                    return None
        
                raise RuntimeError(line.decode('utf8'))
                pass
        
            if b'!ENDMSG!' in line:
                break
        
            line = line[:-3] + b'\r\n'
            outfile.write(line)
            pass
        pass

    df = pd.read_csv(BytesIO(outfile.getvalue()), header=None, index_col=None)

    return df


def get_stock_bar_dt(
        symbol: str,
        dt: str,
        interval: int,
        sock: socket.socket) -> Type[pd.DataFrame]:
    dt = dt.replace('-', '')
    command = 'HIT,{Symbol},{Interval},{BeginTime},{EndTime}\r\n'.format(
        Symbol=symbol, Interval=interval, BeginTime=dt+' 000000',
        EndTime=dt+' 235959').encode('ascii')

    df = get_df(
        command,
        sock)

    if df is None:
        return df
    
    df.columns = ['timestamp', 'high', 'low', 'open', 'close', 'total_vol', 'vol']

    return df
    pass


def get_stock_tick_dt(
        symbol: str,
        dt: str,
        sock: socket.socket) -> Type[pd.DataFrame]:

    dt = dt.replace('-', '')
    command = 'HTT,{Symbol},{BeginTime},{EndTime}\r\n'.format(
        Symbol=symbol, BeginTime=dt+' 000000',
        EndTime=dt+' 235959').encode('ascii')

    return get_df(
        command,
        sock)


def get_future_tick_dt(
        symbol: str,
        dt: str,
        sock: socket.socket) -> Type[pd.DataFrame]:

    pre_dt = utils_common.dt_add(dt, -1)

    dt = dt.replace('-', '')
    pre_dt = pre_dt.replace('-', '')

    command = 'HTT,{Symbol},{BeginTime},{EndTime}\r\n'.format(
        Symbol=symbol, BeginTime=pre_dt+' 180000',
        EndTime=dt+' 170500').encode('ascii')

    return get_df(
        command,
        sock)


def get_daily(
        symbol: str,
        dt_start: str,
        dt_end: str,
        sock: socket.socket) -> Type[pd.DataFrame]:

    command = 'HDT,{symbol},{begin_date},{end_date},,,,\r\n'.format(
        symbol=symbol, begin_date=dt_start.replace('-', ''),
        end_date=dt_end.replace('-', '')).encode('ascii')

    return get_df(command, sock)
