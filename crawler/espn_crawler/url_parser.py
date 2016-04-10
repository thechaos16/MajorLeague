# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 19:09:27 2016

@author: thech
"""

## for getting html file from url
from urllib.request import urlopen
from html.parser import HTMLParser

class URLHandler(HTMLParser):
    def __init__(self, url):
        super().__init__()
        self.url = url
        self.urldata = urlopen(url)
        self.illegal_string_list = ['<','>','{','}','=','|',',']
    
    ## make url as string
    def url_parser(self):
        # it should be upgraded by auto-checking encoding
        new_url_data = str(self.urldata.read().decode('cp1251'))
        return new_url_data
        
    ## parse only data
    def handle_data(self, data):
        check = True
        for string in self.illegal_string_list:
            if string in data:
                check = False
                break
        if check:
            data = data.replace('\n','')
            data = data.replace('\t','')
            if len(set(data))>1:
                print(data)
       
if __name__=='__main__':
    mm = URLHandler('http://espn.go.com/mlb/playbyplay?gameId=350615102')
    #mm = URLHandler('https://docs.python.org/3/library/html.parser.html')
    
    dd = mm.url_parser()
    mm.feed(dd)    
    