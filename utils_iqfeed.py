import asyncio
from datetime import datetime
import pytz
from io import BytesIO
import pandas as pd
from typing import Type, Tuple
import socket


DEFAULT_HOST = 'localhost'
DEFAULT_PORT = 9100


async def get_tick_dt_(
        symbol: str,
        dt: str) -> pd.DataFrame:
    current_dt = datetime.now().astimezone(pytz.timezone('US/Eastern'))
    current_dt = current_dt.replace(tzinfo=None)
    dt_ = datetime.strptime(dt, '%Y-%m-%d')
    num_days = (current_dt - dt_).days + 1

    if num_days < 1:
        raise RuntimeError('num_days less than 1: ' + str(num_days))

    reader: asyncio.StreamReader
    writer: asyncio.StreamWriter
    reader, writer = await asyncio.open_connection(
        DEFAULT_HOST, DEFAULT_PORT)

    writer.write('HTD,{Symbol},{MaxDays},,,,,\r\n'.format(
        Symbol=symbol, MaxDays=num_days).encode('utf8'))

    await writer.drain()

    outfile = BytesIO()
    while True:
        line: bytes
        line = await reader.readline()
        if line.startswith(b'E'):
            raise RuntimeError(line.decode('utf8'))
            pass

        if b'!ENDMSG!' in line:
            break

        line = line[:-3] + b'\r\n'
        outfile.write(line)
        pass

    writer.close()
    await writer.wait_closed()

    df = pd.read_csv(BytesIO(outfile.getvalue()), header=None, index_col=None)

    return df
    pass


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


def get_tick_dt(
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
    pass
