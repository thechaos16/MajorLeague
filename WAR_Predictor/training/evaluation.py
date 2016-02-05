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
        mse = np.sqrt(np.mean((np.array(self.prediction)-np.array(self.ground_truth))**2))
        return mse
        
    def gini(self):
        gini_score = 0.0
        return gini_score
        