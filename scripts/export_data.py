import pytz
from datetime import datetime
import sys
import context
import os


def export(symbol: str, dt: str, output_dir: str):
    eastern = pytz.timezone('US/Eastern')

    start = f'{dt} 09:30:00'
    end = f'{dt} 16:00:00'

    start_date = datetime.strptime(start, '%Y-%m-%d %H:%M:%S').replace(tzinfo=eastern)
    end_date = datetime.strptime(end, '%Y-%m-%d %H:%M:%S').replace(tzinfo=eastern)

    start_ts = start_date.timestamp() * 1000
    end_ts = end_date.timestamp() * 1000

    data_manager = context.create_data_manager()

    bar_seq = data_manager.get_bars(symbol, 60000, start_ts, end_ts)

    folder = os.path.join(output_dir, symbol)
    os.makedirs(folder, exist_ok=True)
    filename = os.path.join(folder, f'{dt}.txt')

    df = bar_seq.to_df()

    df.to_csv(filename, index=False)
    pass


if __name__ == '__main__':
    symbol = sys.argv[1]
    dt = sys.argv[2]
    output_dir = sys.argv[3]

    context.init()

    export(symbol, dt, output_dir)
    pass