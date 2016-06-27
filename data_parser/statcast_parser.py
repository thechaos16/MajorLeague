# -*- coding: utf-8 -*-

import os,sys
import numpy as np
import json


class StatCastParser:
    def __init__(self, **args):
        if 'db' in args:
            self.db_path = args['db']
        else:
            self.db_path = '../data/statcast'
        if 'year' in args:
            year_list = [str(year) for year in args['year']]
            self.year = year_list
        else:
            self.year = 'all'
        if 'type' in args:
            self.position = args['type']
        else:
            self.year = 'both'
        self.data = {}
            
    def read_data(self):
        db_list = os.listdir(self.db_path)
        for file in db_list:
            year = file.split('.')[0]
            if self.year == 'all' or year in self.year:
                data_for_one_year = json.load(open(os.path.join(self.db_path, file), 'r'))
                self.data[year] = {}
                if self.position == 'batter' or self.position == 'both':
                    self.data[year]['batter'] = data_for_one_year['batter']
                elif self.position == 'pitcher' or self.position == 'both':
                    self.data[year]['pitcher'] = data_for_one_year['pitcher']
                    
    def get_data(self):
        self.read_data()
        return self.data
            

if __name__ == '__main__':
    sci = StatCastParser(year = range(2015, 2017), type = 'both')
    sci.read_data()