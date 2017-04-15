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
    # param should be specified
    def __init__(self, data, param, alg='regression', is_train=False, ignore_fields=['player_id', 'player_name']):
        """
        
        :param data: entire data including WAR of each season, player id, and player name (dataframe)
        :param param: TODO: this should be moved to each function (because they are all different)
        :param alg: name of method
        :param is_train: only for similarity check (maybe it needs to be moved to specific function)
        :param ignore_fields: list of fields to ignore (remove from training set)
        """
        self.w_data = data
        self.alg = alg.lower()
        self.param = param
        self.is_train = is_train
        self.ignore_fields = ignore_fields
        self.train = None
        self.test = None
    
    # modules for splitting data
    def split_data(self, opt):
        """
        Splitting data if there is only one given dataset
        :param opt: options for splitting (check data_splitter.py)
        :return: index for test data (to save memory size)
        """
        splitter = SplitData(self.w_data, opt)
        test_idx = splitter.get_index()
        # if not cross validation, split is only for once
        if type(test_idx[0]) is not list and type(test_idx[0]) is not np.ndarray:
            train_idx = np.ones(len(self.w_data)).astype(bool)
            for idx in test_idx:
                train_idx[idx] = False
            self.train = self.w_data[train_idx]
            self.test = self.w_data[~train_idx]
        # for cross validation, return index list
        else:
            return test_idx

    def training_preparation(self, train=None, test=None):
        """
        Some steps which all methods share
        :param train: 
        :param test: 
        :return: 
        """
        # exception handler
        if train is None:
            if self.train is not None:
                train = self.train
            else:
                self.split_data({'method': 'random', 'ratio': 0.2})
                train = self.train
        if test is None:
            if self.test is not None:
                test = self.test
            else:
                self.split_data({'method': 'random', 'ratio': 0.2})
                test = self.test
        return train, test
    
    # training model by similarity check
    # FIXME: sim_check method should be replaced by gaussian process (it's basically same mechanism)
    def by_sim_check(self, train=None, test=None, is_iter=False):
        train, test = self.training_preparation(train, test)
        season_interval = self.param['season']
        # checking sim
        train_input = train[list(set(train.columns) - set(self.ignore_fields))]
        test_input = train[list(set(train.columns) - set(self.ignore_fields))]
        pred_res = []
        ground_truth = []
        for i in range(len(test)):
            # season for test should be different (last season shouldn't be added)
            if self.is_train:
                test_season = [season_interval[0], season_interval[1]-1]
            else:
                test_season = [season_interval[0]+1, season_interval[1]]
            test_list = dict_to_list(test[i]['data'], test_season)
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
                if err == 0:
                    err = 0.00001
                res += (train_list[-1][0]/err)
                errsum += 1/err
            res /= errsum
            pred_res.append(res)
        eval_res = self.evaluation(pred_res, ground_truth)
        return pred_res, eval_res
    
    def by_regression(self, train=None, test=None):
        train, test = self.training_preparation(train, test)
        season_interval = self.param['season']
        target_season = ['WAR_'+str(season_interval[1])]
        # FIXME: for now, replace nan into 0
        train_input = np.nan_to_num(np.array(train[list(set(train.columns) - set(target_season + self.ignore_fields))]))
        train_output = np.nan_to_num(np.array(train[target_season]))

        rg_instance = Regressor(train_input, train_output)
        coef = rg_instance.run()
        # season for test should be different (last season shouldn't be added)
        test_input = np.nan_to_num(np.array(test[list(set(test.columns) - set(target_season + self.ignore_fields))]))
        test_output = np.nan_to_num(np.array(test[target_season]))
        
        predict_output = rg_instance.prediction(test_input, coef[0])
        eval_res = self.evaluation(predict_output, test_output)
        return predict_output, eval_res
        
    def by_crf(self, train=None, test=None):
        train, test = self.training_preparation(train, test)
        begin_prob = np.zeros(1)
        trans_matrix = np.zeros(1,1)
        means = np.zeros(1)
        variance = np.zeros(1,1)
        hmm_model = HiddenMarkovModel(begin_prob, 
                                      trans_matrix, means, variance)        
        return 0

    def by_gaussian_process(self, train=None, test=None):
        train, test = self.training_preparation(train, test)

    def evaluation(self, prediction, ground_truth, opt='mse'):
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
