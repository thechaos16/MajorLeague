# -*- coding: utf-8 -*-
"""
Created on Fri Jan 22 23:51:05 2016

@author: Minkyu
"""

import numpy as np


class Evaluation:
    def __init__(self, prediction, ground_truth, opt = 'mse'):
        self.prediction = np.array(prediction)
        self.ground_truth = np.array(ground_truth)
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
        else:
            raise NotImplementedError()
        
    def mse(self):
        # normalization?
        result = (np.array(self.prediction)-np.array(self.ground_truth))**2
        mse = np.sqrt(np.mean(np.array([elm for elm in result if elm is not np.nan])))
        return mse
        
    def gini(self):
        sorted_gt_by_pred = self.ground_truth[np.argsort(self.prediction)]
        sorted_gt_by_pred = np.cumsum(sorted_gt_by_pred) / np.sum(sorted_gt_by_pred)
        sorted_gt_by_gt = self.ground_truth[np.argsort(self.ground_truth)]
        sorted_gt_by_gt = np.cumsum(sorted_gt_by_gt) / np.sum(sorted_gt_by_gt)
        x_axis = np.linspace(0, 1, len(self.prediction))
        score_pred = np.sum(sorted_gt_by_pred - x_axis)
        score_gt = np.sum(sorted_gt_by_gt - x_axis)
        gini_score = score_pred / score_gt
        return gini_score
        