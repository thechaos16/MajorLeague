# -*- coding: utf-8 -*-
"""
Created on Fri Dec 25 01:13:27 2015

@author: Minkyu
"""

import unittest
import sys
import numpy as np
sys.path.append('../')
import WAR_utils as wu

class utilsTest(unittest.TestCase):
    nTest = 10
    def testsInterval(self):
        for i in range(self.nTest):
            leastInt = np.random.randint(1990,2020)
            interval = np.random.randint(0,10)
            sampleList = []
            #print([leastInt, leastInt+interval-1])
            for j in range(interval):
                sampleList.append({'season':leastInt+j})
            try:
                res = wu.getSeasonInterval(sampleList)
            #print(res)
                self.assertEqual(res,[leastInt, leastInt+interval-1])
            except Exception:
                pass
    def testdictolist(self):
        for i in range(self.nTest):
            leastInt = np.random.randint(1990,2020)
            interval = np.random.randint(0,10)
            sampleList = []
            #print([leastInt, leastInt+interval-1])
            for j in range(interval):
                sampleList.append({'season':leastInt+j,'testcase':j})
            try:
                targetDict = wu.DictoList(sampleList,[leastInt, leastInt+interval-1])
                print(targetDict)
            except Exception:
                pass
            except IndexError:
                pass
            

if __name__=='__main__':
    test = unittest.makeSuite(utilsTest,'test')
    run = unittest.TextTestRunner()
    run.run(test)