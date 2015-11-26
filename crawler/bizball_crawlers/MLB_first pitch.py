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
    #qqq = parser('http://scores.espn.go.com/mlb/playbyplay?gameId=330520108&full=1&inning=0')
    qqq = parser('http://scores.espn.go.com/mlb/playbyplay?gameId='+code+'&full=1&inning=0')
    return qqq

# analysis of first pitch
def afp(data):
    # number of hitter
    noh = 0
    # number of strikes
    nos = 0
    # number of balls
    nob = 0
    # number of swings (include struck by swinging and foul)
    nosw = 0
    # number of contacts (only in-play)
    noc = 0
    # number of contacts ab (remove sh sb)
    nocab = 0
    # number of hits
    nohit = 0
    # total bases
    tb = 0
    
    # all innings
    for i in range(len(data)):
        # all hitters in specific inning
        for j in range(len(data[i][1])):
            if j%4 == 1:
                if data[i][1][j-1][0]>='A' and data[i][1][j-1][0]<='z':
                    pp = 0
                    if 'ran for' in data[i][1][j][0] or 'hit for' in data[i][1][j][0]:
                        pp = pp+2
                    if data[i][1][j][pp][0:4]=='Ball':
                        nob = nob+1
                    elif data[i][1][j][pp][0:6]=='Strike':
                        nos = nos+1
                        temp = data[i][1][j][pp].split(',')[0]
                        if 'swing' in temp or 'foul' in temp:
                            nosw = nosw+1
                    else:
                        noc = noc+1
                        nosw = nosw+1
                        if 'sacrificed' not in data[i][1][j][pp]:
                            nocab = nocab+1
                            if 'singled' in data[i][1][j][pp]:
                                nohit = nohit+1
                                tb = tb+1
                            elif 'doubled' in data[i][1][j][pp]:
                                nohit = nohit+1
                                tb = tb+2
                            elif 'tripled' in data[i][1][j][pp]:
                                nohit = nohit+1
                                tb = tb+3
                            elif 'homered' in data[i][1][j][pp]:
                                nohit = nohit+1
                                tb = tb+4
                    noh = noh+1
            
    return [noh,nos+noc,nob,nosw,noc,nocab,nohit,tb]

# analysis of first pitch for rp
def afpr(data):
    # number of hitter
    noh = 0
    # number of strikes
    nos = 0
    # number of balls
    nob = 0
    # number of swings (include struck by swinging and foul)
    nosw = 0
    # number of contacts (only in-play)
    noc = 0
    # number of contacts ab (remove sh sb)
    nocab = 0
    # number of hits
    nohit = 0
    # total bases
    tb = 0

    cnt = 0

    check = 0
    # all innings
    for i in range(len(data)):
        # all hitters in specific inning
        for j in range(len(data[i][1])):
            if j%4 == 1:
                pp = 0
                if data[i][1][j-1][0]>='A' and data[i][1][j-1][0]<='z':
                    if 'ran for' in data[i][1][j][0] or 'hit for' in data[i][1][j][0]:
                        pp = pp+2
                    if check==1:
                        if data[i][1][j][pp][0:4]=='Ball':
                            nob = nob+1
                        elif data[i][1][j][pp][0:6]=='Strike':
                            nos = nos+1
                            temp = data[i][1][j][pp].split(',')[0]
                            if 'swing' in temp or 'foul' in temp:
                                nosw = nosw+1
                        else:
                            noc = noc+1
                            nosw = nosw+1
                            if 'sacrificed' not in data[i][1][j][pp]:
                                nocab = nocab+1
                                if 'singled' in data[i][1][j][pp]:
                                    nohit = nohit+1
                                    tb = tb+1
                                elif 'doubled' in data[i][1][j][pp]:
                                    nohit = nohit+1
                                    tb = tb+2
                                elif 'tripled' in data[i][1][j][pp]:
                                    nohit = nohit+1
                                    tb = tb+3
                                elif 'homered' in data[i][1][j][pp]:
                                    nohit = nohit+1
                                    tb = tb+4
                        noh = noh+1
                if len(data[i][1][j])==1:
                    if 'relieved' in data[i][1][j][0]:
                        check = 1
                    else:
                        check = 0
                # if rp comes after predecessor throws at least one pitch
                else:
                    check = 0
                    for kk in range(len(data[i][1][j])):
                        if 'relieved' in data[i][1][j][kk]:
                            if kk==len(data[i][1][j])-1:
                                check = 1
                            else:
                                cnt = cnt+1
                                if kk==len(data[i][1][j])-2:
                                    noc = noc+1
                                    nosw = nosw+1
                                    if 'sacrificed' not in data[i][1][j][pp]:
                                        nocab = nocab+1
                                        if 'singled' in data[i][1][j][pp]:
                                            nohit = nohit+1
                                            tb = tb+1
                                        elif 'doubled' in data[i][1][j][pp]:
                                            nohit = nohit+1
                                            tb = tb+2
                                        elif 'tripled' in data[i][1][j][pp]:
                                            nohit = nohit+1
                                            tb = tb+3
                                        elif 'homered' in data[i][1][j][pp]:
                                            nohit = nohit+1
                                            tb = tb+4
                                else:
                                    if data[i][1][j][pp][0]=='B':
                                        nob = nob+1
                                    else:
                                        nos = nos+1
                                        temp = data[i][1][j][pp].split(',')[0]
                                        if 'swing' in temp or 'foul' in temp:
                                            nosw = nosw+1
                                noh = noh+1
    return [noh,nos+noc,nob,nosw,noc,nocab,nohit,tb,cnt]

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
        games.append(codes[i].split('"')[0])

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
        
    return res


# appropriate matches
amatch = schedule()
#amatch = ['330505123']

# results
res1 = [0,0,0,0,0,0,0,0]
res2 = [0,0,0,0,0,0,0,0]

cnt = 0

for i in range(len(amatch)):
    # parsing data for appropriate matches
    matd = doom(amatch[i])

    # data analysis for first pitch ([entire first pitchs, strikes, balls, swings, contacts, at bats, hits, total bases])
    t1 = afp(matd)
    for pp in range(len(res1)):
        res1[pp] = res1[pp]+t1[pp]

    # data analysis for pitcher's first pitch ([entire first pitchs, strikes, swings, balls, contacts, at bats, hits, total bases])
    t2 = afpr(matd)
    cnt = cnt + t2[len(t2)-1]
    for pp in range(len(res2)):
        res2[pp] = res2[pp]+t2[pp]

    if i%1000==0:
        kk = file('result'+str(i/1000)+'.txt','w')
        for j in range(len(res1)):
            kk.write(str(res1[j])+' ')
        kk.write('\n')
        for j in range(len(res2)):
            kk.write(str(res2[j])+' ')
        kk.close()

kk = file('final result.txt','w')
# result for first pitch
for j in range(len(res1)):
    kk.write(str(res1[j])+' ')
kk.write('\n')
# result for rp's first pitch
for j in range(len(res2)):
    kk.write(str(res2[j])+' ')
# number of games
kk.write('\n')
kk.write('Number of games : '+str(len(amatch)))
kk.write('\n')
# number of relievers who came after predecessor threw first pitch
kk.write('Number of rp : '+str(cnt))
kk.close()
   
raw_input('Press enter')
