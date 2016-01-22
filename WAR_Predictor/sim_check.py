import numpy as np
import sys
import scipy.signal as sig
import scipy as sc
   
class SimCheck:
    def __init__(self,vec1,vec2,opt='mse'):
        ## smooth vectors
        self.vec1 = self.smooth(np.array(vec1))
        self.vec2 = self.smooth(np.array(vec2))
        self.opt = opt
        
    def run_by_option(self,opt=None):
        if opt!=None:
            self.opt = opt
        if self.opt=='mse':
            return self.mse()
        elif self.opt=='kl':
            return self.kl_divergence()
        else:
            sys.exit('Error!')
    
    ## same length, dic
    ## MSE
    def mse(self):
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
    def mse_with_diff_length(self):
        ans = []
        return ans
                
    ## Kullback-Leibler distance
    def kl_divergence(self):
        res = []
        for i in range(len(self.vec1[0])):
            ## vector normalization
            norm_vec1 = self.vec1/np.sum(self.vec1)
            norm_vec2 = self.vec2/np.sum(self.vec2)
            ## kl-distance
            kl_list = [(norm_vec1[elm]-norm_vec2[elm])*np.log10(norm_vec1[elm]/norm_vec2[elm]) for elm in range(len(norm_vec1)) if norm_vec1[elm]!=0 and norm_vec2[elm]!=0]
            if len(kl_list)==0:
                res.append(np.nan)
            else:
                res.append(np.sum(kl_list))
        return res
        
    ## smoothing
    def smooth(self,data,kernel_size = 5):
        trans_data = data.T
        for i in range(data.shape[1]):
            ## exception handler
            if kernel_size%2==0:
                kernel_size+=1
            half_window = (kernel_size-1)/2
            ## gaussian filter
            gauss_filter = np.exp(-0.5*np.power([elm-(kernel_size-1)/2 for elm in range(kernel_size)],2))
            smooth_signal = np.convolve(trans_data[i],gauss_filter)
            smooth_signal = smooth_signal[half_window:-half_window]
            if i==0:
                new_data = np.array([smooth_signal])
            else:
                new_data = np.append([new_data],smooth_signal)
        return new_data.T
        
    
        
## test
if __name__=='__main__':
    test_sig1 = [[1],[2],[1],[2],[1],[2],[1],[2]]
    test_sig2 = [[2],[1],[2],[1],[2],[1],[2],[1]]
    sim = SimCheck(test_sig1,test_sig2,'kl')
    aaa = sim.run_by_option()