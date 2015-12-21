import numpy as np

## utility functions for WAR predictor
def getSeasonInterval(dic):
    minSeason = 1000000
    maxSeason = 0
    for i in range(len(dic)):
        if int(dic[i]['season'])<=minSeason:
            minSeason = int(dic[i]['season'])
        if int(dic[i]['season'])>=maxSeason:
            maxSeason = int(dic[i]['season'])
    return [minSeason,maxSeason]

'''def DictoList(dic):
    nos = len(dic[0])-1
    [minSeason,maxSeason] = getSeasonInterval(dic)
    li = []
    for j in range(maxSeason-minSeason+1):
        templi = range(nos)
        for i in range(len(templi)):
            templi[i]=0
        li.append(templi)
    keyset = dic[0].keys()
    for i in range(len(dic)):
        jj = 0
        for j in range(len(keyset)):
            if keyset[j]=='season':
                continue
            li[int(dic[i]['season'])-minSeason][jj] = dic[i][keyset[j]]
            jj+=1
    return li'''

def DictoList(dic,seasonInterval):
    nos = len(dic[0])-1
    minSeason = seasonInterval[0]
    maxSeason = seasonInterval[1]
    li = []
    for j in range(maxSeason-minSeason+1):
        templi = np.linspace(0,nos-1,nos)
        for i in range(len(templi)):
            templi[i]=0
        li.append(templi)
    #print [minSeason,maxSeason]
    keyset = list(dic[0])
    for i in range(len(dic)):
        jj = 0
        for j in range(len(keyset)):
            if keyset[j]=='season':
                continue
            if int(dic[i]['season'])-minSeason>=len(li):
                continue
            li[int(dic[i]['season'])-minSeason][jj] = dic[i][keyset[j]]
            jj+=1
    return li
