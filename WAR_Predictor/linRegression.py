# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 23:37:05 2015

@author: Minkyu
"""

import numpy as np
import scipy
from sklearn import linear_model

## Regressor
class Regressor:
    def __init__(self,inputVec,output,alg='elastic',param={}):
        self.inputVec = inputVec
        self.output = output
        self.alg = alg
        self.param = param
        #self.run()
    
    def run(self):
        if self.alg.lower()=='elastic':
            ## validity checker
            coeff = self.linearRegression()
            return coeff
    
    def linearRegression(self):
        clf = linear_model.LinearRegression()
        #print(self.inputVec)
        clf.fit(self.inputVec,self.output)
        return clf.coef_