import backtest;
import utils_common;
import pandas as pd;
import sys;

def main(strategy,scoreFile,scoreColumn):
    df = pd.read_csv(scoreFile);
    df.sort_values(['tradeDate',scoreColumn],inplace=True,ascending=False);
    dfdt = utils_common.groupDt(df);
    backtest.backtest(1000000,'0000-00-00','9999-99-99',strategy,dfdt);
    pass;

if __name__=='__main__':
    strategy = utils_common.getStrategy(sys.argv[1]);
    scoreFile = sys.argv[2];
    scoreColumn = sys.argv[3];

    main(strategy,scoreFile,scoreColumn);
    pass;
