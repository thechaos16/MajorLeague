import os,sys
sys.path.append('../parser')
import fangraph_parser as fp

# this class exports data by name of stat
# output format is {pid {season, stats}}
class dataExport:
    def __init__(self,opt):
        self.fparser = fp.fangraphs_parser(opt)
        self.wData = self.fparser.getDB()

    def getStat(self,stat):
        for i in range(len(self.wData)):
            mm = self.wData[i]['data']
            newData = {'playerid':self.wData[i]['playerid'],'Name':mm[0]['Name'],'data':[]}
            for j in range(len(mm)):
                newadder = {'season':mm[j]['season']}
                for s in stat:
                    if s in mm[j]:
                        newadder[s] = mm[j][s]
                newData['data'].append(newadder)
            self.wData[i] = newData

    def getDB(self):
        return self.wData
