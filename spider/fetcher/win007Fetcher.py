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

client = pymongo.MongoClient("localhost", 27017)
db = client["soccerData"]
col_daxiao = db["win007daxiaov2"]
col_yapan = db["win007yapanv3"]
col_oupei = db["win007oupeiv3"]


def getIps():
    global ips
    while True:
        ipUrl = "http://127.0.0.1:5010/all"
        resp = requests.get(ipUrl)
        res = json.loads(resp.text)
        for i in res:
            ips.append(i['proxy'])
        print(ips)
        time.sleep(30)


def user_agent():
    """
    return an User-Agent at random
    :return:
    """
    ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/30.0.1599.101',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.71',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95',
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71',
        'Mozilla/4.0 (compatible; MSIE 6.0; Windows NT 5.1; SV1; QQDownload 732; .NET4.0C; .NET4.0E)',
        'Mozilla/5.0 (Windows NT 5.1; U; en; rv:1.8.1) Gecko/20061208 Firefox/2.0.0 Opera 9.50',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
    ]
    return random.choice(ua_list)


def header():
    """
    basic header
    :return:
    """
    return {'User-Agent': user_agent(),
            'Accept': '*/*',
            'Connection': 'keep-alive',
            'Accept-Language': 'zh-CN,zh;q=0.8'}


def get_timeList(year, startMon, endMon):
    timeList = []
    try:
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


def getDayList(time, TypeA="daxiao"):
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
                    for companyId in ["3"]:
                        urlList.append(
                            (id, matchTime, allBifeng[0], allBifeng[1], midBifeng, lianShai, companyId, TypeA))
                except:
                    pass
    except Exception as ex:
        failDateList.add(time)
        print('getDayList error ', ex)
    return time


def get_urlList(timeList, typeA):
    global failDateList
    executor = ThreadPoolExecutor(max_workers=8)
    for data in executor.map(getDayList, timeList, [typeA] * len(timeList)):
        print("get page {} success".format(data))
    errTimes = 0
    while (failDateList and errTimes < 6):
        errorList = failDateList
        failDateList = set()
        errTimes += 1
        for data in executor.map(getDayList, errorList, [typeA] * len(errorList)):
            print("get page {} success".format(data))
    return urlList


def get_one_match(tul):
    try:
        typeA = tul[7]
        bifinglist = [tul[2], tul[3]]

        query = {"time": tul[1],
                 "place": tul[0],
                 "masterGoal": int(bifinglist[0]),
                 "guestGoal": int(bifinglist[1]),
                 "midMasterGoal": tul[4][0],
                 "midGuestGoal": tul[4][1],
                 "lianShai": tul[5]
                 }

        def get_proxy():
            return requests.get("http://127.0.0.1:5010/get/").json()

        def getHtml(typeA):
            retry_count = 5
            while retry_count > 0:
                # proxy = get_proxy().get("proxy")
                proxy = ips[random.randint(0, len(ips) - 1)]
                proxies = {"http": "http://{}".format(proxy), "https": "https://{}".format(proxy)}
                try:
                    url = ""
                    if typeA == "yapan":
                        url = "http://vip.win007.com/changeDetail/handicap.aspx?id=" + tul[0] + "&companyid=" + tul[
                            6] + "&l=0"

                    if typeA == "daxiao":
                        url = "http://vip.win007.com/changeDetail/overunder.aspx?id=" + tul[0] + "&companyid=" + tul[
                            6] + "&l=0"

                    if typeA == "oupei":
                        url = "http://vip.win007.com/changeDetail/1x2.aspx?id=" + tul[0] + "&companyid=" + tul[
                            6] + "&l=0"

                    resp = requests.get(url, proxies=proxies, headers=header(), timeout=15)
                    resp.encoding = 'gb18030'
                    html = resp.text
                    if "操作太频繁了，请先歇一歇" in html:
                        print(html)
                        error = 1 / 0
                    return html
                except Exception:
                    retry_count -= 1
            return "操作太频繁了，请先歇一歇"

        html = getHtml(typeA)
        if "大小球变化表" not in html:
            failList.append(tul)
            return

        doc = pq(html)
        col = {}
        yapan = []
        for td in doc('td').items():
            if "即" in td.text():
                for a in td.parent().items():
                    yapan.append(a.text().strip().split())

        yapan = yapan[1:]
        if len(yapan) != 0:
            startInfo = yapan[0][:3]
            entInfo = yapan[len(yapan) - 1][:3]
            col["masterOdd_Start" + "_" + "Ji" + "_" + tul[6]] = float(startInfo[0])
            col["pankou_Start" + "_" + "Ji" + "_" + tul[6]] = (startInfo[1])
            col["guestOdd_Start" + "_" + "Ji" + "_" + tul[6]] = float(startInfo[2])
            col["masterOdd_End" + "_" + "Ji" + "_" + tul[6]] = float(entInfo[0])
            col["pankouOdd_End" + "_" + "Ji" + "_" + tul[6]] = (entInfo[1])
            col["guestOdd_End" + "_" + "Ji" + "_" + tul[6]] = float(entInfo[2])

        yapan = []
        for td in doc('td').items():
            if "中场" in td.text():
                for a in td.parent().items():
                    yapan.append(a.text().strip().split()[2:])

        yapan = yapan[1:]
        if len(yapan) != 0:
            startInfo = yapan[0][:3]
            entInfo = yapan[len(yapan) - 1][:3]
            col["masterOdd_Start" + "_" + "Zhong" + "_" + tul[6]] = float(startInfo[0])
            col["pankou_Start" + "_" + "Zhong" + "_" + tul[6]] = (startInfo[1])
            col["guestOdd_Start" + "_" + "Zhong" + "_" + tul[6]] = float(startInfo[2])
            col["masterOdd_End" + "_" + "Zhong" + "_" + tul[6]] = float(entInfo[0])
            col["pankouOdd_End" + "_" + "Zhong" + "_" + tul[6]] = (entInfo[1])
            col["guestOdd_End" + "_" + "Zhong" + "_" + tul[6]] = float(entInfo[2])

        if len(col) == 12:
            if typeA == "yapan":
                col_yapan.update_one(query,
                                     {'$set': col},
                                     upsert=True)

            if typeA == "daxiao":
                col_daxiao.update_one(query,
                                      {'$set': col},
                                      upsert=True)
            if typeA == "oupei":
                col_oupei.update_one(query,
                                     {'$set': col},
                                     upsert=True)
        print(col)
    except Exception as ex:
        if "封" not in str(ex):
            failList.append(tul)
        print("get match error ", ex)
    return tul[0]


def get_match(urlList):
    executor = ThreadPoolExecutor(max_workers=16)
    for data in executor.map(get_one_match, urlList):
        print("get match {} success".format(data))


class win007Fetcher():
    def getMatches(self, year, month, endMonth, typeA="daxiao"):
        global failList
        start = time.time()
        t = threading.Thread(target=getIps)
        t.setDaemon(True)
        t.start()
        time.sleep(5)
        timeList = get_timeList(year, month, endMonth)
        urlList = get_urlList(timeList, typeA)
        get_match(urlList)
        errTimes = 0
        while (failList and errTimes < 6):
            errorList = failList
            failList = []
            errTimes += 1
            get_match(errorList)
        end = time.time()
        print("find allMatch time consume: ", end - start)

    def getLastMonMatches(self):
        import time
        localtime = time.localtime(time.time())
        mon = localtime.tm_mon
        self.getMatches(localtime.tm_year, mon - 1, mon + 1, "daxiao")
