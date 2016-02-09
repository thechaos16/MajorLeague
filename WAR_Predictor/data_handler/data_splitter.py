import random
import warnings
import numpy as np

class SplitData:
    ## option: {'method': 'random', 'ratio':0.7}
    def __init__(self,data,opt):
        self.data = data
        self.opt = opt
    
    def split_random(self):
        ## random sampling
        up_limit = max(self.data)
        down_limit = min(self.data)
        test_idx = []
        while True:
            rand_num = random.randint(down_limit,up_limit)
            if rand_num not in test_idx:
                test_idx.append(rand_num)
            if len(test_idx)>=self.opt['ratio']*len(self.data):
                return test_idx
                
    def split_for_cross_validation(self):
        number_of_test = int(1.0/self.opt['ratio'])
        list_size = self.opt['ratio']*len(self.data)
        test_idx = []
        candidates = np.linspace(0,len(self.data)-1,len(self.data))
        np.random.shuffle(candidates)
        test_idx = [candidates[list_size*elm:list_size*(elm+1)] for elm in range(number_of_test)]
        return test_idx

    def split_by_method(self):
        if self.opt['method'].lower()=='random':
            return self.split_random()
        elif self.opt['method'].lower()=='cross':
            return self.split_for_cross_validation()
        else:
            warnings.warn('split method should be selected')
            
    def get_index(self):
        return self.split_by_method()