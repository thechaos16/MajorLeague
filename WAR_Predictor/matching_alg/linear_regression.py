# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 23:37:05 2015

@author: Minkyu
"""

import numpy as np
import warnings
from sklearn import linear_model


# Regressor
class Regressor:
    def __init__(self, input_vector, output, alg='ridge', param={}):
        self.input_vector = input_vector
        self.output = output
        self.alg = alg
        self.param = param
    
    def run(self):
        if self.alg.lower()=='linear':
            # validity checker
            coeff = self.linear_regression()
            return coeff
        elif self.alg.lower()=='ridge':
            coeff = self.ridge_regression()
            return coeff
        elif self.alg.lower()=='elastic':
            coeff = self.ridge_regression()
            return coeff
        else:
            warnings.warn('Other algorithm has not been implemented!')

    def normalization(self):
        # for now, it runs inside sklearn module
        pass
    
    def linear_regression(self):
        clf = linear_model.LinearRegression()
        # print(self.input_vector)
        clf.fit(self.input_vector,self.output)
        return clf.coef_
        
    def ridge_regression(self):
        clf = linear_model.Ridge()
        clf.fit(self.input_vector,self.output)
        return clf.coef_
        
    def elastic_net(self):
        clf = linear_model.ElasticNet()
        clf.fit(self.input_vector,self.output)
        return clf.coef_
        
    def prediction(self,test_data,coeff):
        test_res = []
        for i in range(len(test_data)):
            temp_res = np.sum(np.dot(test_data[i],coeff))
            test_res.append(temp_res)
        return test_res
