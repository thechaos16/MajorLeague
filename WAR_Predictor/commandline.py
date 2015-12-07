import data_gathering as dg
import WAR_utils as wu
import sim_check as si

aa = dg.dataExport({'season':[2008,2015],'type':'batter'})
aa.getStat(['WAR'])
mm = aa.getDB()

li1 = wu.DictoList(mm[0]['data'],[2008,2015])
li2 = wu.DictoList(mm[1]['data'],[2008,2015])
