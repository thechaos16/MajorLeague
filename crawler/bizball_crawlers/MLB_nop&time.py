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
        return [-1,-1,-1]

    res = []

    if 'Game Time' not in data:
        return [-1,-1,-1]

    # game time
    edata = data.split('Game Time')[1]
    edata = edata.split('</td>')[1]
    tres = edata.split('>')[1]

    if(tres=='NA'):
        return [-1,-1,-1]
    if('delay' in tres):
        tres = tres.split(' ')[0]
        tres = tres.strip(',')

    ti = tres.split(':')
    res.append(int(ti[0])*60+int(ti[1]))

    # number of pitches
    pdata = data.split('Totals')
    res.append(int(pdata[1].split('</th><th>')[7]))
    res.append(int(pdata[3].split('</th><th>')[7]))

    #[play time,home team pitched,away team pitched]
    return res

# data of one match
def doom(code):
    #qqq = parser('http://scores.espn.go.com/mlb/playbyplay?gameId=330520108&full=1&inning=0')
    qqq = parser('http://scores.espn.go.com/mlb/boxscore?gameId='+code)
    return qqq

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
        
    return res



# appropriate matches
amatch = schedule()
#amatch = ['330716132']

nog = len(amatch)

f = file('result.txt','w')
f.write('GT\tHnop\tAnop\n')

for i in range(len(amatch)):
    # parsing data for appropriate matches
    matd = doom(amatch[i])
    if(matd[0]!=-1):
        f.write(str(matd[0])+'\t'+str(matd[1])+'\t'+str(matd[2])+'\n')
    else:
        nog-=1

f.write(str(nog))
f.close()

raw_input('Press enter')
