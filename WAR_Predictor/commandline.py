import data_gathering as dg

aa = dg.dataExport({'season':[2014,2015],'type':'batter'})
aa.getStat(['WAR'])
mm = aa.getDB()
