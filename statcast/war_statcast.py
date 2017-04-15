# -*- coding: utf-8 -*-
import sys
import numpy as np
from sklearn.linear_model import Ridge
from data_parser.fangraph_parser import FangraphParser
from data_parser.statcast_parser import StatCastParser


class WARStatCast:
    def __init__(self, **args):
        self.data_args = args['data']
        self.fg_data = None
        self.sc_data = None
        if 'key' in args:
            self.main_key = args['key']
        else:
            self.main_key = 'WAR'
        
    def run(self):
        self.get_data()
        matched_data = self.join_data()
        corr = self.correlation(matched_data)
        importances = self.regression_weight(matched_data)
        return {'correlation': corr, 'importance': importances}
    
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
                        one_row[self.main_key.lower()] = data['data'][idx][self.main_key]
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
        corr_list = []
        for key in converted_data.keys():
            if key != self.main_key.lower():
                corr = np.corrcoef(np.array(converted_data[key]), 
                                            np.array(converted_data[self.main_key.lower()]))
                corr_list.append((key, np.min(corr)))
        return sorted(corr_list, key=lambda x:x[1], reverse=True)

    def regression_weight(self, matched_data):
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
        sorted_key = sorted(converted_data.keys())
        input_key = [key for key in sorted_key if key != self.main_key.lower()]
        x = [] 
        for key in input_key:
            # normalization
            numpy_data = normalization(np.array(converted_data[key]))      
            x.append(numpy_data)
        x = np.array(x).T
        y = normalization(np.array(converted_data[self.main_key.lower()]))
        regressor = Ridge(alpha=1.0, normalize=True)
        regressor.fit(x,y)
        sorted_result = np.array(input_key)[np.argsort(np.array(regressor.coef_))]
        sorted_result = sorted_result[::-1]
        coefficient = sorted(regressor.coef_, reverse = True)
        return [(sorted_result[i], coefficient[i]) for i in range(len(sorted_result))]


def normalization(numpy_data):
    numpy_data -= np.mean(numpy_data)
    if np.std(numpy_data) != 0:
        numpy_data /= np.std(numpy_data)
    return numpy_data


if __name__ == '__main__':
    war_instance = WARStatCast(data = {'season': [2015, 2015],
                                       'type': 'batter',
                                       'year': range(2015, 2016),
                                       'player_id': 'Name'}, key='HR')
    res = war_instance.run()
