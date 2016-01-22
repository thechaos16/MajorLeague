import numpy as np
import scipy
import WAR_Predictor.sim_check as si
import WAR_Predictor.WAR_utils as wu
import WAR_Predictor.data_splitter as ds
import WAR_Predictor.linRegression as rg
import WAR_Predictor.evaluation as ev

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
        pred_res = []
        ground_truth = []
        for i in range(len(test)):
            sInterval = self.param['season']
            # season for test should be different (last season shouldn't be added)
            testSeason = [sInterval[0],sInterval[1]-1]
            newtest = wu.DictoList(test[i]['data'],testSeason)
            ground_truth.append(wu.DictoList(test[i]['data'],[sInterval[1],sInterval[1]])[0])
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
            pred_res.append(res)
            
        eval_res = self.evaluation(pred_res,ground_truth)
        return pred_res, eval_res
    
    def byRegression(self,train,test):
        sInterval = self.param['season']
        ## checking sim
        input_season = [sInterval[0],sInterval[1]-1]
        output_season = [sInterval[1],sInterval[1]]
        train_input = []
        train_output = []
        for i in range(len(train)):
            train_input.append([elm[0] for elm in wu.DictoList(train[i]['data'],input_season)])
            train_output.append(wu.DictoList(train[i]['data'],output_season)[0])
        #print(np.array(train_input).shape)
        #print(np.array(train_output).shape)
        rgIns = rg.Regressor(train_input,train_output)
        coeff = rgIns.run()
        # season for test should be different (last season shouldn't be added)
        test_input = []
        test_output = []
        for i in range(len(test)):
            test_input.append([elm[0] for elm in wu.DictoList(test[i]['data'],input_season)])
            test_output.append(wu.DictoList(test[i]['data'],output_season)[0])
        
        predict_output = rgIns.prediction(test_input,coeff[0])
        eval_res = self.evaluation(predict_output,test_output)
        return predict_output, eval_res
        
    def byCRF(self,trian,test):
        return 0

    def evaluation(self,prediction,ground_truth,opt=None):
        evi = ev.Evaluation(prediction,ground_truth,opt)
        return evi.run_by_option()