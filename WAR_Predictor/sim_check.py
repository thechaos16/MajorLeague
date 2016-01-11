import numpy as np
import scipy.signal as sig
import scipy as sc
## step one:
## same length, dic
## MSE
def MSE(a,b):
    ans = []
    for i in range(len(a[0])):
        ans.append(0.0)
    for i in range(len(a)):
        for j in range(len(a[i])):
            diff = a[i][j]-b[i][j]
            ans[j]+=diff*diff
    ans = list(map(lambda x:x/len(a),ans))
    return ans
   
class simCheck:
    def __init__(self,vec1,vec2,opt='mse'):
        self.vec1 = vec1
        self.vec2 = vec2
        self.opt = opt
        
    def runByOption(self,opt=None):
        if opt!=None:
            self.opt = opt
    
    ## same length, dic
    ## MSE
    def MSE(self):
        ans = []
        for i in range(len(self.vec1[0])):
            ans.append(0.0)
        for i in range(len(self.vec1)):
            for j in range(len(self.vec1[i])):
                diff = self.vec1[i][j]-self.vec2[i][j]
                ans[j]+=diff*diff
        ans = list(map(lambda x:x/len(self.vec1),ans))
        return ans
        
    ## MSE for different length
    ## a should be shorter than b
    def MSEWithDiffLength(self):
        ans = []
        return ans
        
        
    ## Kullback-Leibler divergence
    def KLDivergence(self):
        ans = []
        return ans
    
    ## smoothing
    def smooth(self,data,kernelSize = 5):
        ## exception handler
        if kernelSize%2==0:
            kernelSize+=1
        ## gaussian filter
        return ans