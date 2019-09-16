import utils_tiger
import utils_common
import pandas as pd
import os
import time
import json


def download_tiger_bar(
        config: dict,
        symbols: list,
        save_path,
        start_dt,
        end_dt):
    dt = end_dt

    client = utils_tiger.get_quote_client(config)
    while True:
        print(dt)
        df: pd.DataFrame = utils_tiger.get_bars_minute_dt(client, symbols, dt)
        if df.shape[0] > 0:
            save_name = os.path.join(save_path, dt + '.csv')
            df.to_csv(save_name, index=False)
            pass

        dt = utils_common.dt_add(dt, -1)
        time.sleep(30)
        pass
    pass


if __name__ == '__main__':
    with open('./tiger.json') as fin:
        config = json.loads(fin.read())
        pass

    download_tiger_bar(config, ['UGAZ'], 'UGAZ', '2015-01-01', '2019-09-15')
    pass
