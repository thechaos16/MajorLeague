import random

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
            
    def split_by_method(self):
        if self.opt['method'].lower()=='random':
            return self.split_random()
            
    def get_index(self):
        return self.split_by_method()