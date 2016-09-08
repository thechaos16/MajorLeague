# -*- coding: utf-8 -*-
from data_parser.fangraph_parser import FangraphParser


class DataExport:
    def __init__(self, opt):
        self.f_parser = FangraphParser(opt)
        self.w_data = self.f_parser.get_db()

    def get_stat(self, stat):
        # print len(self.wData[0]['data'])
        for i in range(len(self.w_data)):
            mm = self.w_data[i]['data']
            new_data = {'playerid': self.w_data[i]['playerid'],
            'Name': mm[0]['Name'], 'data': []}
            for j in range(len(mm)):
                new_feature = {'season': mm[j]['season']}
                for s in stat:
                    if s in mm[j]:
                        new_feature[s] = mm[j][s]
                new_data['data'].append(new_feature)
            self.w_data[i] = new_data

    def get_db(self):
        return self.w_data
