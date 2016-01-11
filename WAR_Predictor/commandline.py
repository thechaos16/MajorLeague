import data_gathering as dg
import training as tr
import numpy as np
#import WAR_utils as wu
#import sim_check as si

aa = dg.dataExport({'season':[2006,2015],'type':'batter'})
aa.getStat(['WAR'])
mm = aa.getDB()

newTR = tr.WAR_train(mm,'asdf',{'season':[2006,2015]})

## manual splitter
testIdx = int(len(newTR.wData)*2/3)
tt = newTR.wData[1:testIdx]
ttest = newTR.wData[testIdx:-1]

kk = newTR.bySimCheck(tt,ttest)

print(np.mean(kk))


#li1 = wu.DictoList(mm[0]['data'],[2008,2015])
#li2 = wu.DictoList(mm[1]['data'],[2008,2015])
