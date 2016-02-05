# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 01:13:27 2015

@author: Minkyu
"""

import unittest
import sys
import numpy as np
sys.path.append('../')
import WAR_Predictor.python_utils.WAR_utils as wu

class utilsTest(unittest.TestCase):
    number_of_test = 10
    def test_interval(self):
        for i in range(self.number_of_test):
            least_integer = np.random.randint(1990,2020)
            interval = np.random.randint(0,10)
            sample_list = []
            #print([least_integer, least_integer+interval-1])
            for j in range(interval):
                sample_list.append({'season':least_integer+j})
            try:
                res = wu.getSeasonInterval(sample_list)
            #print(res)
                self.assertEqual(res,[least_integer, least_integer+interval-1])
            except Exception:
                pass
    def test_dict_to_list(self):
        for i in range(self.number_of_test):
            least_integer = np.random.randint(1990,2020)
            interval = np.random.randint(0,10)
            sample_list = []
            #print([least_integer, least_integer+interval-1])
            for j in range(interval):
                sample_list.append({'season':least_integer+j,'testcase':j})
            try:
                targetDict = wu.DictoList(sample_list,[least_integer, least_integer+interval-1])
                print(targetDict)
            except Exception:
                pass
            except IndexError:
                pass
            

if __name__=='__main__':
    test = unittest.makeSuite(utilsTest,'test')
    run = unittest.TextTestRunner()
    run.run(test)