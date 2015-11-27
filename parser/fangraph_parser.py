import os,sys
import math
import random
import utils

# class for fangraph csv parser
class fangraphs_parser:
    # constructor
    def __init__(self,opt):
        # option (dictionary) contains
        # mandatory:
        # season, batter/pitcher
        self.season = [0,0]
        if len(opt['season'])==1:
            self.season[0] = str(opt['season'])
            self.season[1] = str(opt['season'])
        else:
            
            self.season[0] = str(opt['season'][0])
            self.season[1] = str(opt['season'][1])
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

    # fileList
    def setFileList(self):
        for i in range(len(self.season)):
            templi = []
            fpath = '../data/fangraphs/'+self.season[i]+'/'+self.type
            contents = os.listdir(fpath)
            for j in range(len(contents)):
                templi.append(fpath+'/'+contents[j])
            self.fp.append(templi)
    def getFileList(self):
        return self.fp

    # background knowledge (later)
    def setBackground(self,t):
        if t == 'batter':
            self.bgknow = []
        elif t == 'pitcher':
            self.bgknow = []
    def getBackground(self):
        return self.bgknow

    # read file (return array of full files)
    def fReader(self):
        # if there is no file, set file list
        if len(self.fp)==0:
            self.setFileList()
        data =[]
        for i in range(len(self.fp)):
            templi = []
            for j in range(len(self.fp[i])):
                if not os.path.isfile(self.fp[i][j]):
                    print self.fp[i][j]+' does not exist!'
                    continue
                reader = open(self.fp[i][j],'r')
                # read line by line
                oneDB = []
                # header (field)
                fieldline = reader.readline()
                fieldline = fieldline.strip('\n')
                [field,ftype] = self.fParser(fieldline)
                oneDB.append(field)
                for line in reader:
                    # remove '\n' & '"'
                    line = line.strip('\n')
                    line = line.strip('"')
                    # parsing string into data
                    oneDB.append(self.lParser(line,field))
                templi.append(oneDB)
            data.append(templi)
        return data

    # field parser
    def fParser(self,fieldline):
        ftype = []
        tfield = fieldline.split('","')
        tfield[0] = tfield[0].split('"')[1]
        #for i in range(len(tfield)):
        #    bg = getBackground()            
        return [tfield,ftype]
    
    # line parser
    def lParser(self,line,field):
        # requirements:
        # type controller (e.g. 33.5% -> 0.335)
        # error finder (if integer in name, return error)
        lineDB = []
        tline = line.split('","')
        # consistency check
        ccheck = len(tline)==len(field)
        # modification
        for i in range(len(field)):
            if '%' in field[i]:
                tline[i] = tline[i].strip('%')
                if not utils.isNumber(tline[i]):
                    continue
                tline[i] = float(tline[i])/100.0
            else:
                # convert string to float
                if utils.isNumber(tline[i]):
                    tline[i] = float(tline[i])
        # error find (later)
        return tline

    # get database
    def getDB(self):
        return self.db
