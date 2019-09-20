from typing import Type
import tigeropen.common.consts as tiger_consts
from tigeropen.tiger_open_config import TigerOpenClientConfig
from tigeropen.quote.quote_client import QuoteClient
from tigeropen.common.util.signature_utils import read_private_key

import utils_common


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


def get_bars_minute(
        quote_client: QuoteClient,
        symbols: list,
        begin_time: int,
        end_time: int):

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
