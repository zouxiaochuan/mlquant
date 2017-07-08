import sys;
import utils_io;

if __name__=='__main__':
    if len(sys.argv)>1:
        utils_io.runExtract('features',sys.argv[1]);
    else:
        utils_io.runExtract('features',None);
        pass;
    pass;

