# -*- coding: utf-8 -*-
import os,sys
import numpy as np
import data_parser.utils as utils

# class for fangraph csv parser
class FangraphParser:
    # constructor
    def __init__(self,opt):
        # option (dictionary) contains
        # mandatory:
        # season, batter/pitcher
        self.season = []
        if len(opt['season'])==1:
            self.season.append(str(opt['season'][0]))
            #self.season[1] = str(opt['season'])
        else:            
            self.season = np.linspace(opt['season'][0],opt['season'][1],opt['season'][1]-opt['season'][0]+1)
            for i in range(len(self.season)):
                self.season[i] = np.uint(self.season[i])
        # batter or pitcher
        self.type = opt['type']
        # options:
        # position, file path, etc (tbd)
        if 'postion' in opt:
            self.position = opt['position']
        else:
            self.position = 'NULL'
        if 'file' in opt:
            self.fp = opt['file']
        else:
            self.fp = []
        # initialize DB
        # DB structure
        # [season] -> [each files] -> [each line]
        self.db = []

    # option handler
    def option_handler(self):
        return ''

    # fileList
    def set_file_list(self):
        for i in range(len(self.season)):
            temp_list = []
            file_path = '../data/fangraphs/'+str(np.uint(self.season[i]))+'/'+self.type
            contents = os.listdir(file_path)
            for j in range(len(contents)):
                temp_list.append(file_path+'/'+contents[j])
            self.fp.append(temp_list)
            
    def get_file_list(self):
        return self.fp

    # background knowledge (later)
    def set_background(self,t):
        if t == 'batter':
            self.background_knowledge = []
        elif t == 'pitcher':
            self.background_knowledge = []
    def get_background(self):
        return self.background_knowledge

    # read file (return array of full files)
    def file_reader(self):
        # if there is no file, set file list
        if len(self.fp)==0:
            self.set_file_list()
        data =[]
        for i in range(len(self.fp)):
            temp_list = []
            for j in range(len(self.fp[i])):
                if not os.path.isfile(self.fp[i][j]):
                    print(self.fp[i][j]+' does not exist!')
                    continue
                reader = open(self.fp[i][j],'r',encoding='utf-8')
                # read line by line
                oneDB = []
                # header (field)
                field_line = reader.readline()
                field_line = field_line.strip('\n')
                field_line = field_line.strip('"')
                [field,field_type] = self.field_parser(field_line)
                oneDB.append(field)
                for line in reader:
                    # remove '\n' & '"'
                    line = line.strip('\n')
                    line = line.strip('"')
                    # parsing string into data
                    oneDB.append(self.line_parser(line,field))
                temp_list.append(oneDB)
            data.append(temp_list)
        return data

    # field parser
    def field_parser(self,field_line):
        field_type = []
        field = field_line.split('","')
        field[0] = field[0].split('"')[1]
        #for i in range(len(tfield)):
        #    bg = getBackground()            
        return [field,field_type]
    
    # line parser
    def line_parser(self,line,field):
        # requirements:
        # type controller (e.g. 33.5% -> 0.335)
        # error finder (if integer in name, return error)
        temp_line = line.split('","')
        # consistency check
        ccheck = len(temp_line)==len(field)
        # modification
        for i in range(len(field)):
            if '%' in field[i]:
                temp_line[i] = temp_line[i].strip('%')
                if not utils.is_number(temp_line[i]):
                    continue
                temp_line[i] = float(temp_line[i])/100.0
            else:
                # convert string to float
                if utils.is_number(temp_line[i]):
                    temp_line[i] = float(temp_line[i])
        # error find (later)
        return temp_line

    # csv join
    def join(self):
        # raw data
        raw_data = self.file_reader()
        self.db = []
        for i in range(len(raw_data)):
            # get joined data by year
            joined = self.join_one_year(raw_data[i])
            # season info
            sInfo = self.season[i]
            # each data
            for player in joined:
                # add season data
                player['season'] = sInfo
                # check if player is in the dictionary or not
                check = 0
                for j in range(len(self.db)):
                    if self.db[j]['playerid']==player['playerid']:
                        del player['playerid']
                        self.db[j]['data'].append(player)
                        check = 1
                        break
                if check==0:
                    temp_dict = dict()
                    temp_dict['playerid'] = player['playerid']
                    del player['playerid']
                    temp_dict['data'] = [player]
                    self.db.append(temp_dict)
                
    # join for same year data
    def join_one_year(self,data):
        merged = []
        key = 'playerid'
        id_idx = []
        # merge
        temp_header = []
        # merge header & find index of key
        for i in range(len(data)):
            if key in data[i][0]:
                id_idx.append(data[i][0].index(key))
                temp_header = temp_header + data[i][0]
            else:
                print(data[i][0])
                id_idx.append(-1)
        merged.append(temp_header)
        # merge data
        for i in range(1,len(data[0])):
            current_key = data[0][i][id_idx[0]]
            current_data = data[0][i]
            # find matched data
            for j in range(1,len(data)):
                if id_idx[j]==-1:
                    continue
                check = 0
                for k in range(1,len(data[j])):
                    if data[j][k][id_idx[j]]==current_key:
                        current_data = current_data+data[j][k]
                        check = 1
                        break
                if check==0:
                    junkli = []
                    for k in range(len(data[j][0])):
                        junkli.append('')
                    current_data = current_data+junkli
            merged.append(current_data)
        # remove redundant fields
        # find redundant indices
        new_idx = []
        bad_idx = []
        for i in range(len(merged[0])):
            if merged[0][i] in new_idx:
                bad_idx.append(i)
                continue
            new_idx.append(merged[0][i])
        # remove redundant indecs
        final = []
        for i in range(len(merged)):
            for j in range(len(bad_idx)):
                del merged[i][bad_idx[j]-j]
            if i==0:
                continue
            #temptuple = zip(merged[0],merged[i])
            final.append(dict(zip(merged[0],merged[i])))
        return final
        

    # get database
    def get_db(self):
        self.join()
        return self.db
