import sys;
sys.path.append('..');

import client;
import utils_common;

def getClient():
    return client.YHClientTrader('225300024455','842613', 'D:\ext_c\中国银河证券双子星3.2\Binarystar.exe');

def testBuyList():
    with getClient() as client:
        client.buyList([('510300',100),('601003',100),('600125',100)]);
        print(client.user_.position);
        pass;
    pass;

def testSellSec():
    with getClient() as client:
        client.sellSec({'510300','601003','600125'});
        pass;
    pass;

def testGetMarketValue():
    with getClient() as client:
        print(client.getMarketValue());
        print(client.getPrices(['002312']));
        print(client.getPrice('002312'));
        print(client.getPreClosePrice('002312'));
        print(client.getAvailable());
        pass;
    pass;

def testOnOpen():
    client.strategy = utils_common.getStrategy(sys.argv[1]);
    client.onOpen();

def testOnClose():
    client.strategy = utils_common.getStrategy(sys.argv[1]);
    client.onClose();

if __name__=='__main__':
    #testGetMarketValue();
    #testBuyList();
    testSellSec();
    #testOnOpen();
    #testOnClose();
    pass;
