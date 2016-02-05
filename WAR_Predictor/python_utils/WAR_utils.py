# -*- coding: utf-8 -*-
import numpy as np

## utility functions for WAR predictor
def get_season_interval(dic):
    ## if given dictionary is empty
    if len(dic)==0:
        raise Exception('list is empty')
    ## if input is not a dictionary
    if type(dic)!=list:
        raise Exception('input should be a list')
    if type(dic[0])!=dict:
        raise Exception('list should contain a dictionary')
        
    ## initialize
    min_season = 1000000
    max_season = 0
    try:
        for i in range(len(dic)):
            if int(dic[i]['season'])<=min_season:
                min_season = int(dic[i]['season'])
            if int(dic[i]['season'])>=max_season:
                max_season = int(dic[i]['season'])
        return [min_season,max_season]
    except KeyError:
        raise KeyError('There is no season in dictionary!')

## convert dictionary to list
def dict_to_list(dic,season_interval):
    ## if given dictionary is empty
    if len(dic)==0:
        raise Exception('list is empty')
    nos = len(dic[0])-1
    try:
        min_season = season_interval[0]
        max_season = season_interval[1]
    except IndexError:
        raise IndexError('seaonInterval should have lenght of 2')
    ## initialize list
    li = []
    for j in range(max_season-min_season+1):
        temp_list = np.linspace(0,nos-1,nos)
        for i in range(len(temp_list)):
            temp_list[i]=0
        li.append(temp_list)
    #print [minSeason,maxSeason]
    key_set = list(dic[0])
    for i in range(len(dic)):
        jj = 0
        for j in range(len(key_set)):
            if key_set[j]=='season':
                continue
            if int(dic[i]['season'])-min_season>=len(li) or int(dic[i]['season'])-min_season<0:
                continue
            li[int(dic[i]['season'])-min_season][jj] = dic[i][key_set[j]]
            jj+=1
    return li
