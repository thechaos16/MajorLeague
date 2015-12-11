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
        self.season = []
        if len(opt['season'])==1:
            self.season.append(str(opt['season'][0]))
            #self.season[1] = str(opt['season'])
        else:            
            self.season = range(opt['season'][0],(opt['season'][1]+1))
            for i in range(len(self.season)):
                self.season[i] = str(self.season[i])
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
    def optHander(self):
        return ''

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
                fieldline = fieldline.strip('"')
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

    # csv join
    def join(self):
        # raw data
        raw_data = self.fReader()
        self.db = []
        for i in range(len(raw_data)):
            # get joined data by year
            joined = self.join1year(raw_data[i])
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
                    tempdic = dict()
                    tempdic['playerid'] = player['playerid']
                    del player['playerid']
                    tempdic['data'] = [player]
                    self.db.append(tempdic)
                
    # join for same year data
    def join1year(self,data):
        merged = []
        key = 'playerid'
        ididx = []
        # merge
        tmpheader = []
        # merge header & find index of key
        for i in range(len(data)):
            if key in data[i][0]:
                ididx.append(data[i][0].index(key))
                tmpheader = tmpheader + data[i][0]
            else:
                print data[i][0]
                ididx.append(-1)
        merged.append(tmpheader)
        # merge data
        for i in range(1,len(data[0])):
            curKey = data[0][i][ididx[0]]
            curData = data[0][i]
            # find matched data
            for j in range(1,len(data)):
                if ididx[j]==-1:
                    continue
                check = 0
                for k in range(1,len(data[j])):
                    if data[j][k][ididx[j]]==curKey:
                        curData = curData+data[j][k]
                        check = 1
                        break
                if check==0:
                    junkli = []
                    for k in range(len(data[j][0])):
                        junkli.append('')
                    curData = curData+junkli
            merged.append(curData)
        # remove redundant fields
        # find redundant indices
        newidx = []
        badidx = []
        for i in range(len(merged[0])):
            if merged[0][i] in newidx:
                badidx.append(i)
                continue
            newidx.append(merged[0][i])
        # remove redundant indecs
        final = []
        for i in range(len(merged)):
            for j in range(len(badidx)):
                del merged[i][badidx[j]-j]
            if i==0:
                continue
            #temptuple = zip(merged[0],merged[i])
            final.append(dict(zip(merged[0],merged[i])))
        return final
        

    # get database
    def getDB(self):
        self.join()
        return self.db
