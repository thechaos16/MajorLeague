import numpy as np
import warnings
from WAR_Predictor.training.evaluation import Evaluation
from WAR_Predictor.data_handler.data_splitter import SplitData
from WAR_Predictor.matching_alg.sim_check import SimCheck
from WAR_Predictor.matching_alg.sim_check_iter import SimCheckIteration
from WAR_Predictor.matching_alg.linear_regression import Regressor
from WAR_Predictor.matching_alg.hidden_markov_model import HiddenMarkovModel
from WAR_Predictor.python_utils.WAR_utils import dict_to_list


# WAR predictor (training model)
class WAR_Train:
    # initialize
    # param should be specified
    def __init__(self,data, param, alg = 'sim', is_train=False):
        self.w_data = data
        self.alg = alg.lower()
        self.param = param
        self.is_train = is_train
    
    # modules for splitting data
    def split_data(self, opt):
        self.train = []
        self.test = []
        splitter = SplitData(self.w_data,opt)
        test_idx = splitter.get_index()
        # if not cross validation, split is only for once
        if type(test_idx[0]) is not list and type(test_idx[0]) is not np.ndarray:
            for i in range(len(self.w_data)):
                if i in test_idx:
                    self.test.append(self.w_data)
                else:
                    self.train.append(self.w_data)
        # for cross validation, return index list
        else:
            return test_idx
    
    # training model by similarity check
    def by_sim_check(self, train=None, test=None, is_iter=False):
        # exception handler
        if train is None:
            try:
                train = self.train
            except NameError:
                self.split_data('random')
                train = self.train
        if test is None:
            try:
                test = self.test
            except NameError:
                self.split_data('random')
                test = self.test
        season_interval = self.param['season']
        ## checking sim
        pred_res = []
        ground_truth = []
        for i in range(len(test)):
            season_interval = self.param['season']
            # season for test should be different (last season shouldn't be added)
            if self.is_train:
                test_season = [season_interval[0], season_interval[1]-1]
            else:
                test_season = [season_interval[0]+1, season_interval[1]]
            test_list = dict_to_list(test[i]['data'],test_season)
            ground_truth.append(dict_to_list(test[i]['data'], 
                                                [season_interval[1],
                                                 season_interval[1]])[0])
            res = 0.0
            errsum = 0.0
            for j in range(len(train)):
                train_list = dict_to_list(train[j]['data'], season_interval)
                # this is only for current one. err should be array afterwards
                if is_iter:
                    sii = SimCheckIteration(test_list,
                                            train_list[0:-1], 'corr')
                else:
                    sii = SimCheck(test_list, train_list[0:-1], 'corr')
                err = sii.run()[0]
                if err==0:
                    err = 0.00001
                res+=(train_list[-1][0]/err)
                errsum+=1/err
            res/=errsum
            pred_res.append(res)
        eval_res = self.evaluation(pred_res, ground_truth)
        return pred_res, eval_res
    
    def by_regression(self, train=None, test=None):
        # exception handler
        if train is None:
            try:
                train = self.train
            except NameError:
                self.split_data('random')
                train = self.train
        if test is None:
            try:
                test = self.test
            except NameError:
                self.split_data('random')
                test = self.test
                
        season_interval = self.param['season']
        # checking sim
        input_season = [season_interval[0],season_interval[1]-1]
        output_season = [season_interval[1],season_interval[1]]
        train_input = []
        train_output = []
        for i in range(len(train)):
            train_input.append([elm[0] for elm in dict_to_list(
            train[i]['data'], input_season)])
            train_output.append(dict_to_list(train[i]['data'],
                                                output_season)[0])
            
        rg_instance = Regressor(train_input,train_output)
        coeff = rg_instance.run()
        # season for test should be different (last season shouldn't be added)
        test_input = []
        test_output = []
        for i in range(len(test)):
            test_input.append([elm[0] for elm in dict_to_list(
            test[i]['data'], input_season)])
            test_output.append(dict_to_list(test[i]['data'],
                                               output_season)[0])
        
        predict_output = rg_instance.prediction(test_input, coeff[0])
        eval_res = self.evaluation(predict_output, test_output)
        return predict_output, eval_res
        
    def by_crf(self, train=None, test=None):
        ## exception handler
        if train is None:
            try:
                train = self.train
            except NameError:
                self.split_data('random')
                train = self.train
        if test is None:
            try:
                test = self.test
            except NameError:
                self.split_data('random')
                test = self.test
        begin_prob = np.zeros(1)
        trans_matrix = np.zeros(1,1)
        means = np.zeros(1)
        variance = np.zeros(1,1)
        hmm_model = HiddenMarkovModel(begin_prob, 
                                      trans_matrix, means, variance)        
        return 0

    def evaluation(self,prediction, ground_truth, opt='mse'):
        evi = Evaluation(prediction, ground_truth, opt)
        return evi.run_by_option()
        
    def cross_validation(self, valid_ratio=0.2):
        test_idx = self.split_data({'method': 'cross', 'ratio': valid_ratio})
        total_evaluation = 0.0
        for i in range(len(test_idx)):
            new_train = []
            new_test = []
            for j in range(len(self.w_data)):
                if j in test_idx[i]:
                    new_test.append(self.w_data[j])
                else:
                    new_train.append(self.w_data[j])
            if self.alg == 'sim':
                predict, evaluation = self.by_sim_check(new_train, new_test)
            elif self.alg == 'regression':
                predict, evaluation = self.by_regression(new_train, new_test)
            elif self.alg == 'crf':
                predict, evaluation = self.by_crf(new_train, new_test)
            else:
                warnings.warn('algorithm error!')
            total_evaluation += evaluation
        return total_evaluation / len(test_idx)
