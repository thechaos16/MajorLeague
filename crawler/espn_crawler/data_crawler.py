# -*- coding: utf-8 -*-
"""
Created on Tue Mar 29 16:55:55 2016

@author: minkyu
"""

# for getting html file from url
from urllib.request import urlopen
from bs4 import BeautifulSoup
import chardet
from schedule_parser import ScheduleParser

class EspnCrawler():
    def __init__(self, interval):
        self.interval = ScheduleParser(interval[0], interval[1]).interval
        self.base_url_for_schedule = 'http://espn.go.com/mlb/schedule/_/date/'
        
    def run(self):
        game_list = []
        for date in self.interval:
            game_list += self.schedule_parser(date)
        
    def schedule_parser(self, date):
        date_url = self.base_url_for_schedule + str(date)
        url_date = self.url_parser(date_url)
        # print(url_date)
        return []
    
    # make url as string
    def url_parser(self, url):
        urldata = urlopen(url)
        # this encoding should be checked automatically
        data = urldata.read()
        encoding = chardet.detect(data)
        new_url_data = str(data.decode(encoding['encoding']))
        return new_url_data
    
    def play_by_play_parser(self, url):
        url_data = self.url_parser(url)
        soup = BeautifulSoup(url_data, 'lxml')
        valid_list = soup.find_all('table')
        is_valid = False
        valid_data = []
        # table parser
        for elm in valid_list:
            row_lists = elm.find_all('tr')
            one_inning = []
            for row in row_lists:
                new_row = list(row.find_all('td'))
                if len(new_row) != 0:
                    if 'Play-By-Play' in str(new_row[0]):
                        is_valid = True
                if is_valid:
                    if len(new_row) != 0:
                        one_inning.append(new_row)
                    else:
                        if len(one_inning) != 0:
                            valid_data.append(one_inning)
                            one_inning = []
        # parser each cell
        html_return = []
        for inning in valid_data:
            inn = []
            for data in inning:
                row = []
                for column in data:
                    column =  str(column)
                    parsed_column = column.split('<')
                    for elm in parsed_column:
                        if not elm.endswith('>') and elm != '':
                            real_data = elm.split('>')[1]
                            break
                    row.append(real_data)
                inn.append(row)
            html_return.append(inn)
        return html_return
        
       
if __name__=='__main__':
    mm = EspnCrawler([{'year':2015,'month':5,'day':10},{'year':2015,'month':5,'day':10}]) 
    # dd = mm.play_by_play_parser()
