# -*- coding: utf-8 -*-

import sys
import pandas as pd
import numpy as np
from data_parser.statcast_parser import StatCastParser


def covariance_calculator(data_frame):
    # remove non-numerical columns
    data_frame = data_frame.convert_objects(convert_numeric=True)
    valid_columns = [field for field in data_frame.columns if data_frame[field].dtype!='object']
    #print(valid_columns)
    result = data_frame[valid_columns].corr()
    return result


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
    

def result_miner(cov_result):
    result = {}
    for field in cov_result.columns:
        one_series = cov_result[field]
        field_result = [(idx, one_series[idx]) for idx in one_series.index if idx!=field]
        result[field] = sorted(field_result, key=lambda x:x[1], reverse=True)
    return result
    

if __name__ == '__main__':
    data = statcase_data_parser({'season': [2015, 2015],
                                       'type': 'batter',
                                       'year': range(2015, 2016),
                                       'player_id': 'Name'})
    cov = covariance_calculator(data)
    print(cov)
