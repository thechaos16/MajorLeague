# -*- coding: utf-8 -*-
"""
Created on Sat Feb 13 19:09:27 2016

@author: thech
"""
## for getting html file from url
from urllib.request import urlopen

class UrlParser():
    def __init__(self,url):
        self.urldata = urlopen(url)
        
    def html_parser(self):
        pass
    
    def table_parser(self):
        pass
    

if __name__=='__main__':
    pass