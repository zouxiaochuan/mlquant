# -*- coding: utf-8 -*-

#from pathos.multiprocessing import Pool;
from multiprocessing import Pool;

NUM_PROC=30;

def parallel(func,params,nProc=NUM_PROC):
    pool = Pool(processes=nProc);
    results = pool.map(func,params);
    pool.close()
    return results;

def parallel_debug(func,params,nProc=NUM_PROC):
    ret = [];
    for i,p in enumerate(params):
        print(i);
        ret.append(func(p));
    return ret;
