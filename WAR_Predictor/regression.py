# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 23:37:05 2015

@author: Minkyu
"""

## Regressor
class Regressor:
    def __init(self,train,test,alg,param):
        self.train = train
        self.test = test
        self.alg = alg
        self.param = param
        self.run()
    
    def run(self):
        if self.alg.lower()=='elastic':
            ## validity checker
            runElastic(self.train,self.test)
    
    def runElastic(self,train,test):
        return 0