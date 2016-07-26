# -*- coding: utf-8 -*-

import sys
import pandas as pd
try:
    from data_parser.statcast_parser import StatCastParser
except ImportError:
    sys.path.append('../')
    from data_parser.statcast_parser import StatCastParser


def correlation_checker(data_frame, field1, field2):
    pass


def statcase_data_parser(data_args):
    sc_parser = StatCastParser(**data_args)
    sc_data = sc_parser.get_data()[str(data_args['season'][0])][data_args['type']]
    keys = sc_data[0].keys()
    key_dict = {key:[] for key in keys}
    for data in sc_data:
        for key in data.keys():
            key_dict[key].append(data[key])
    df = pd.DataFrame(key_dict)
    return df
    

if __name__ == '__main__':
    data = statcase_data_parser({'season': [2015, 2015],
                                       'type': 'batter',
                                       'year': range(2015, 2016),
                                       'player_id': 'Name'})
