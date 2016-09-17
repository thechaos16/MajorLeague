# -*- coding: utf-8 -*-
import sys
sys.path.append('../')

from WAR_Predictor.data_handler.data_gathering import DataExport
from WAR_Predictor.training.training import WAR_Train
import numpy as np

aa = DataExport(season=[2011, 2015], type='batter')
aa.get_stat(['WAR'])
mm = aa.get_data_frame()

'''new_train = WAR_Train(mm, {'season': [2011, 2015]}, 'regression', True)

# manual splitter
test_idx = int(len(new_train.w_data)*2/3)
tt = new_train.w_data[1:test_idx]
ttest = new_train.w_data[test_idx:-1]

#(prediction,evaluation) = new_train.by_regression(tt,ttest)
(prediction,evaluation) = new_train.by_sim_check(tt,ttest,is_iter=True)'''
