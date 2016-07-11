# -*- coding: utf-8 -*-

import sys
import numpy as np
import pandas as pd
try:
    from crawler.baseball_savant_crawler.data_crawler import URLHandler
except ImportError:
    sys.path.append('../')
    from crawler.baseball_savant_crawler.data_crawler import URLHandler
from data_parser.fangraph_parser import FangraphParser
from data_parser.statcast_parser import StatCastParser


class WARStatCast:
    def __init__(self, **args):
        self.data_args = args['data']
        self.fg_data = None
        self.sc_data = None
        
    def run(self):
        self.get_data()
        matched_data = self.join_data()
        corr = self.correlation(matched_data)
    
    def get_data(self):
        fg_parser = FangraphParser(self.data_args)
        self.fg_data = fg_parser.get_db()
        sc_parser = StatCastParser(**self.data_args)
        self.sc_data = sc_parser.get_data()
        
    def join_data(self):
        self.get_data()
        # use name as a key (because player id are differnt in statcast and fangraphs)
        matched_data = []
        for data in self.fg_data:
            player_id = data['data'][0][self.data_args['player_id']]
            for idx, year in enumerate(self.data_args['year']):
                statcast = self.sc_data[str(year)][self.data_args['type']]
                for sc in statcast:
                    id_for_sc = self.data_args['player_id'].lower()
                    if id_for_sc in sc and sc[id_for_sc] == player_id:
                        one_row = sc.copy()
                        one_row['war'] = data['data'][idx]['WAR']
                        matched_data.append(one_row)
        return matched_data
        
    def correlation(self, matched_data):
        converted_data = {}
        for i, data in enumerate(matched_data):
            if i==0:
                for key in data.keys():
                    try:
                        value = float(data[key])
                        converted_data[key] = [value]
                    except ValueError:
                        pass
            else:
                for key in data.keys():
                    if key in converted_data:
                        converted_data[key].append(float(data[key]))
        main_key = 'war'
        for key in converted_data.keys():
            if key != main_key:
                corr = np.corrcoef(np.array(converted_data[key]), np.array(converted_data[main_key]))
                print([np.min(corr), key])


if __name__ == '__main__':
    war_instance = WARStatCast(data = {'season': [2015, 2015],
                                       'type': 'batter',
                                       'year': range(2015, 2016),
                                       'player_id': 'Name'})
    war_instance.get_data()
    match = war_instance.join_data()