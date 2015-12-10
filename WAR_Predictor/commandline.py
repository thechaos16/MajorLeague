import data_gathering as dg
import training as tr
#import WAR_utils as wu
#import sim_check as si

aa = dg.dataExport({'season':[2006,2015],'type':'batter'})
aa.getStat(['WAR'])
mm = aa.getDB()

aa = tr.WAR_train(mm,'asdf',{'season':[2006,2015]})

## manual splitter
tt = aa.wData[1:len(aa.wData)*2/3]
ttest = aa.wData[len(aa.wData)*2/3:-1]

kk = aa.bySimCheck(tt,ttest)



#li1 = wu.DictoList(mm[0]['data'],[2008,2015])
#li2 = wu.DictoList(mm[1]['data'],[2008,2015])
