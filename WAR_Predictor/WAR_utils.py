import numpy as np

## utility functions for WAR predictor
def getSeasonInterval(dic):
    ## if given dictionary is empty
    if len(dic)==0:
        raise Exception('list is empty')
    ## if input is not a dictionary
    if type(dic)!=list:
        raise Exception('input should be a list')
    if type(dic[0])!=dict:
        raise Exception('list should contain a dictionary')
        
    ## initialize
    minSeason = 1000000
    maxSeason = 0
    try:
        for i in range(len(dic)):
            if int(dic[i]['season'])<=minSeason:
                minSeason = int(dic[i]['season'])
            if int(dic[i]['season'])>=maxSeason:
                maxSeason = int(dic[i]['season'])
        return [minSeason,maxSeason]
    except KeyError:
        raise KeyError('There is no season in dictionary!')

## convert dictionary to list
def DictoList(dic,seasonInterval):
    ## if given dictionary is empty
    if len(dic)==0:
        raise Exception('list is empty')
    nos = len(dic[0])-1
    try:
        minSeason = seasonInterval[0]
        maxSeason = seasonInterval[1]
    except IndexError:
        raise IndexError('seaonInterval should have lenght of 2')
    ## initialize list
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
