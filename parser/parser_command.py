import fangraph_parser as fp

opt = {'season':[2008,2015],'type':'batter'}

fparser = fp.fangraphs_parser(opt)
#kk = fparser.fReader()
pp = fparser.getDB()
