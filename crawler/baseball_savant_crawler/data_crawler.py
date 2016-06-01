# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 16:55:55 2016

@author: minkyu
"""

# for getting html file from url
from urllib.request import urlopen
from bs4 import BeautifulSoup
import chardet
import json

class URLHandler():
    def __init__(self, **kwargs):
        if 'url' not in kwargs:
            raise KeyError('URL should be in input argument!')
        self.url = str(kwargs['url'])
        if len(kwargs) >= 2:
            self.url += '?'
        for key, data in kwargs.items():
            if key == 'url':
                continue
            self.url += (key + '=' + str(data) + '&')
        self.urldata = urlopen(self.url)
    
    # make url as string
    def url_parser(self):
        # this encoding should be checked automatically
        data = self.urldata.read()
        encoding = chardet.detect(data)
        new_url_data = str(data.decode(encoding['encoding']))
        return new_url_data
    
    # statcast
    # it returns list of dictionary
    def data_from_baseball_savant(self):
        url_data = self.url_parser()
        soup = BeautifulSoup(url_data, 'lxml')
        valid_list = soup.find_all('script')
        for elm in valid_list:
            if 'leaderboard_data' in str(elm):
                data = str(elm).split('leaderboard_data = ')[1].split('</script>')[0]
                data = data.replace('\n','')
                data = data.replace(';','')
        return json.loads(data)
            
    # put refined data into DB
    def store_db(self, db_path):
        pass
       
if __name__=='__main__':
    url = 'https://baseballsavant.mlb.com/statcast_leaderboard'
    mm = URLHandler(url = url, year = 2016, abs = 100, player_type = 'pitcher')
    dd = mm.data_from_baseball_savant()
