# -*- coding: utf-8 -*-
import pandas as pd
import numpy as np
from data_parser.fangraph_parser import FangraphParser


class DataExport:
    def __init__(self, **opt):
        self.f_parser = FangraphParser(opt)
        self.w_data = self.f_parser.get_db()

    def get_stat(self, stat):
        # data frame initialization
        frame_dict = {'player_id': [], 'player_name': []}
        for stat_name in stat:
            for year in self.f_parser.season:
                frame_dict[stat_name+'_'+str(int(year))] = []
                
        for i in range(len(self.w_data)):
            data = self.w_data[i]['data']
            # dictionary
            new_data = {'playerid': self.w_data[i]['playerid'],
            'Name': data[0]['Name'], 'data': []}
            # data frame
            frame_dict['player_id'].append(self.w_data[i]['playerid'])
            frame_dict['player_name'].append(data[0]['Name'])
            for key in frame_dict.keys():
                if 'player' not in key:
                    frame_dict[key].append(np.nan)
            for datum in data:
                new_feature = {'season': datum['season']}
                for s in stat:
                    if s in datum:
                        new_feature[s] = datum[s]
                        frame_dict[s+'_'+str(int(datum['season']))][-1] = datum[s]
                new_data['data'].append(new_feature)
            self.w_data[i] = new_data
        self.data_frame = pd.DataFrame(frame_dict)      

    def get_dictionary(self):
        return self.w_data
        
    def get_data_frame(self):
        return self.data_frame
