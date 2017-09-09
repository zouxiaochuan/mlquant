import numpy as np;
import config;

def getWeight(dt,weighter=config.WEIGHTER):
    udt = sorted(np.unique(dt).tolist(),reverse=True);
    uw = weighter.get(len(udt));
    wdict = {udt[i]:uw[i] for i in range(len(udt))};

    op = np.vectorize(lambda x:wdict[x]);
    return op(dt);
