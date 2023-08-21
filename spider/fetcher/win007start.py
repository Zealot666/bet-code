import json
import random
import threading
import time
from concurrent.futures import ThreadPoolExecutor

import pymongo
import requests
from pyquery import PyQuery as pq

ips = []
failDateList = set()
urlList = []
failList = []
failListMap = {}
successMap = {}
success = {}
dataList = []
dataListYa = []
client = pymongo.MongoClient("localhost", 27017)
db = client["soccerData"]
col_oupei = db["win007daxiaoZaotest11"]

from faker import Faker

ua = Faker()


def header():
    """
    basic header
    :return:
    """
    return {'User-Agent': ua.user_agent()}


def get_timeList(year, startMon, endMon, days=222):
    timeList = []
    try:
        for m in range(startMon, endMon):
            if days == 222:
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


def getDayList(time, TypeA="daxiao"):
    proxy = ""
    try:
        url = "http://bf.win007.com/football/Over_" + time + ".htm"
        resp = requests.get(url, headers=header(), timeout=5)
        resp.encoding = 'gb18030'
        html = resp.text
        if "赛程赛果" not in html:
            failDateList.add(time)
        doc = pq(html)
        for tr in list(doc('tr').items())[1:]:
            tds = list(tr('td').items())
            if len(tds) == 10:
                try:
                    if tds[7] != "":
                        lianShai = tds[0].text().strip()
                        day = tds[1].text().split('日')[0]
                        hour = tds[1].text().split('日')[1]
                        matchTime = time[0:4] + "-" + time[4:6] + "-" + day.zfill(2) + " " + hour + ":00"
                        allBifeng = (tds[4].text().split('\n')[0], tds[4].text().split('\n')[2])
                        midBifeng = (tds[6].text().split('\n')[0], tds[6].text().split('\n')[2])
                        id = list(tds[9]('a').items())[0].attr('onclick')[9:-1]
                        urlList.append(
                            (id, matchTime, allBifeng[0], allBifeng[1], midBifeng, lianShai, "3", TypeA))
                except:
                    pass
    except Exception as ex:
        if "HTTPConnectionPool" in str(ex):
            print(ex)
            # delete_proxy(proxy)
        failDateList.add(time)
        print('getDayList error ', ex)
    return time


def get_urlList(timeList, typeA):
    global failDateList
    executor = ThreadPoolExecutor(max_workers=1)
    for data in executor.map(getDayList, timeList, [typeA] * len(timeList)):
        print("get page {} success".format(data))

    errTimes = 0
    while (failDateList and errTimes < 6):
        print(len(failDateList), "errorDateList")
        errorList = failDateList
        failDateList = set()
        errTimes += 1
        for data in executor.map(getDayList, errorList, [typeA] * len(errorList)):
            print("get page {} success".format(data))


def get_proxy():
    return requests.get("http://127.0.0.1:5010/get/", timeout=10).json()


def delete_proxy(proxy):
    requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))


def get_html(tul, typeA):
    html = ""
    retry_count = 3

    def get_proxy():
        return requests.get("http://127.0.0.1:5010/get/", timeout=10).json()

    def delete_proxy(proxy):
        requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))

    if ips != 0:
        proxy = ips[random.randint(0, len(ips) - 1)]
    else:
        proxy = get_proxy().get("proxy")

    proxies = {"http": "http://{}".format(proxy), "https": "https://{}".format(proxy)}
    while retry_count > 0:
        url = "http://vip.win007.com/OverDown_n.aspx?id=" + tul[0]
        try:
            resp = requests.get(url, proxies=proxies, headers=header(), timeout=8)
            # resp = requests.get(url, headers=header(), timeout=5)
            resp.encoding = 'utf-8'
            html = resp.text
            if resp.status_code != 200:
                delete_proxy(proxy)
                error = 1 / 0
            if "操作太频繁了，请先歇一歇" in html:
                error = 1 / 0
            if html != "":
                break
        except Exception as ex:
            if "HTTPConnectionPool" in str(ex):
                print("AAA", ex)
                delete_proxy(proxy)
            if "HTTPConnectionPool" not in str(ex):
                print("AA", ex)
            retry_count -= 1
            pass
    if "变化" not in html:
        if tul[0] + typeA not in successMap.keys() and tul[0] + typeA not in failListMap.keys():
            failList.append(tul)
            failListMap[tul[0] + typeA] = 1
    return html


def get_one_match(tul):
    proxy = ""
    typeA = tul[7]
    bifinglist = [tul[2], tul[3]]
    start = time.time()
    query = {"time": tul[1],
             "place": tul[0],
             "masterGoal": int(bifinglist[0]),
             "guestGoal": int(bifinglist[1]),
             "midMasterGoal": tul[4][0],
             "midGuestGoal": tul[4][1],
             "lianShai": tul[5]
             }
    html = ""
    try:
        html = get_html(tul, typeA)
        doc = pq(html)
        col = {}

        def getComCol(col, company, startInfo, entInfo):
            col["masterOdd_Start" + "_" + "Zao" + "_" + company] = float(startInfo[0])
            col["pankou_Start" + "_" + "Zao" + "_" + company] = (startInfo[1])
            col["guestOdd_Start" + "_" + "Zao" + "_" + company] = float(startInfo[2])
            col["masterOdd_End" + "_" + "Zao" + "_" + company] = float(entInfo[0])
            col["pankouOdd_End" + "_" + "Zao" + "_" + company] = (entInfo[1])
            col["guestOdd_End" + "_" + "Zao" + "_" + company] = float(entInfo[2])
            return col

        for tr in list(doc('tr').items()):
            tds = list(tr('td').items())
            if len(tds) == 12:
                if tds[0].text() != "":
                    try:
                        startInfo = [tds[2].text(), tds[3].text(), tds[4].text()]
                        entInfo = [tds[8].text(), tds[9].text(), tds[10].text()]
                        col = getComCol(col, tds[0].text(), startInfo, entInfo)
                    except:
                        pass

        if len(col) > 0:
            col_oupei.update_one(query,
                                 {'$set': col},
                                 upsert=True)
        end = time.time()
        print("one match time", end - start)
    except Exception as ex:
        if "HTTPConnectionPool" in str(ex):
            print("AAA", ex)
            try:
                delete_proxy(proxy)
            except:
                pass
        if "封" not in str(ex):
            if tul[0] + typeA not in successMap.keys() and tul[0] + typeA not in failListMap.keys():
                failList.append(tul)
                failListMap[tul[0] + typeA] = 1
        print("get one match error", ex)
    return tul[0]


def get_match(urlList):
    executor = ThreadPoolExecutor(max_workers=32)
    for data in executor.map(get_one_match, urlList):
        pass

def getIps():
    while True:

        ipUrl = "http://127.0.0.1:5010/all"
        resp = requests.get(ipUrl)
        global ips
        data = json.loads(resp.text)
        a = []
        for i in data:
            if i['https'] == False:
                a.append(i['proxy'])
        ips = a
        time.sleep(1)

if __name__ == '__main__':
    t = threading.Thread(target=getIps)
    t.setDaemon(True)
    t.start()
    start = time.time()
    timeList = []
    # timeList += get_timeList(2014, 8, 13)
    # timeList += get_timeList(2015, 1, 13)
    # timeList += get_timeList(2016, 1, 13)
    # timeList += get_timeList(2017, 1, 13)
    # timeList += get_timeList(2018, 1, 13)
    # timeList += get_timeList(2019, 1, 13)
    # timeList += get_timeList(2020, 1, 13)
    timeList += get_timeList(2021, 11, 12)
    get_urlList(timeList, "oupei")
    col_insert = col_oupei
    print(len(urlList), "urlList")
    newList = []
    res = col_insert.find()
    map = {}
    for item in res:
        map[item["place"]] = 1
    for tul in urlList:
        if tul[0] not in map.keys():
            newList.append(tul)
    print(len(newList), "newList")
    get_match(newList)
    errTimes = 0
    while (failList and errTimes < 20):
        print(len(failList), "failList")
        errorList = failList
        failList = []
        failListMap = {}
        errTimes += 1
        get_match(errorList)
    end = time.time()
    print("find allMatch time consume: ", end - start)
