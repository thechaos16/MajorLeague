# -*- coding: utf-8 -*-
"""
Created on Wed Feb 10 19:13:50 2016

@author: thech
"""

import numpy as np
import sys
## for test
try:
    import WAR_Predictor.matching_alg.sim_check as si
except ImportError:
    sys.path.append('../../')
    import WAR_Predictor.matching_alg.sim_check as si
 

class SimCheckIteration:
    def __init__(self,vec1,vec2,opt):
        self.vec1 = vec1
        self.vec2 = vec2
        self.opt = opt
    
    def run(self):
        result_list = []
        for i in range(len(self.vec1)):
            similarity_check = si.SimCheck(self.vec1[i:],self.vec2[i:],self.opt)
            error = similarity_check.run()
            result_list.append(error)
        ## should be improved
        return [np.mean([elm for elm in result_list if elm is not np.nan])]
            
if __name__=='__main__':
    kk = SimCheckIteration([[1],[2],[3]],[[1],[2],[5]],'kl')
    print(kk.run())