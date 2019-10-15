from typing import Type
import time
import tigeropen.common.consts as tiger_consts
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.push.push_client import PushClient
from tigeropen.common.util.signature_utils import read_private_key

import utils_common

g_config = None
g_quote_client = None


def call_api(func, time_limit, retry=0):
    itry = 0
    while True:
        try:
            result = func()
            time.sleep(time_limit)
            break
        except Exception as e:
            if itry < retry:
                itry += 1
            else:
                raise e
            pass
        pass
    return result


def get_client_config(config: dict) -> Type[TigerOpenClientConfig]:
    client_config = TigerOpenClientConfig()
    client_config.private_key = read_private_key(config['tiger_private_key'])
    client_config.tiger_id = config['tiger_id']
    client_config.account = config['tiger_account']
    client_config.standard_account = config.get('tiger_standard_account')
    client_config.paper_account = config['tiger_paper_account']
    client_config.language = tiger_consts.Language.zh_CN
    return client_config


def get_quote_client(config: dict) -> Type[QuoteClient]:
    return QuoteClient(get_client_config(config))


def set_config(config: dict):
    global g_config, g_quote_client
    g_config = config

    g_quote_client = get_quote_client(config)


def get_push_client(config: dict) -> Type[PushClient]:
    client_config = get_client_config(config)
    protocol, host, port = client_config.socket_host_port
    push_client = PushClient(host, port, use_ssl=(protocol == 'ssl'))

    push_client.connect(client_config.tiger_id, client_config.private_key)
    return push_client


def get_bars(
        quote_client: QuoteClient,
        symbols: list,
        begin_time: int,
        end_time: int):

    def func(): return g_quote_client.get_bars(
            symbols)
    return quote_client.get_bars(
        symbols=symbols,
        period=tiger_consts.BarPeriod.ONE_MINUTE,
        begin_time=begin_time,
        end_time=end_time,
        right=tiger_consts.QuoteRight.BR,
        limit=600)


def get_bars_minute_dt(
        quote_client: QuoteClient,
        symbols: list,
        dt: str):
    ms = utils_common.dt2ms(dt)
    start = ms + 12 * 60 * 60 * 1000
    end = ms + 36 * 60 * 60 * 1000

    return quote_client.get_bars(
        symbols=symbols,
        period=tiger_consts.BarPeriod.ONE_MINUTE,
        begin_time=start,
        end_time=end,
        right=tiger_consts.QuoteRight.BR,
        limit=600)


def get_timeline(
        symbols: list,
        begin_time: int = -1):

    def func(): return g_quote_client.get_timeline(
            symbols, include_hour_trading=True,
            begin_time=begin_time)

    return call_api(func, 0.5, 0)


def get_bars_minute_month(
        quote_client: QuoteClient,
        symbols: list,
        dt: str):
    ms = utils_common.dt2ms(dt)
    start = ms + (12-31*24) * 60 * 60 * 1000
    end = ms + 36 * 60 * 60 * 1000

    print(start)
    print(end)

    return quote_client.get_bars(
        symbols=symbols,
        period=tiger_consts.BarPeriod.ONE_MINUTE,
        begin_time=start,
        end_time=end,
        right=tiger_consts.QuoteRight.BR,
        limit=60000)


def get_trade_ticks(
        symbols: list,
        limit: int):

    def func(): return g_quote_client.get_trade_ticks(
            symbols, begin_index=None, end_index=None, limit=limit)

    return call_api(func, 0.5, 0)


def get_future_trade_ticks(
        symbol: str,
        begin_index: int,
        end_index: int,
        limit: int):

    def func(): return g_quote_client.get_future_trade_ticks(
            symbol, begin_index=begin_index, end_index=end_index,
            limit=limit)

    return call_api(func, 0.5, 0)
