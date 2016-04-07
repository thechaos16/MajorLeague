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
    
    ## make url as string
    def url_parser(self):
        new_url_data = str(self.urldata.read().decode('cp1251'))
        return new_url_data
        
    ## parse only data
    def handle_data(self, data):
        if 'Perez' in data:
            print(data)
       
if __name__=='__main__':
    mm = URLHandler('http://espn.go.com/mlb/playbyplay?gameId=350615102')
    #mm = URLHandler('https://docs.python.org/3/library/html.parser.html')
    
    dd = mm.url_parser()
    mm.feed(dd)
    
    