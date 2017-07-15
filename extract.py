import sys;
import utils_io;

if __name__=='__main__':
    if len(sys.argv)>1:
        utils_io.runExtract('extractors',sys.argv[1]);
    else:
        utils_io.runExtract('extractors',None);
        pass;
    pass;

