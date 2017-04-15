# -*- coding: utf-8 -*-
import numpy as np
import warnings
from sklearn import linear_model


class Regressor:
    def __init__(self, input_vector, output, alg='ridge', param={}):
        self.input_vector = input_vector
        self.output = output
        self.alg = alg
        self.param = param
        self.regressor = None
    
    def run(self):
        if self.alg.lower() == 'linear':
            # validity checker
            coeff = self.linear_regression()
        elif self.alg.lower() == 'ridge':
            coeff = self.ridge_regression()
        elif self.alg.lower() == 'elastic':
            coeff = self.ridge_regression()
        else:
            warnings.warn('Other algorithm has not been implemented!')
        return coeff

    def normalization(self):
        # for now, it runs inside sklearn module
        pass
    
    def linear_regression(self):
        self.regressor = linear_model.LinearRegression()
        # print(self.input_vector)
        self.regressor.fit(self.input_vector, self.output)
        return self.regressor.coef_
        
    def ridge_regression(self):
        self.regressor = linear_model.Ridge()
        self.regressor.fit(self.input_vector, self.output)
        return self.regressor.coef_
        
    def elastic_net(self):
        self.regressor = linear_model.ElasticNet()
        self.regressor.fit(self.input_vector, self.output)
        return self.regressor.coef_
        
    def prediction(self, test_data, coef=None):
        if coef is None:
            coef = self.regressor.coef_
        test_res = []
        for i in range(len(test_data)):
            temp_res = np.sum(np.dot(test_data[i], coef))
            test_res.append(temp_res)
        return test_res
