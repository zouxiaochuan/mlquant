import config;

whilelist= set(['600','601','603','000']);
blacklist = set(['000033.XSHE']);

def filterSecID(secID):
    return (secID[:3] in whilelist) and (secID not in blacklist);

def filterNewStock(df):
    pass;
