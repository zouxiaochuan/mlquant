import wget
import json
import pandas as pd
import os
import utils_common


if __name__ == '__main__':
    wget.download(
        'https://sbcharts.investing.com/events_charts/us/386.json')

    with open('386.json') as fin:
        jdict = json.loads(fin.read())
        pass
    os.remove('386.json')
    
    records = jdict['data']
    records = [[utils_common.ms2dt(r[0]), r[1], 0] for r in records]
    records = sorted(records, key = lambda x: x[0])

    print('num of records: {0}'.format(len(records)))
    base_date = '2020-04-16'
    base_total = 2097

    for i, r in enumerate(records):
        if r[0] == base_date:
            base_idx = i
            break
        pass
            
    if base_idx is None:
        raise RuntimeError('cannot find base index, base date: {0}'.format(
            base_date))

    records[base_idx][2] = base_total
    for i in range(base_idx+1, len(records)):
        records[i][2] = records[i-1][2] + records[i-1][1]
        pass

    for i in range(base_idx-1, -1, -1):
        records[i][2] = records[i+1][2] - records[i+1][1]
        pass

    df = pd.DataFrame(data=records, columns=['date', 'inrement', 'total'])

    df.to_csv('ng_inv.csv', index=False)
    pass
