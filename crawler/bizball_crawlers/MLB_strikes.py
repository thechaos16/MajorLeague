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

# swing-and-hit percentage
def swp(data):
    # results (overall, first strike)
    # PA, BA, H, 2B, 3B, HR, BBHBP, SO, OUT
    overall = [0,0,0,0,0,0,0,0,0]
    fst = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]]
    
    brake = 0
    # all innings
    for i in range(len(data)):
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
                                check = check+2
                                if len(data[i][1][j])<check+1:
                                    brake = 1
                                    break
                            else:
                                brake = 1
                                break
                        else:
                            break

                    if brake!=1:
                        fchecker = [0,0,0,0,0]
                        overall[0]+=1
                        # if first pitch hasn't been hit
                        if 'Ball'==data[i][1][j][check][0:4]:
                            # split other balls and last ball
                            temp = data[i][1][j][check].split(',')
                            pitcnt = len(temp)
                            for pitch in range(min(pitcnt,5)):
                                if 'Strike' in temp[pitch]:
                                    fchecker[pitch]+=1
                                    fst[pitch][0]+=1
                        elif  'Strike'==data[i][1][j][check][0:6]:
                            # split other balls and last ball
                            temp = data[i][1][j][check].split(',')
                            pitcnt = len(temp)
                            for pitch in range(min(pitcnt,5)):
                                if 'Strike' in temp[pitch]:
                                    fchecker[pitch]+=1
                                    fst[pitch][0]+=1
                        else:
                            pitcnt = 1

                        # parsing the result
                        kk = check+1
                        # adjust for espn's error
                        oops = 0
                        if pitcnt==1:
                            kk = check
                            #fst[0]+=1
                            #fchecker = 1
                        else:
                            if len(data[i][1][j])==check+1:
                                oops = 1

                        # events
                        if oops==0:
                            if 'single' in data[i][1][j][kk]:
                                overall[1]+=1
                                overall[2]+=1
                                for ccc in range(5):
                                    if fchecker[ccc]==1:
                                        fst[ccc][1]+=1
                                        fst[ccc][2]+=1
                            elif 'doubled' in data[i][1][j][kk]:
                                overall[1]+=1
                                overall[3]+=1
                                for ccc in range(5):
                                    if fchecker[ccc]==1:
                                        fst[ccc][1]+=1
                                        fst[ccc][3]+=1
                            elif 'ground rule double' in data[i][1][j][kk]:
                                overall[1]+=1
                                overall[3]+=1
                                for ccc in range(5):
                                    if fchecker[ccc]==1:
                                        fst[ccc][1]+=1
                                        fst[ccc][3]+=1
                            elif 'tripled' in data[i][1][j][kk]:
                                overall[1]+=1
                                overall[4]+=1
                                for ccc in range(5):
                                    if fchecker[ccc]==1:
                                        fst[ccc][1]+=1
                                        fst[ccc][4]+=1
                            elif 'homer' in data[i][1][j][kk]:
                                overall[1]+=1
                                overall[5]+=1
                                for ccc in range(5):
                                    if fchecker[ccc]==1:
                                        fst[ccc][1]+=1
                                        fst[ccc][5]+=1
                            elif 'walk' in data[i][1][j][kk]:
                                overall[6]+=1
                                for ccc in range(5):
                                    if fchecker[ccc]==1:
                                        fst[ccc][6]+=1
                            elif 'hit by pitch' in data[i][1][j][kk]:
                                overall[6]+=1
                                for ccc in range(5):
                                    if fchecker[ccc]==1:
                                        fst[ccc][6]+=1
                            elif 'sacrifice' in data[i][1][j][kk]:
                                continue
                            elif 'struck' in data[i][1][j][kk]:
                                overall[1]+=1
                                overall[7]+=1
                                for ccc in range(5):
                                    if fchecker[ccc]==1:
                                        fst[ccc][1]+=1
                                        fst[ccc][7]+=1
                            else:
                                overall[1]+=1
                                overall[8]+=1
                                for ccc in range(5):
                                    if fchecker[ccc]==1:
                                        fst[ccc][1]+=1
                                        fst[ccc][8]+=1
                        else:
                            if data[i][1][j][check][len(data[i][1][j][check])-1]=='l':
                                if len(temp)>=4:
                                    overall[6]+=1
                                    for ccc in range(5):
                                        if fchecker[ccc]==1:
                                            fst[ccc][6]+=1
                            elif data[i][1][j][check][len(data[i][1][j][check])-1]==')':
                                if len(temp)>=3:
                                    overall[1]+=1
                                    overall[7]+=1
                                    for ccc in range(5):
                                        if fchecker[ccc]==1:
                                            fst[ccc][1]+=1
                                            fst[ccc][7]+=1
    
                        
                    else:
                        brake = 0

    return [overall,fst]

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

res = [0,0,0,0,0,0,0,0,0]
res2 = [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0]] 
for i in range(len(amatch)):
    # parsing data for appropriate matches
    matd = doom(amatch[i])
    aa = swp(matd)
    for j in range(len(aa[0])):
        res[j]+=aa[0][j]
    for j in range(len(aa[1])):
        for k in range(len(aa[1][0])):
            res2[j][k] += aa[1][j][k]

f = file(str(tempsch[1])+'_result.txt','w')
#f = file('asdf.txt','w')
f.write('PA\tBA\tH\t2B\t3B\tHR\tBBHBP\tSO\tOUT\n')
for j in range(len(res)):
    f.write(str(res[j])+'\t')
f.write('\n')
for i in range(len(res2)):
    for j in range(len(res2[i])):
        f.write(str(res2[i][j])+'\t')
    f.write('\n')
f.close()

raw_input('Press enter')
