# -*- coding: utf-8 -*-
"""
Created on Sat Feb  6 23:40:19 2016

@author: thech
"""

class FangraphsDownload():
    ## optinos include: batter/pitcher, position, specific stats
    def __init__(self,season,options=None):
        self.base_url = 'http://www.fangraphs.com/leaders.aspx'        
        self.season = season
        self.options = options
    
    def url_generator(self,is_batter,pos,stats_type,team):
        target_url = self.base_url
        ## formats for batter and pitcher are slightly different
        if is_batter:
            if pos is None:
                target_url+='?pos=all'
            else:
                target_url+='?pos='+pos
            target_url+='&stats=bat'
        else:
            target_url+='?pos=all'
            if pos is None:
                target_url+='&stats=pit'
            else:
                target_url+='&stats='+pos
        target_url+='&lg=all&qual=y&type='+str(stats_type)+'&season='+str(self.season)+'&month=0&season1='+str(self.season)+'&ind=0&team='
        if team is None:
            target_url+='0&rost=0&age=0&filter=&players=0'
        else:
            target_url+=str(team)+'&rost=0&age=0&filter=&players=0'