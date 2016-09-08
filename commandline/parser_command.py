# -*- coding: utf-8 -*-
import sys

sys.path.append('../')
from data_parser.fangraph_parser import FangraphParser

opt = {'season':[2011,2015],'type':'batter'}

fparser = FangraphParser(opt)
pp = fparser.get_db()
