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


def get_conn() -> Tuple[asyncio.StreamReader, asyncio.StreamWriter]:
    sock: socket.socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((DEFAULT_HOST, DEFAULT_PORT))
    return sock


def get_df(
        command: str,
        sock: socket.socket) -> Type[pd.DataFrame]:

    sock.sendall(command)

    outfile = BytesIO()
    for line in sock.makefile(mode='rb'):
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

    df = pd.read_csv(BytesIO(outfile.getvalue()), header=None, index_col=None)

    return df


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
        EndTime=dt+' 170000').encode('ascii')

    return get_df(
        command,
        sock)



