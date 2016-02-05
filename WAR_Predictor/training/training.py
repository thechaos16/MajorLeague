import numpy as np
import scipy
import WAR_Predictor.matching_alg.sim_check as si
import WAR_Predictor.python_utils.WAR_utils as wu
import WAR_Predictor.data_handler.data_splitter as ds
import WAR_Predictor.matching_alg.linRegression as rg
import WAR_Predictor.training.evaluation as ev

## WAR predictor (training model)
class WAR_Train:
    ## initialize
    ## param should be specified
    def __init__(self,data,alg,param):
        self.w_data = data
        self.alg = alg
        self.param = param
    
    ## modules for splitting data
    def split_data(self,opt):
        self.train = []
        self.test = []
        splitter = ds.SplitData(self.w_data,opt)
        test_idx = splitter.get_index()
        for i in range(len(self.w_data)):
            if i in test_idx:
                self.test.append(self.w_data)
            else:
                self.train.append(self.w_data)
    
    ## training model by similarity check
    def by_sim_check(self,train,test):
        season_interval = self.param['season']
        ## checking sim
        pred_res = []
        ground_truth = []
        for i in range(len(test)):
            season_interval = self.param['season']
            # season for test should be different (last season shouldn't be added)
            test_season = [season_interval[0],season_interval[1]-1]
            test_list = wu.dict_to_list(test[i]['data'],test_season)
            ground_truth.append(wu.dict_to_list(test[i]['data'],[season_interval[1],season_interval[1]])[0])
            res = 0.0
            errsum = 0.0
            for j in range(len(train)):
                train_list = wu.dict_to_list(train[j]['data'],season_interval)
                ## this is only for current one. err should be array afterwards
                sii = si.SimCheck(test_list,train_list[0:-1])
                err = sii.mse()[0]
                if err==0:
                    err = 0.00001
                res+=(train_list[-1][0]/err)
                errsum+=1/err
            res/=errsum
            pred_res.append(res)
            
        eval_res = self.evaluation(pred_res,ground_truth)
        return pred_res, eval_res
    
    def by_regression(self,train,test):
        season_interval = self.param['season']
        ## checking sim
        input_season = [season_interval[0],season_interval[1]-1]
        output_season = [season_interval[1],season_interval[1]]
        train_input = []
        train_output = []
        for i in range(len(train)):
            train_input.append([elm[0] for elm in wu.dict_to_list(train[i]['data'],input_season)])
            train_output.append(wu.dict_to_list(train[i]['data'],output_season)[0])
        #print(np.array(train_input).shape)
        #print(np.array(train_output).shape)
        rg_instance = rg.Regressor(train_input,train_output)
        coeff = rg_instance.run()
        # season for test should be different (last season shouldn't be added)
        test_input = []
        test_output = []
        for i in range(len(test)):
            test_input.append([elm[0] for elm in wu.dict_to_list(test[i]['data'],input_season)])
            test_output.append(wu.dict_to_list(test[i]['data'],output_season)[0])
        
        predict_output = rg_instance.prediction(test_input,coeff[0])
        eval_res = self.evaluation(predict_output,test_output)
        return predict_output, eval_res
        
    def by_crf(self,trian,test):
        return 0

    def evaluation(self,prediction,ground_truth,opt=None):
        evi = ev.Evaluation(prediction,ground_truth,opt)
        return evi.run_by_option()