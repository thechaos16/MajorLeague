# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import data_parser.fangraph_parser as fp

opt = {'season':[2006,2015],'type':'batter'}

fparser = fp.fangraphs_parser(opt)
#kk = fparser.fReader()
pp = fparser.getDB()
