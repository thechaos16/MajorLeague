import random

class splitData:
    ## option: {'method': 'random', 'ratio':0.7}
    def __init__(self,data,opt):
        self.data = data
        self.opt = opt
    
    def splitRandom(self):
        ## random sampling
        upLimit = max(self.data)
        downLimit = min(self.data)
        testIdx = []
        while True:
            randNum = random.randint(downLimit,upLimit)
            if randNum not in testIdx:
                testIdx.append(randNum)
            if len(testIdx)>=self.opt['ratio']*len(self.data):
                return testIdx
            
    def splitByMethod(self):
        if self.opt['method'].lower()=='random':
            return self.splitRandom()