# -*- coding: cp949 -*-
import os,sys,thread,Queue,sets
import httplib
import HTMLParser
import urllib2
import urlparse
import string
import math
import time
#import xlwt

# for schedule
months = ['January','Feburary','March','April','May','June','July','August','September','October','November','December']
dinm = [31,28,31,30,31,30,31,31,30,31,30,31]

def parser(url):
    # open url
    p = urllib2.urlopen(url)

    # read html source
    data = p.read()

    # remove all-stars
    if 'All-Stars' in data:
        return []

    # split data from script
    edata = data.split('Play-By-Play')[2]
    edata = edata.split('table')[2]
    tres = edata.split('thead')
    tres = tres[1:len(tres)-1]

    # rearrange data
    tres2 = []
    res = []
    # parsing
    for i in range(len(tres)):
        temp = tres[i].split('</tr>')
        tempp = []
        for j in range(len(temp)):
            # beginning of inning & pitcher who pitchs
            if '</th>' in temp[j]:
                kkk = temp[j].split('</th>')
                ppp = []
                for k in range(len(kkk)):
                    ppp = []
                    temppp = ''
                    for kk in range(len(kkk[k])):
                        if kkk[k][kk]=='>':
                            temppp = ''
                            continue
                        if kkk[k][kk]=='<':
                            if temppp!='':
                                ppp.append(temppp)
                        temppp = temppp+kkk[k][kk]
                        if kk==len(kkk[k])-1:
                            if temppp!='':
                                ppp.append(temppp)
                    if ppp!=[]:
                        tempp.append(ppp)
            # batting result
            if '</td>' in temp[j]:
                kkk = temp[j].split('</td>')
                for k in range(len(kkk)):
                    ppp = []
                    temppp = ''
                    for kk in range(len(kkk[k])):
                        if kkk[k][kk]=='>':
                            temppp = ''
                            continue
                        if kkk[k][kk]=='<':
                            if temppp!='':
                                ppp.append(temppp)
                        temppp = temppp+kkk[k][kk]
                        if kk==len(kkk[k])-1:
                            if temppp!='':
                                ppp.append(temppp)
                    if ppp!=[]:
                        tempp.append(ppp)
        if tempp!=[]:
            res.append(tempp)

    res2 = []
    temp = []
    for i in range(len(res)):
        temp.append(res[i])
        if i%3==2:
            res2.append(temp)
            temp = []
    
    return res2

# data of one match
def doom(code):
    url = 'http://scores.espn.go.com/mlb/playbyplay?gameId='+code+'&full=1&inning=0'
    #print url
    qqq = parser(url)
    return qqq

# number of pitches
def nopp(data):
    # results
    ares = ['',[]]
    hres = ['',[]]

    # current score buffer
    acs = 0
    hcs = 0

    # previosu pitchcnt
    ppitcnt = 0

    brake = 0
    # all innings
    for i in range(len(data)):
        # away team
        pitcnt = 0
        if i%2==0:
            # team name
            if ares[0]=='':
                ares[0] = data[i][0][3][0]

            # compute score at the end of inning
            ecs = int(data[i][1][len(data[i][1])-2][0])
            inscore = ecs-acs
            acs = ecs

            # all hitters
            for j in range(len(data[i][1])):
                if j%4==1:
                    if data[i][1][j-1][0]>='A' and data[i][1][j-1][0]<='z':
                        # to remove changing man or position line from data
                        check = 0
                        while 1:
                            if 'ejected' in data[i][1][j][check] or 'hit for' in data[i][1][j][check] or ' in ' in data[i][1][j][check]:
                                if len(data[i][1][j])!=1:
                                    check = check+2
                                    if len(data[i][1][j])<check+1:
                                        brake = 1
                                        break
                                else:
                                    brake = 1
                                    break
                            elif 'relieved' in data[i][1][j][check]:
                                if len(data[i][1][j])!=1:
                                    check = check+1
                                    if len(data[i][1][j])<check+1:
                                        brake = 1
                                        break
                                else:
                                    brake = 1
                                    break
                            else:
                                break

                        if brake!=1:
                            # if first pitch hasn't been hit
                            if 'Ball'==data[i][1][j][check][0:4] or 'Strike'==data[i][1][j][check][0:6]:
                                # split other balls and last ball
                                temp = data[i][1][j][check].split(',')
                                lll = len(temp)
                            else:
                                lll = 1
                                
                            pitcnt = pitcnt+lll
                        else:
                            brake = 0


            # result
            ares[1].append([ppitcnt,inscore])
            ppitcnt = pitcnt
                

        # home team
        else:
            # team name
            if hres[0]=='':
                hres[0] = data[i][0][4][0]

            # compute score at the end of inning
            ecs = int(data[i][1][len(data[i][1])-1][0])
            inscore = ecs-hcs
            hcs = ecs
            
            # all hitters
            for j in range(len(data[i][1])):
                if j%4==1:
                    if data[i][1][j-1][0]>='A' and data[i][1][j-1][0]<='z':
                        # to remove changing man or position line from data
                        check = 0
                        while 1:
                            if 'ejected' in data[i][1][j][check] or 'hit for' in data[i][1][j][check] or ' in ' in data[i][1][j][check]:
                                if len(data[i][1][j])!=1:
                                    check = check+2
                                    if len(data[i][1][j])<check+1:
                                        brake = 1
                                        break
                                else:
                                    brake = 1
                                    break
                            elif 'relieved' in data[i][1][j][check]:
                                if len(data[i][1][j])!=1:
                                    check = check+1
                                    if len(data[i][1][j])<check+1:
                                        brake = 1
                                        break
                                else:
                                    brake = 1
                                    break
                            else:
                                break

                        if brake!=1:
                            # if first pitch hasn't been hit
                            if 'Ball'==data[i][1][j][check][0:4] or 'Strike'==data[i][1][j][check][0:6]:
                                # split other balls and last ball
                                temp = data[i][1][j][check].split(',')
                                lll = len(temp)
                            else:
                                lll = 1
                                
                            pitcnt = pitcnt+lll
                        else:
                            brake = 0

            # result
            hres[1].append([ppitcnt,inscore])
            ppitcnt = pitcnt

    # [away name, away pitches, away pa], [home name, home pitches, home pa]
    res = [ares,hres]
     
    return res

# schedule checker
def scheck(code,date):
    temp = date.split(' ')
    if int(code[2:4])==months.index(temp[0])+1 and int(code[4:6])==int(temp[1]):
        return 1
    else:
        return 0

# schedule parser (url, today, tomorrow)
def sparser(data):
    [url,td,tm] = data
    
    # open url
    p = urllib2.urlopen(url)

    # read html source
    data = p.read()

    # games
    temp = data.split(td)
    glist = temp[len(temp)-1].split(tm)[0]

    codes = glist.split('boxscore?id=')
    games = []
    for i in range(1,len(codes)):
        temp2 = codes[i].split('"')[0]
        if scheck(temp2,td)==1:
            games.append(temp2)
 
    return games

# find match schedule
def schedule():
    y = []
    m = []
    d = []
    pp = time.localtime()
    while 'true':
        for i in range(2):
            y.append(int(raw_input('season?')))
            m.append(int(raw_input('month?')))
            d.append(int(raw_input('date?')))

        if y[1]>pp.tm_year:
            print 'error!'
            continue
        elif y[1]==pp.tm_year:
            if m[1]>pp.tm_mon:
                print 'error!'
                continue
            elif m[1]==pp.tm_mon:
                if d[1]>pp.tm_mday:
                    print 'error!'
                    continue

        if y[0]>y[1]:
            print 'error!'
        elif y[0]==y[1]:
            if m[0]>m[1]:
                print 'error!'
            elif m[0]==m[1]:
                if d[0]>d[1]:
                    print 'error!'
                else:
                    break
            else:
                break
        else:
            break

    # beginning of schdule
    if m[0]<10:
        tempm = '0'+str(m[0])
    else:
        tempm = str(m[0])
    if d[0]<10:
        tempd = '0'+str(d[0])
    else:
        tempd = str(d[0])
    tempday = str(y[0])+tempm+tempd
    inn = int(tempday)

    # end of schedule
    if m[1]<10:
        tempm = '0'+str(m[1])
    else:
        tempm = str(m[1])
    if d[1]<10:
        tempd = '0'+str(d[1])
    else:
        tempd = str(d[1])
    tempday = str(y[1])+tempm+tempd
    enn = int(tempday)

    res = []
    # basic url for schedule (day-by-day)
    while 1:
        if inn>enn:
            break

        today = months[int(str(inn)[4:6])-1]+' '+str(int(str(inn)[6:8]))
        if int(str(inn)[6:8])+1>dinm[int(str(inn)[4:6])-1]:
            if str(inn)[4:6]=='12':
                tomorrow = 'January 1'
            else:
                tomorrow = months[int(str(inn)[4:6])]+' 1'
        else:
            tomorrow = months[int(str(inn)[4:6])-1]+' '+str(int(str(inn)[6:8])+1)

        tempsch = sparser(['http://espn.go.com/mlb/schedule?date='+str(inn), today, tomorrow])
        for i in range(len(tempsch)):
            res.append(tempsch[i])
        
        inn = inn+1
        if int(str(inn)[6:8])>dinm[int(str(inn)[4:6])-1]:
            if int(str(inn)[4:6])<9:
                kkk = '0'+str(int(str(inn)[4:6])+1)
            else:
                kkk = str(int(str(inn)[4:6])+1)
            temp = str(inn)[0:4]+kkk+'01'
            inn = int(temp)
        if str(inn)[4:6]=='13':
            temp = str(int(str(inn)[0:4])+1)+'0101'
            inn = int(temp)
        
    return [res, y[0]]


# appropriate matches
tempsch = schedule()
amatch = tempsch[0]
#amatch = ['330429111']

# result [[team name,[nop,run,nop,run...]]
for i in range(len(amatch)):
    matd0 = doom(amatch[i])
    matd = nopp(matd0)

    contents = os.listdir('.')
    for j in range(len(matd)):
        if os.path.isfile(matd[j][0]+'.txt'):
            f = file(matd[j][0]+'.txt','a')
            for k in range(len(matd[j][1])):
                if matd[j][1][k][0]!=0:
                    f.write(str(matd[j][1][k][0])+'\t'+str(matd[j][1][k][1])+'\n')
            f.close()
        else:
            f = file(matd[j][0]+'.txt','w')
            f.write('time\tscore\n')
            for k in range(len(matd[j][1])):
                if matd[j][1][k][0]!=0:
                    f.write(str(matd[j][1][k][0])+'\t'+str(matd[j][1][k][1])+'\n')
            f.close()
   
raw_input('Press enter')
