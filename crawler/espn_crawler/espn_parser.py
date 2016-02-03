# -*- coding: utf-8 -*-
"""
Created on Wed Feb  3 23:07:28 2016

@author: thech
"""

import time

class ScheduleParser():
    ## each time interval has a format of {year:aa,month:bb,day:cc}
    def __init__(self,start_interval,end_interval):
        self.month_day_dictionary = {1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}
        self.interval = self.interval_generator(start_interval,end_interval)
        
    def interval_generator(self,start_interval,end_interval):
        ## start should be earlier than end
        if self.time_comparison(end_interval,start_interval):
            raise ValueError('start date should be before end date')
        ## compare to current time
        cur_time = {}
        temp_local_time = time.localtime()
        cur_time['year'] = temp_local_time.tm_year
        cur_time['month'] = temp_local_time.tm_mon
        cur_time['day'] = temp_local_time.tm_mday
        if self.time_comparison(cur_time,start_interval):
            raise ValueError('start date should be before today')
        ## if end interval is future, update it with today
        if self.time_comparison(cur_time,end_interval):
            end_interval = cur_time.copy()
            
        interval_list = [self.time_dict_to_str(start_interval)]
        
        return interval_list
        
    ## if time1<time2, return True, otherwise, return False        
    def time_comparison(self,time1,time2):
        if time1['year']>time2['year']:
            return False
        if time1['month']>time2['month']:
            return False
        if time1['day']>time2['day']:
            return False        
        return True
        
    def time_dict_to_str(self,time_dict):
        time_str = str(time_dict['year'])
        if time_dict['month']<10:
            month_str = '0'+str(time_dict['month'])
        else:
            month_str = str(time_dict['month'])
        if time_dict['day']<10:
            day_str = '0'+str(time_dict['day'])
        else:
            day_str = str(time_dict['day'])
        time_str = time_str+month_str+day+str
        return time_str