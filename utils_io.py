import os;
import glob;
import importlib;
import inspect;
import config;
import sys;
import utils_common;

def runExtractInternal(param):
    path = param[0];
    name = param[1];

    print(name);
    constructor = getattr(importlib.import_module(name),name);

    if len(inspect.getargspec(constructor.__init__).args)>1:
        return;

    ext = constructor();
    df = ext.extract();
    #print(df.head(10));
    savename = name;
    config.dataio.save_df(df,savename);
    
    pass;

def runExtract(path, name=None):
    names = [(path,i.split('/')[-1][:-3]) for i in glob.glob(path + '/*.py')];
    sys.path.append(path);
    if name is None:
        for name in names:
            runExtractInternal(name);
            pass;
        pass;
    else:
        runExtractInternal((path,name));
    pass;

def write_df(path,df):
    #utils_common.system('rm -rf {0}'.format(path));
    #df.to_hdf(path,'data');
    df.to_csv(path,float_format='%g');

