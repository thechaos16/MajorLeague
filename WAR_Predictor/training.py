import os,sys
import numpy as np
import sim_check as si
import WAR_utils as wu
import data_splitter as ds

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
                err = si.MSE(newtest,newtrain[0:-1])[0]
                if err==0:
                    err = 0.00001
                res+=(newtrain[-1][0]/err)
                errsum+=1/err
            res/=errsum
            predRes.append(res)
        return predRes
    
    def byRegression(self,train,test):
        return 0
        
    def byCRF(self,trian,test):
        return 0
