import sys;
import utils_io;

if __name__=='__main__':
    if len(sys.argv)>2:
        utils_io.runExtract(sys.argv[1],sys.argv[2]);
    else:
        utils_io.runExtract(sys.argv[1],None);
        pass;
    pass;

