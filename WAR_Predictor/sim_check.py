import numpy as np
import sys
import scipy.signal as sig
import scipy as sc
   
class simCheck:
    def __init__(self,vec1,vec2,opt='mse'):
        ## smooth vectors
        self.vec1 = self.smooth(np.array(vec1))
        self.vec2 = self.smooth(np.array(vec2))
        self.opt = opt
        
    def runByOption(self,opt=None):
        if opt!=None:
            self.opt = opt
        if self.opt=='mse':
            return self.MSE()
        elif self.opt=='kl':
            return self.KLDivergence()
        else:
            sys.exit('Error!')
    
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
                
    ## Kullback-Leibler distance
    def KLDivergence(self):
        ## vector normalization
        normVec1 = self.vec1/np.sum(self.vec1)
        normVec2 = self.vec2/np.sum(self.vec2)
        ## kl-distance
        klList = [(normVec1[elm]-normVec2[elm])*np.log10(normVec1[elm]/normVec2[elm]) for elm in range(len(normVec1)) if normVec1[elm]!=0 and normVec2[elm]!=0]
        if len(klList)==0:
            return np.nan
        return np.sum(klList)
        
    ## smoothing
    def smooth(self,data,kernelSize = 5):
        transData = data.T
        for i in range(data.shape[1]):
            ## exception handler
            if kernelSize%2==0:
                kernelSize+=1
            halfWindow = (kernelSize-1)/2
            ## gaussian filter
            gaussFilter = np.exp(-0.5*np.power([elm-(kernelSize-1)/2 for elm in range(kernelSize)],2))
            smoothSignal = np.convolve(transData[i],gaussFilter)
            smoothSignal = smoothSignal[halfWindow:-halfWindow]
            if i==0:
                newData = np.array([smoothSignal])
            else:
                newData = np.append([newData],smoothSignal)
        return newData.T
        
## test
if __name__=='__main__':
    testSig1 = [[1],[2],[1],[2],[1],[2],[1],[2]]
    testSig2 = [[2],[1],[2],[1],[2],[1],[2],[1]]
    sim = simCheck(testSig1,testSig2)
    aaa = sim.runByOption()