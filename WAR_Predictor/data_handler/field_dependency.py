# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


class FieldDependency:
    # TODO: this framework should be upgraded to deal with chunk-by-chunk mehotd afterwards
    def __init__(self, data):
        self.data = self.data_converter(data)
    
    def data_converter(self, data):
        if type(data) is pd.DataFrame:
            return data
        else:
            raise NotImplementedError('Currently, only dataframe is acceptable!')
            
    def field_decomposition(self):
        # decomposite fields based on independency
        pass        
        
    def dependency_check_with_correlation(self):
        # compute correlation
        correlation_mat = self.data.corr()
        # determination coefficient
        determination = correlation_mat**2
        corr_thr = 0.5
        susp_idx = np.where(determination >= corr_thr)
        susp_fields = []
        for idx in range(len(susp_idx[0])):
            if susp_idx[0][idx] == susp_idx[1][idx]:
                continue
            matched = sorted((correlation_mat.columns[susp_idx[0][idx]],
                              correlation_mat.columns[susp_idx[1][idx]]))
            if matched not in susp_fields:
                susp_fields.append(matched)
        return susp_fields
        
    def dependency_check_with_t_test(self):
        pass
    

if __name__ == '__main__':
    kk = pd.DataFrame(np.random.randn(100, 5), columns=['a','b','c','d','e'])
    kk['f'] = kk['a']
    nnn = FieldDependency(kk)
    aaa = nnn.dependency_check_with_correlation()