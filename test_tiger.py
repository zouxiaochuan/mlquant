import json
import utils_tiger
import pandas as pd
import time
import utils_common


with open('./tiger.json') as fin:
    config = json.loads(fin.read())
    pass


utils_tiger.set_config(config)

# symbols = utils_common.file2list('./symbols.txt')

# df: pd.DataFrame = utils_tiger.get_trade_ticks(
#     ['SPY'], 20000, begin_index=None, end_index=None)


# print(df)
# df.to_csv('temp.csv', index=False)

push_client = utils_tiger.get_push_client(config)
quote_client = utils_tiger.get_quote_client(config)

class MyClass(object):
    def on_quote_change(self, *args):
        print(args)
        pass

def on_quote_change(*args):
    print(args)

def on_disconnect():
    while True:
        try:
            push_client._connect()
            break
        except Exception as e:
            print('error happend when connect')
            pass
        pass
    pass

myobj = MyClass()
push_client.quote_changed = on_quote_change
push_client.disconnect_callback = on_disconnect

push_client.subscribe_quote(
    ['CLmain','SPY'], utils_tiger.tiger_consts.QuoteKeyType.ALL)
time.sleep(60)

push_client.unsubscribe_quote(['SPY', 'UGAZ','CLmain','NGmain'])

push_client.disconnect()

#print(utils_tiger.get_bars_minute_dt(quote_client, ['UGAZ'], '2020-03-19'))
