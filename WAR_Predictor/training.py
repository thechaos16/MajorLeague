import os,sys
import numpy as np
import sim_check as si
import WAR_utils as wu

class WAR_train:
    def __init__(self,data,alg,param):
        self.wData = data
        self.alg = alg
        self.param = param

    def bySimCheck(self,train,test):
        ## checking sim
        predRes = []
        for i in range(len(test)):
            # season for test should be different (last season shouldn't be added)
            testSeason = [self.param['season'][0],self.param['season'][1]-1]
            newtest = wu.DictoList(test[i]['data'],testSeason)
            res = 0.0
            errsum = 0.0
            for j in range(len(train)):
                newtrain = wu.DictoList(train[j]['data'],self.param['season'])
                ## this is only for current one. err should be array afterwards                
                err = si.MSE(newtest,newtrain[0:-1])[0]
                if err==0:
                    err = 0.00001
                print [newtrain[-1][0],err]
                res+=(newtrain[-1][0]/err)
                errsum+=1/err
            res/=errsum
            predRes.append(res)
        return predRes
        
        
