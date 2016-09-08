# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 20:25:37 2016

@author: thech
"""

import numpy as np
from hmmleanr import hmm


class HiddenMarkovModel:
    def __init__(self, begin_prob, trans_matrix, means,
                 covariance,number_of_samples=100):
        self.begin_prob = begin_prob
        self.trans_matrix = trans_matrix
        self.means = means
        self.covariance = covariance
        self.number_of_samples = number_of_samples
        if not self.validity_checker():
            raise ValueError('HMM initialization failed!')
        self.model_construction()
        
    def validity_checker(self):
        return True
        
    def model_construction(self):
        self.model = hmm.GaussianHMM(len(self.begin_prob),'full',begin_prob,trans_matrix)
        self.model.means_ = self.means
        self.model.covars_ = self.covariance
        # return model.sample(self.number_of_samples)
    
    def prediction(self,input_data):
        self.model.fit([input_data])
        pred = self.model.predict(input_data)
        return pred
    

# sample
if __name__=='__main__':
    begin_prob = np.array([0.6, 0.1, 0.3])
    trans_matrix = np.array([[0.7, 0.2, 0.1], [0.3, 0.5, 0.2], 
                             [0.3, 0.3, 0.4]])
    means = np.array([[0.0, 0.0], [3.0, -3.0], [5.0, 10.0]])
    covariance = np.tile(np.identity(2), (3, 1, 1))
    hmm_instance = HiddenMarkovModel(begin_prob, trans_matrix,
                                     means, covariance)
    X = []
    for i in range(100):
        temp_list  = np.random.normal(loc=0.0, scale=5.0, size=2)
        X.append(temp_list)
    Z = hmm_instance.prediction(np.array(X))
