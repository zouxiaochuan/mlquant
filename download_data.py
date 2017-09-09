
import mercury;
import utils_common;

def download(names):
    client = mercury.Client('zouxiaochuan@163.com','iphoipho');
    client.list_data();
    for name in names:
        #print(name);
        utils_common.system('rm -rf *.csv.gz');
        client.download_data(name,True);
        utils_common.system('mkdir -p ../raw/{0}'.format(name));
        utils_common.system('mv *.csv.gz ../raw/{0}/'.format(name));
        utils_common.system('rm -rf *.csv.gz');

        merge('../raw/' + name, '../raw/'+name+'.csv');
        pass;
    pass;

def merge(path,name):
    utils_common.mergeCsvLocal(path,name);
    pass;

def clearDir(names):
    for name in names:
        utils_common.system('rm -rf ../raw/{0}/*'.format(name));
        pass;
    pass;

if __name__=='__main__':
    #client = mercury.Client('zouxiaochuan@163.com','iphoipho');
    #client.list_data();
    #client.download_data('MktEqudGet',True);
    download(['FundETFConsGet']);
