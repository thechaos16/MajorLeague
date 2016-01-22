# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

import WAR_Predictor.data_gathering as dg
import WAR_Predictor.training as tr
import numpy as np
#import WAR_utils as wu
#import sim_check as si

aa = dg.dataExport({'season':[2006,2015],'type':'batter'})
aa.getStat(['WAR'])
mm = aa.getDB()

new_train = tr.WAR_Train(mm,'asdf',{'season':[2006,2015]})

## manual splitter
test_idx = int(len(new_train.w_data)*2/3)
tt = new_train.w_data[1:test_idx]
ttest = new_train.w_data[test_idx:-1]

(prediction,evaluation) = new_train.byRegression(tt,ttest)
(prediction,evaluation) = newTR.bySimCheck(tt,ttest)

#print(np.mean(kk))


#li1 = wu.DictoList(mm[0]['data'],[2008,2015])
#li2 = wu.DictoList(mm[1]['data'],[2008,2015])
