import numpy as np
import scipy
import WAR_Predictor.sim_check as si
import WAR_Predictor.WAR_utils as wu
import WAR_Predictor.data_splitter as ds
import WAR_Predictor.linRegression as rg

## WAR predictor (training model)
class WAR_train:
    ## initialize
    ## param should be specified
    def __init__(self,data,alg,param):
        self.wData = data
        self.alg = alg
        self.param = param
    
    ## modules for splitting data
    def splitData(self,opt):
        self.train = []
        self.test = []
        splitter = ds.splitData(self.wData,opt)
        testIdx = splitter.getIdx()
        for i in range(len(self.wData)):
            if i in testIdx:
                self.test.append(self.wData)
            else:
                self.train.append(self.wData)
    
    ## training model by similarity check
    def bySimCheck(self,train,test):
        sInterval = self.param['season']
        ## checking sim
        predRes = []
        for i in range(len(test)):
            sInterval = self.param['season']
            # season for test should be different (last season shouldn't be added)
            testSeason = [sInterval[0],sInterval[1]-1]
            newtest = wu.DictoList(test[i]['data'],testSeason)
            res = 0.0
            errsum = 0.0
            for j in range(len(train)):
                newtrain = wu.DictoList(train[j]['data'],sInterval)
                ## this is only for current one. err should be array afterwards
                sii = si.simCheck(newtest,newtrain[0:-1])
                err = sii.MSE()[0]
                if err==0:
                    err = 0.00001
                res+=(newtrain[-1][0]/err)
                errsum+=1/err
            res/=errsum
            predRes.append(res)
        return predRes
    
    def byRegression(self,train,test):
        sInterval = self.param['season']
        ## checking sim
        predRes = []
        inputSeason = [sInterval[0],sInterval[1]-1]
        outputSeason = [sInterval[1],sInterval[1]]
        trainInput = []
        trainOutput = []
        for i in range(len(train)):
            trainInput.append([elm[0] for elm in wu.DictoList(train[i]['data'],inputSeason)])
            trainOutput.append(wu.DictoList(train[i]['data'],outputSeason)[0])
        print(np.array(trainInput).shape)
        print(np.array(trainOutput).shape)
        rgIns = rg.Regressor(trainInput,trainOutput)
        coeff = rgIns.run()
        # season for test should be different (last season shouldn't be added)
        #testSeason = [sInterval[0],sInterval[1]-1]
        #newtest = wu.DictoList(test[i]['data'],testSeason)
        return coeff
        
    def byCRF(self,trian,test):
        return 0
