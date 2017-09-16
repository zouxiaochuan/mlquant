import urllib2;
import sys;
import pandas as pd;
import json;

ip = '47.52.101.241'

def main(filename):
    df = pd.read_csv(filename);
    records = df.to_dict('records');
    urllib2.urlopen('http://{0}:18000/uploadScore'.format(ip),data=json.dumps(records)
                    ,timeout=10);
    pass;

if __name__=='__main__':
    filename = sys.argv[1];
    main(filename);
    pass;
