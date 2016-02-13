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
            
        interval_list = []
        cur_str = self.time_dict_to_str(start_interval)
        terminal_cond = self.time_dict_to_str(end_interval)
        while True:
            cur_str = self.time_validity_checker(cur_str)
            if int(cur_str)>int(terminal_cond):
                break
            interval_list.append(cur_str)
            cur_str = str(int(cur_str)+1)
        return interval_list
        
    ## if time1<time2, return True, otherwise, return False        
    def time_comparison(self,time1,time2):
        if time1['year']>time2['year']:
            return False
        elif time1['year']<time2['year']:
            return True
        if time1['month']>time2['month']:
            return False
        elif time1['month']<time2['month']:
            return True
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
        time_str = time_str+month_str+day_str
        return time_str
        
    def time_validity_checker(self,time_str):
        ## parse year as well in case of leap year
        ## for baseball, leap year doesn't count
        year = time_str[:4]
        month = time_str[4:6]
        day = time_str[6:]
        
        if int(day)>self.month_day_dictionary[int(month)]:
            new_month_str = int(month)+1
            if new_month_str<10:
                new_month_str = '0'+str(new_month_str)
            else:
                new_month_str = str(new_month_str)
            return year+new_month_str+'01'
        return time_str
        
if __name__=='__main__':
    test_instance = ScheduleParser({'year':2015,'month':5,'day':10},{'year':2015,'month':6,'day':30})