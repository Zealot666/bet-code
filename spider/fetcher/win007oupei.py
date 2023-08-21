import time
from concurrent.futures import ThreadPoolExecutor

import pymongo
import requests
from pyquery import PyQuery as pq

ips = []


def get_timeList(year, startMon, endMon):
    try:
        timeList = []
        for m in range(startMon, endMon):
            if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
                days = 31
            elif m == 2:
                if int(year) % 4 == 0 and int(year) % 100 != 0:
                    days = 29
                else:
                    days = 28
            else:
                days = 30
            for day in range(1, days + 1):
                timeList.append(str(year) + str(m).zfill(2) + str(day).zfill(2))
    except Exception as ex:
        print("get date error", ex)
    return timeList


failDateList = set()

urlList = []


def getDayList(time):
    try:
        url = "http://bf.win007.com/football/Over_" + time + ".htm"
        resp = requests.get(url)
        resp.encoding = 'gb18030'
        doc = pq(resp.text)
        for tr in list(doc('tr').items())[1:]:
            tds = list(tr('td').items())
            if len(tds) == 10:
                try:
                    lianShai = tds[0].text().strip()
                    day = tds[1].text().split('日')[0]
                    hour = tds[1].text().split('日')[1]
                    matchTime = time[0:4] + "-" + time[4:6] + "-" + day.zfill(2) + " " + hour + ":00"
                    allBifeng = (tds[4].text().split('\n')[0], tds[4].text().split('\n')[2])
                    midBifeng = (tds[6].text().split('\n')[0], tds[6].text().split('\n')[2])
                    id = list(tds[9]('a').items())[0].attr('onclick')[9:-1]
                    urlList.append((id, matchTime, allBifeng[0], allBifeng[1], midBifeng, lianShai))
                except:
                    pass
    except Exception as ex:
        failDateList.add(time)
        print('getDayList error ', ex)
    return time


def get_urlList(timeList):
    global failDateList
    executor = ThreadPoolExecutor(max_workers=1)
    for data in executor.map(getDayList, timeList):
        print("get page {} success".format(data))

    errTimes = 0
    while (failDateList and errTimes < 6):
        errorList = failList
        failDateList = set()
        errTimes += 1
        for data in executor.map(getDayList, errorList):
            print("get page {} success".format(data))

    return urlList


client = pymongo.MongoClient("localhost", 27017)
db = client["soccerData"]
col_daxiao = db["win007Oupei"]

failList = []


def get_one_match(tul):
    try:
        bifinglist = [tul[2], tul[3]]

        query = {"time": tul[1],
                 "place": tul[0],
                 "masterGoal": int(bifinglist[0]),
                 "guestGoal": int(bifinglist[1]),
                 "midMasterGoal": int(tul[4][0]),
                 "midGuestGoal": int(tul[4][1]),
                 "lianShai": tul[5]
                 }

        url = ("http://1x2d.win007.com/" + tul[0] + ".js")
        resp = requests.get(url)
        resp.encoding = 'utf-8'
        oupei = ''
        for i in resp.text.split('\n')[:-2]:
            if 'game' in i:
                oupei = i
        oupei = oupei[15:-3].split('"')
        company = ['Bet 365', 'William Hill', 'Ladbrokes', '10BET', 'Interwetten', 'Vcbet', 'Crown', 'Macauslot',
                   'Easybets',
                   'Oddset']
        item = {}

        def get_odd(info):
            item["oupei_" + "start" + "_ma_" + info[0]] = float(info[1])
            item["oupei_" + "start" + "_pin_" + info[0]] = float(info[2])
            item["oupei_" + "start" + "_guest_" + info[0]] = float(info[3])
            item["oupei_" + "start" + "_ma_per_" + info[0]] = float(info[4])
            item["oupei_" + "start" + "_pin_per_" + info[0]] = float(info[5])
            item["oupei_" + "start" + "_guest_per_" + info[0]] = float(info[6])
            item["oupei_" + "start" + "_ret_per_" + info[0]] = float(info[7])

            item["oupei_" + "end" + "_ma_" + info[0]] = float(info[8])
            item["oupei_" + "end" + "_pin_" + info[0]] = float(info[9])
            item["oupei_" + "end" + "_guest_" + info[0]] = float(info[10])
            item["oupei_" + "end" + "_ma_per_" + info[0]] = float(info[11])
            item["oupei_" + "end" + "_pin_per_" + info[0]] = float(info[12])
            item["oupei_" + "end" + "_guest_per_" + info[0]] = float(info[13])
            item["oupei_" + "end" + "_ret_per_" + info[0]] = float(info[14])

        for i in oupei:
            if len(i) > 2:
                info = i.split('|')[2:]
                if info[0] in company:
                    get_odd(info)

        if len(item) != 0:
            col_daxiao.update_one(query,
                                  {'$set': item},
                                  upsert=True)
        print(item)
    except Exception as ex:
        failList.append(tul)
        print("get match error ", ex)
    return tul[0]


def get_match(urlList):
    executor = ThreadPoolExecutor(max_workers=8)
    for data in executor.map(get_one_match, urlList):
        print("get match {} success".format(data))


if __name__ == '__main__':
    start = time.time()
    timeList = []
    timeList += get_timeList(2016, 2, 13)
    timeList += get_timeList(2017, 1, 13)
    timeList += get_timeList(2018, 1, 13)
    timeList += get_timeList(2019, 1, 13)
    timeList += get_timeList(2020, 1, 13)
    timeList += get_timeList(2021, 1, 13)
    print(timeList)
    urlList = get_urlList(timeList)
    print(urlList)
    get_match(urlList)
    errTimes = 0
    while (failList and errTimes < 6):
        errorList = failList
        failList = []
        errTimes += 1
        get_match(errorList)
    end = time.time()
    print("find allMatch time consume: ", end - start)
