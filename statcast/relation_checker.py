# -*- coding: utf-8 -*-

import sys
import pandas as pd
import numpy as np
try:
    from data_parser.statcast_parser import StatCastParser
except ImportError:
    sys.path.append('../')
    from data_parser.statcast_parser import StatCastParser


def covariance_calculator(data_frame):
    # remove non-numerical columns
    data_frame = data_frame.convert_objects(convert_numeric=True)
    valid_columns = [field for field in data_frame.columns if data_frame[field].dtype!='object']
    #print(valid_columns)
    result = data_frame[valid_columns].corr()
    return valid_columns, result


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
    field_names, cov = covariance_calculator(data)
