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
                        tempp.append(ppp[0])
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
                        tempp.append(ppp[0])
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
    qqq = parser('http://scores.espn.go.com/mlb/playbyplay?gameId='+code+'&full=0&inning=0')
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

# save batter's batting result
def bresult(data,db,dd):
    # results [[away name, sws, swl],[home name, sws, swl]]
    result = [['',0,0],['',0,0]]
    for i in range(len(data)):
        if result[i%2][0]=='':
            result[i%2][0] = data[i][0][3+i%2]
        for j in range(len(data[i][1])):
            # ignore score line
            if data[i][1][j][0]>='0' and data[i][1][j][0]<='9':
                continue
            # events
            if 'single' in data[i][1][j]:
                temp = 'H'
            elif 'doubled' in data[i][1][j]:
                temp = '2B'
            elif 'ground rule double' in data[i][1][j]:
                temp = '2B'
            elif 'tripled' in data[i][1][j]:
                temp = '3B'
            elif 'homer' in data[i][1][j]:
                temp = 'HR'
            elif 'walk' in data[i][1][j]:
                temp = 'BB'
            elif 'hit by pitch' in data[i][1][j]:
                temp = 'BB'
            elif 'out' in data[i][1][j]:
                if 'struck' in data[i][1][j]:
                    if 'swinging' in data[i][1][j] or 'bunting' in data[i][1][j]:
                        temp = 'SO(s)'
                        result[i%2][1]+=1
                    else:
                        temp = 'SO(l)'
                        result[i%2][2]+=1
                else:
                    temp = 'O'
            elif 'error' in data[i][1][j]:
                temp = 'O'
            elif 'choice' in data[i][1][j]:
                temp = 'O'
            elif 'sacrifice' in data[i][1][j]:
                temp = 'S'
            else:
                continue
            # batter
            temp2 = data[i][1][j].split(' ')
            temp3 = temp2[0]+' '+temp2[1]
            # add to database
            if [temp3] in db:
                db[db.index([temp3])+1].append(temp)
            else:
                db.append([temp3])
                db.append([temp])
    return [db,result]

# result parser
def rp(text,data):
    checker = 0
    data[0] = data[0]+1
    if text!='S' and text!='BB':
        data[1] = data[1]+1
    if text=='H':
        data[2] = data[2]+1
        data[3] = data[3]+1
        data[4] = data[4]+1
    elif text=='BB':
        data[3] = data[3]+1
    elif text=='2B':
        data[2] = data[2]+1
        data[3] = data[3]+1
        data[4] = data[4]+2
    elif text=='3B':
        data[2] = data[2]+1
        data[3] = data[3]+1
        data[4] = data[4]+3
    elif text=='HR':
        data[2] = data[2]+1
        data[3] = data[3]+1
        data[4] = data[4]+4
    elif text=='SO(s)':
        data[5]+=1
    elif text=='SO(l)':
        data[6]+=1
    return data

# stat calculator
def scal(data):
    if data[0]==0:
        avg = 0
        obp = 0
        slg = 0
    else:
        if data[1]==0:
            avg = 0
            slg = 0
        else:
            avg = float(data[2])/float(data[1])
            slg = float(data[4])/float(data[1])
        obp = float(data[3])/float(data[0])
    return [round(avg,3),round(obp,3),round(slg,3)]



# appropriate matches
amatch = schedule()
#amatch = ['320713126']

# personal db
db = []
# teamm db
dbt = []

# number of games
nog = 0

for i in range(len(amatch)):
    # parsing data for appropriate matches
    matd = doom(amatch[i])
    if len(matd)!=0:
        nog = nog+1
        [db,result] = bresult(matd,db,amatch[i])
        ch = 0
        if(len(dbt)==0):
            dbt.append(result[0])
            dbt.append(result[1])
        else:
            for j in range(len(result)):
                for k in range(len(dbt)):
                    if result[j][0]==dbt[k][0]:
                        dbt[k][1]+=result[j][1]
                        dbt[k][2]+=result[j][2]
                        ch = 1
                        break
                if ch==0:
                    dbt.append(result[j])

f = file('team.txt','w')
f.write('team\tSO(s)\tSO(l)\n')
for i in range(len(dbt)):
    for j in range(len(dbt[i])):
        f.write(str(dbt[i][j])+'\t')
    f.write('\n')
f.close()

fresult = []
temp = []
# parsing data
for i in range(len(db)):
    if i%2==0:
        temp.append(db[i][0])
    else:
        dd = [0,0,0,0,0,0,0]
        for j in range(len(db[i])):
            dd = rp(db[i][j],dd)
        for j in range(len(dd)):
            temp.append(dd[j])
        fresult.append(temp)
        temp = []

f = file('player.txt','w')
f.write('name\tpa\tab\tH\tOB\tTB\tSO(s)\tSO(l)\n')
for i in range(len(fresult)):
    for j in range(len(fresult[i])):
        f.write(str(fresult[i][j])+'\t')
    f.write('\n')
f.close()


raw_input('Press enter')
