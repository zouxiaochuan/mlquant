# -*- coding: utf-8 -*-

from pathos.multiprocessing import Pool;

NUM_PROC=20;

def parallel(func,params,nProc=NUM_PROC):
    pool = Pool(processes=nProc);
    return pool.map(func,params);

def parallel_debug(func,params,nProc=NUM_PROC):
    ret = [];
    for i,p in enumerate(params):
        print(i);
        ret.append(func(p));
    return ret;
