# -*- coding: utf-8 -*-

import os
import numpy as np
import pandas as pd


class PreProcessor():
    def __init__(self, data, target):
        if type(data) == pd.DataFrame:
            self.data = data.copy()
        else:
            # if data is another format, convert it into dataframe
            self.data = self.__convert_data_frame(data)
        self.target = target
        
    def __convert_data_frame(self, data):
        if type(data) == dict:
            print('dict!')
        return data
        
    def one_hot_encoding(self, field):
        pass
    
    def numeric_encoding(self, field):
        pass
    

if __name__ == '__main__':
    pass