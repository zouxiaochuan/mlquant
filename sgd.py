import numpy as np;

class LinearTimeSeries(object):
    def __init__(self,rank,C):
        self.frank_ = np.array(rank + [0]);
        self.dim_ = len(self.frank_);
        self.w_ = np.random.random(self.dim_)*0.1;
        self.C_ = C;
        pass;

    def sigmoid(self,x):
        return  1/(1+np.exp(-x));

    def project(self,w):
        r = self.frank_ + 1;
        w -= w * r * self.C_;
        return w;
    
    def forwardBackward(self,feature,label):
        n, _ = feature.shape;

        fea = np.hstack((feature,np.ones(n).reshape(-1,1)));
        proba = self.sigmoid(fea.dot(self.w_));
        proba[proba>(1-1e-12)] = 1-1e-12;
        proba[proba<(1e-12)] = 1e-12;
        #print(label);
        loss = -np.mean(label*np.log(proba) + (1-label)*np.log(1-proba));

        grad = (proba-label).dot(fea) / n;

        #print(np.sum(grad*grad));
        #print(self.w_);
        self.w_ -= 5.0*grad;
        self.w_ = self.project(self.w_);

        return loss;

    def predict_proba(self,feature):
        n,_ = feature.shape;
        
        return self.sigmoid(np.hstack((feature,np.ones(n).reshape(-1,1))).dot(self.w_));
    pass;

class SGDSolver(object):
    def __init__(self,function):
        self.function_ = function;
        self.maxIter_ = 30000;
        self.batchSize_ = 100;
        pass;

    def fit(self,feature,label):
        idx = 0;
        n,d = feature.shape;
        self.batchSize_ = n;

        batch = np.zeros((self.batchSize_,d));
        batchLabel = np.zeros(self.batchSize_);
        batchIdx = 0;
        
        for it in range(self.maxIter_):
            while (self.batchSize_-batchIdx+idx)>n:
                stride = n-idx;
                batch[batchIdx:batchIdx+stride] = feature[idx:idx+stride];
                batchLabel[batchIdx:batchIdx+stride] = label[idx:idx+stride];
                idx = 0;
                batchIdx += stride;
                pass;

            stride = self.batchSize_-batchIdx;
            batch[batchIdx:batchIdx+stride] = feature[idx:idx+stride];
            batchLabel[batchIdx:batchIdx+stride] = label[idx:idx+stride];

            loss = self.function_.forwardBackward(batch,batchLabel);
            #print(loss);

            idx += stride;
            batchIdx = 0;
            if idx>=n:
                idx = 0;
                pass;
            pass;
        #print(self.function_.w_);
        pass;

    def predict_proba(self,feature):
        return self.function_.predict_proba(feature);
    
