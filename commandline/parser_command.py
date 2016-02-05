# -*- coding: utf-8 -*-
import sys

sys.path.append('../')

import data_parser.fangraph_parser as fp

opt = {'season':[2011,2015],'type':'batter'}

fparser = fp.FangraphParser(opt)
#kk = fparser.fReader()
pp = fparser.get_db()
