# -*- coding: utf-8 -*-
"""
Created on Thu Feb 25 23:11:39 2016

@author: thech
"""

import unittest
import sys
import numpy as np
sys.path.append('../')


class FangraphsParserTest(unittest):
    def init_test(self):
        self.__make_fake_csv()

    def test_parser(self):
        pass
    
    def test_join(self):
        pass

    ## internal fucntion to make fake data
    def __make_fake_csv(self,number_of_files=5,data_line=100):
        ## generate fields
        key = 'Key'
        fields_cand = ['A','B','C','D','E','F','AAA','BBB','CCC','DDD','EEE','FFF']
        for i in range(number_of_files):
            csv_file = 'temp_csv_'+str(i+1)+'.csv'
            f = open(csv_file,'w')
            fields = [key]
            rand_idx = np.random.randint(0,len(fields_cand),3)
            for idx in rand_idx:
                fields.append(fields_cand[idx])
            f.write(','.join(fields)+'\n')
            for j in range(data_line):
                data_line = np.random.random(size=len(fields))*100
                data_line = [str(round(elm,3)) for elm in data_line]
                f.write(','.join(data_line)+'\n')
            f.close()            
    
if __name__=='__main__':
    fpt = FangraphsParserTest()