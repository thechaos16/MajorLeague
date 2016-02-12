# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 23:51:05 2016

@author: Minkyu
"""

import numpy as np

class Evaluation:
    def __init__(self,prediction,ground_truth,opt = 'mse'):
        self.prediction = prediction
        self.ground_truth = ground_truth
        if len(self.prediction)!=len(self.ground_truth):
            raise ValueError('ground truth and prediction should have same length!')
        if opt==None:
            self.opt='mse'
        else:
            self.opt = opt
    
    def run_by_option(self):
        if self.opt=='mse':
            return self.mse()
        elif self.opt=='gini':
            return self.gini()
        
    def mse(self):
        ## normalization?
        result = (np.array(self.prediction)-np.array(self.ground_truth))**2
        mse = np.sqrt(np.mean(np.array([elm for elm in result if elm is not np.nan])))
        return mse
        
    def gini(self):
        gini_score = 0.0
        return gini_score
        