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
        
    def data_transform(self):
        intermediate_data = self.data.copy()
        for field in self.data.columns:
            # only categorical fields
            converted = self.one_hot_encoding(field)
            # remove field
            intermediate_data = intermediate_data.drop(field, 1)
            # add fields
            intermediate_data = pd.concat([intermediate_data, 
                                           converted], axis=1)
        final_data = self.numeric_encoding(intermediate_data)
        return final_data
        
    def one_hot_encoding(self, field):
        pass
    
    def numeric_encoding(self, data_frame):
        # decomposition based on field_dependency
        # first, do one_hot_encoding to convert everything into numeric, and run numeric encoding        
        pass

    

if __name__ == '__main__':
    pass