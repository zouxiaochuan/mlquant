import numpy as np;

class Simple(object):
    def __init__(self,alpha=0.001):
        self.alpha_ = alpha;
    
    def get(self,num):
        v = np.array(range(num));
        v = 2.0/(1.0+np.exp(v*self.alpha_));
        return v;

    pass;

class Step(object):
    def __init__(self,step=66):
        self.step_ = step;
        pass;

    def get(self,num):
        if num<=self.step_:
            return np.ones(num);
        else:
            ret = np.ones(num);
            ret[self.step_:] = 0.55;
            return ret;
            pass;
        pass;

class AllSame(object):
    def get(self,num):
        return np.ones(num);
    pass;


if __name__=='__main__':
    wg = Simple();
    w = wg.get(10000);

    intervals = [1,10,50,100,300,500,1000];
    for i in intervals:
        print('{0}:{1}'.format(i,w[i]));
        pass;
    pass;

