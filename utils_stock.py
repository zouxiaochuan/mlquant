import config;

whilelist= set(['600','601','603','000']);

def filterSecID(secID):
    return (secID[:3] in whilelist) and (secID not in config.BLACK_LIST);

def filterNewStock(df):
    pass;
