# -*- coding: utf-8 -*-
from WAR_Predictor.data_handler.data_gathering import DataExport
from WAR_Predictor.training.training import WAR_Train

aa = DataExport(season=[2011, 2015], type='batter')
aa.get_stat(['WAR'])
mm = aa.get_data_frame()

new_train = WAR_Train(mm, {'season': [2011, 2015]}, 'regression', True)

(prediction, evaluation) = new_train.by_regression()
# (prediction, evaluation) = new_train.by_sim_check(tt, ttest, is_iter=True)
