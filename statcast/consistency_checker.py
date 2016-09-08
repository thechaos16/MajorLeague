# -*- coding: utf-8 -*-
"""
Created on Thu Jun  2 21:07:03 2016

@author: thech
"""

import sys
try:
    from crawler.baseball_savant_crawler.data_crawler import URLHandler
except ImportError:
    sys.path.append('../')
    from crawler.baseball_savant_crawler.data_crawler import URLHandler


class ConsistencyChecker:
    def __init__(self, year_interval, position='all'):
        self.year_interval = year_interval
        self.position = position.lower()
        
    def read_data(self):
        if self.position == 'all':
            pass
        elif self.position == 'batter':
            pass
        elif self.position == 'pitcher':
            pass
        else:
            raise NotImplementedError()
            
    def consistency_checker(self):
        pass

    
if __name__ == '__main__':
    pass