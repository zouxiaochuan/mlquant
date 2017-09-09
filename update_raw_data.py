import download_data;
import config;
from config import dataio;
import process_raw_data;
import utils_io;

def main():
    names = list(config.DATA_NAMES.keys());
    download_data.clearDir(names);
    download_data.download(names);

    for name,keys in config.DATA_NAMES.items():
        if name=='MktFunddAdjGet' or name=='FundETFConsGet':
            flt = False;
        else:
            flt = True;
            pass;
        print(name);
        dataio.updatedb(name,keys,filterSecID=flt);

    process_raw_data.main();
    utils_io.runExtract('extractors',None);
    pass;

if __name__=='__main__':
    main();
    pass;
