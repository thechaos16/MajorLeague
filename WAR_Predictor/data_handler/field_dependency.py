# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd


class FieldDependency:
    def __init__(self, data):
        self.data = self.data_converter(data)
    
    def data_converter(self, data):
        if type(data) is pd.DataFrame:
            return data
        else:
            raise NotImplementedError('Currently, only data frame is acceptable!')
    
    def check_by_covariance(self):
        pass
    

if __name__ == '__main__':
    pass