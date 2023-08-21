import json
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
col_daxiao = db["win007Lastv1006-3"]
col_yapan = db["win007yapantest"]
col_oupei = db["win007oupeitest"]

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
        url = "http://bf.titan007.com/football/Over_" + time + ".htm"
        print(url)

        def get_proxy():
            return requests.get("http://127.0.0.1:5010/get/", timeout=10).json()

        proxy = get_proxy().get("proxy")
        proxies = {"http": "http://{}".format(proxy), "https": "https://{}".format(proxy)}

        resp = requests.get(url, headers=header(), timeout=5, proxies=proxies)
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
    executor = ThreadPoolExecutor(max_workers=32)
    for data in executor.map(getDayList, timeList, [typeA] * len(timeList)):
        print("get page {} success".format(data))

    errTimes = 0
    while (failDateList and errTimes < 20):
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

    # if ips != 0:
    #     proxy = ips[random.randint(0, len(ips) - 1)]
    # else:
    proxy = get_proxy().get("proxy")

    proxies = {"http": "http://{}".format(proxy), "https": "https://{}".format(proxy)}
    while retry_count > 0:
        url = "http://vip.titan007.com/changeDetail/overunder.aspx?id=" + tul[0] + "&companyid=3&l=0"
        if typeA == "yapan":
            url = "http://vip.titan007.com/changeDetail/handicap.aspx?id=" + tul[0] + "&companyid=3&l=0"
        if typeA == "oupei":
            url = "http://vip.titan007.com/changeDetail/1x2.aspx?id=" + tul[0] + "&companyid=3&l=0"
        try:
            resp = requests.get(url, proxies=proxies, headers=header(), timeout=8)
            # resp = requests.get(url, headers=header(), timeout=5)
            resp.encoding = 'gb18030'
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


def daxiao_num(x):
    x_list = str(x).split("/")
    num = 0
    for i in x_list:
        num += float(i)
    return (float(num) / len(x_list))


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
    url = "http://vip.titan007.com/changeDetail/overunder.aspx?id=" + tul[0] + "&companyid=3&l=0"
    try:
        html = get_html(tul, typeA)
        doc = pq(html)
        col = {}
        yapan = []
        for td in doc('td').items():
            if "即" in td.text():
                for a in td.parent().items():
                    yapan.append(a.text().strip().split())
        yapan = yapan[1:]
        if len(yapan) != 0:
            startInfo = yapan[len(yapan) - 1][:3]
            entInfo = yapan[0][:3]
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
            startInfo = yapan[len(yapan) - 1][:3]
            entInfo = yapan[0][:3]
            col["masterOdd_Start" + "_" + "Zhong" + "_" + tul[6]] = float(startInfo[0])
            col["pankou_Start" + "_" + "Zhong" + "_" + tul[6]] = (startInfo[1])
            col["guestOdd_Start" + "_" + "Zhong" + "_" + tul[6]] = float(startInfo[2])

            col["masterOdd_End" + "_" + "Zhong" + "_" + tul[6]] = float(entInfo[0])
            col["pankouOdd_End" + "_" + "Zhong" + "_" + tul[6]] = (entInfo[1])
            col["guestOdd_End" + "_" + "Zhong" + "_" + tul[6]] = float(entInfo[2])

        yapan = []
        for td in doc('td').items():
            if "滚" in td.text():
                for a in td.parent().items():
                    yapan.append(a.text().strip().split())

        yapan = yapan[1:]
        num = 0

        xiaList = []
        for i in yapan:
            xiaList.append(i)
            if i[0] == '中场':
                break

        numMap = {}

        for i in xiaList:
            numMap[i[1]] = 1
        old = xiaList[0][1]
        oldItem = xiaList[0]
        num = 1
        j = 0
        firstGoal = []
        for i in xiaList[1:]:
            j += 1
            if old != i[1]:
                firstGoal = oldItem
                num += 1
                if (num == len(numMap)):
                    break
            old = i[1]
            oldItem = i

        firstGoal = xiaList[j - 2]
        secondGoal = xiaList[j]
        print("secondGoal", secondGoal)
        if num == len(numMap) and len(numMap) >= 2:
            print("firstGoal", firstGoal, firstGoal[2], firstGoal[3], firstGoal[4])
            col["lastTime"] = firstGoal[0]
            col["lastBifeng"] = firstGoal[1]
            col["masterOdd_End" + "_" + "last" + "_" + tul[6]] = float(firstGoal[2])
            col["pankouOdd_End" + "_" + "last" + "_" + tul[6]] = (firstGoal[3])
            col["guestOdd_End" + "_" + "last" + "_" + tul[6]] = float(firstGoal[4])
        yapan = []
        for td in doc('td').items():
            if col["lastBifeng"] in td.text():
                for a in td.parent().items():
                    yapan.append(a.text().strip().split())
        yapan = yapan[1:]

        yapan2 = []
        for i in yapan:
            try:
                sum1 = 0
                for j in i[1].split('-'):
                    sum1 += int(j)
                if daxiao_num(i[3]) - sum1 == 0.5 and float(i[0]) >= float(col['lastTime']):
                    yapan2.append(i)
            except:
                pass
        info = yapan2[len(yapan2) - 1]
        print("lastBifeng75", info)
        col["lastTime75"] = info[0]
        col["masterOdd_End" + "_" + "75" + "_" + tul[6]] = float(info[2])
        col["pankouOdd_End" + "_" + "75" + "_" + tul[6]] = (info[3])
        col["guestOdd_End" + "_" + "75" + "_" + tul[6]] = float(info[4])

        yapan = []
        for td in doc('td').items():
            if "滚" in td.text():
                for a in td.parent().items():
                    info = a.text().strip().split()
                    try:
                        sum1 = 0
                        for j in info[1].split('-'):
                            sum1 += int(j)

                        if daxiao_num(info[3]) - sum1 == 0.5 and float(info[2]) >= 1.00 and float(info[0]) >= float(col['lastTime75']) \
                            and daxiao_num(info[3]) >= daxiao_num(col['pankouOdd_End_75_3']):
                            yapan.append(info)
                    except Exception as ex:
                        pass

        yapan = yapan[1:]
        info = yapan[len(yapan)-1]

        col["lastTime130"] = info[0]
        col["lastBifeng130"] = info[1]
        col["masterOdd_End" + "_" + "130" + "_" + tul[6]] = float(info[2])
        col["pankouOdd_End" + "_" + "130" + "_" + tul[6]] = info[3]
        col["guestOdd_End" + "_" + "130" + "_" + tul[6]] = float(info[4])


        list65 = []
        for i in xiaList:
            try:
                if int(i[0]) == 60:
                    list65.append(i)
            except:
                pass
        info = list65[0]
        col["lastBifeng60"] = info[1]
        col["masterOdd_End" + "_" + "60" + "_" + tul[6]] = float(info[2])
        col["pankouOdd_End" + "_" + "60" + "_" + tul[6]] = (info[3])
        col["guestOdd_End" + "_" + "60" + "_" + tul[6]] = float(info[4])

        list65 = []
        for i in xiaList:
            try:
                if int(i[0]) == 75:
                    list65.append(i)
            except:
                pass
        info = list65[0]
        col["lastBifeng752"] = info[1]
        col["masterOdd_End" + "_" + "752" + "_" + tul[6]] = float(info[2])
        col["pankouOdd_End" + "_" + "752" + "_" + tul[6]] = (info[3])
        col["guestOdd_End" + "_" + "752" + "_" + tul[6]] = float(info[4])

        yapan = []
        for td in doc('td').items():
            if "滚" in td.text():
                for a in td.parent().items():
                    yapan.append(a.text().strip().split())

        yapan = yapan[1:]

        list65 = []
        for i in yapan:
            try:
                if int(i[0]) == 15:
                    list65.append(i)
            except:
                pass
        info = list65[0]
        col["lastBifeng15"] = info[1]
        col["masterOdd_End" + "_" + "15" + "_" + tul[6]] = float(info[2])
        col["pankouOdd_End" + "_" + "15" + "_" + tul[6]] = (info[3])
        col["guestOdd_End" + "_" + "15" + "_" + tul[6]] = float(info[4])

        list65 = []
        for i in yapan:
            try:
                if int(i[0]) == 30:
                    list65.append(i)
            except:
                pass
        info = list65[0]
        col["lastBifeng30" \
            ""] = info[1]
        col["masterOdd_End" + "_" + "30" + "_" + tul[6]] = float(info[2])
        col["pankouOdd_End" + "_" + "30" + "_" + tul[6]] = (info[3])
        col["guestOdd_End" + "_" + "30" + "_" + tul[6]] = float(info[4])

        print("len130", len(col))

        if len(col) >= 37 and num == len(numMap) \
                and int(col["lastTime"]) <= int(col["lastTime75"]):
            print(col, query, len(col), len(query))
            if typeA == "daxiao":
                col_daxiao.update_one(query,
                                      {'$set': col},
                                      upsert=True)

        end = time.time()

        if len(col) >= 37:
            successMap[tul[0] + typeA] = 1
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
        if "封" not in str(ex):
            print("get one match error", ex, url)
    return tul[0]


def get_match(urlList):
    executor = ThreadPoolExecutor(max_workers=48)
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
        print(ips)
        time.sleep(1)


if __name__ == '__main__':
    start = time.time()
    timeList = []
    timeList += get_timeList(2016, 1, 13)
    timeList += get_timeList(2017, 1, 13)
    timeList += get_timeList(2018, 1, 13)
    # timeList += get_timeList(2019, 1, 13)
    # timeList += get_timeList(2020, 1, 13)
    # timeList += get_timeList(2021, 1, 13)
    # timeList += get_timeList(2022, 1, 13)
    get_urlList(timeList, "daxiao")
    col_insert = col_daxiao
    print(len(urlList), "urlList")

    times = 1
    while times > 0:
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
        times -= 1
    end = time.time()
    print("find allMatch time consume: ", end - start)
