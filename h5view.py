
import sys;
import pandas as pd;

if __name__=='__main__':
    df = pd.read_hdf(sys.argv[1]);
    start = int(sys.argv[2]);
    end = int(sys.argv[3]);

    print(df[start:end].to_records());
    pass;

