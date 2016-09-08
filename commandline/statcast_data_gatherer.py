# -*- coding: utf-8 -*-
import sys
import json
import os
sys.path.append('../')
from crawler.baseball_savant_crawler.data_crawler import URLHandler


def data_gatherer(**args):
    return_dict = {}
    url_handler = URLHandler(url=args['url'])
    year_interval = args['year']
    for year in year_interval:
        year_dict = {}
        if args['player_type'] == 'both':
            url_handler.update_url(url=args['url'], year=year, 
                                   abs=args['abs'], player_type='pitcher')
            year_dict['pitcher'] = url_handler.data_from_baseball_savant()
            url_handler.update_url(url=args['url'], year=year, 
                                   abs=args['abs'], player_type='batter')
            year_dict['batter'] = url_handler.data_from_baseball_savant()
        else:
            url_handler.update_url(url=args['url'], year=year, 
                                   abs=args['abs'], player_type=args['pitcher_type'])
            year_dict[args['pitcher_type']] = url_handler.data_from_baseball_savant()
        return_dict[str(year)] = year_dict
    return return_dict


def data_storage(data, args):
    if args['type'] == 'file_system':
        base_dir = args['dir']
        for year in data.keys():
            json.dump(data[year], open(os.path.join(base_dir, year+'.json'),'w'))
    else:
        raise NotImplementedError()


if __name__ == '__main__':
    base_url = 'https://baseballsavant.mlb.com/statcast_leaderboard'
    ans = data_gatherer(url=base_url, abs=100, year=[2015, 2016], player_type='both')
    data_storage(ans, {'type': 'file_system', 'dir': 'C:\git_project\MajorLeague\data\statcast'})
