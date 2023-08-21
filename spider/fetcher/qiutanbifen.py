import asyncio
import json
import random
import threading
import time

import aiohttp
import motor.motor_asyncio
import requests
from async_timeout import timeout
from loguru import logger
from pyquery import PyQuery as pq

client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
db = client["soccerData"]
col_yapan = db["midYapan007"]
col_daxiao = db["midDaxiao007v3"]

urlAlllist = set()
failList = []
failUrlList = set()


def list_of_groups(init_list, childern_list_len):
    return [init_list[i:i + childern_list_len] for i in range(0, len(init_list), childern_list_len)]


async def chooseDay(time):
    async with timeout(120):
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
                        # if lianShai == "球会友谊":
                        #     continue
                        day = tds[1].text().split('日')[0]
                        hour = tds[1].text().split('日')[1]
                        matchTime = time[0:4] + "-" + time[4:6] + "-" + day.zfill(2) + " " + hour + ":00"
                        allBifeng = (tds[4].text().split('\n')[0], tds[4].text().split('\n')[2])
                        midBifeng = (tds[6].text().split('\n')[0], tds[6].text().split('\n')[2])
                        id = list(tds[9]('a').items())[0].attr('onclick')[9:-1]
                        for companyId in ["3"]:
                            urlAlllist.add((id, matchTime, allBifeng[0], allBifeng[1], midBifeng, lianShai, companyId))
                    except:
                        pass
            logger.debug("find day match success " + time)
        except asyncio.CancelledError as ex:
            logger.warning("find day match time out " + time + "{}", ex)
            global failList
            failList.append(time)
            return
        except Exception as ex:
            failList.append(time)
            logger.warning("find day match fail " + time + " {}", ex)
            return


async def fetch(session, tul, type):
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/79.0.3945.130 Chrome/79.0.3945.130 Safari/537.36'
    }
    newUrl = ""
    if type == "yapan":
        newUrl = "http://vip.win007.com/changeDetail/handicap.aspx?id=" + tul[0] + "&companyid=" + tul[6] + "&l=0"
    if type == "daxiao":
        newUrl = "http://vip.win007.com/changeDetail/overunder.aspx?id=" + tul[0] + "&companyid=" + tul[6] + "&l=0"
    content = ""
    times = 0
    while content == "" and times < 4:
        try:
            times += 1
            ip = ips[random.randint(0, len(ips) - 1)]
            print(ip)
            try:
                async with session.get(newUrl, headers=headers, timeout=7, proxy=ip) as response:
                    # content = await response.text(encoding='gb18030', errors='ignore')
                    content = await response.text()
                    if "操作太频繁了，请先歇一歇" in content:
                        content = ""
            except Exception as e:
                if "codec" in str(e):
                    content = await response.text(encoding='gb18030', errors='ignore')
                    print('codec', tul)
                    break
                failUrlList.add(tul)
                logger.warning("fetch error:,{},{}", e, "222")
        except Exception as e:
            failUrlList.add(tul)
            logger.warning("get proxy ip error:,{},{}", e, "111")

    return content


async def parser(html, tul, type):
    if "操作太频繁了，请先歇一歇" in html:
        failUrlList.add(tul)
        return
    if html == "":
        failUrlList.add(tul)
        return
    url = ""
    if type == "yapan":
        url = "http://vip.win007.com/changeDetail/handicap.aspx?id=" + tul[0] + "&companyid=" + tul[6] + "&l=0"
    if type == "daxiao":
        url = "http://vip.win007.com/changeDetail/overunder.aspx?id=" + tul[0] + "&companyid=" + tul[6] + "&l=0"

    try:
        bifinglist = [tul[2], tul[3]]

        query = {"time": tul[1],
                 "place": tul[0],
                 "masterGoal": int(bifinglist[0]),
                 "guestGoal": int(bifinglist[1]),
                 "midMasterGoal": tul[4][0],
                 "midGuestGoal": tul[4][1],
                 "lianShai": tul[5]
                 }
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

        try:
            if len(col) != 0:
                await col_daxiao.update_one(query,
                                            {'$set': col},
                                            upsert=True)
        except Exception as ex:
            logger.debug("insert mongo error: {},{}", ex, url)
            return
    except Exception as ex:
        logger.warning("get eu match error:,{},{}", ex, url)
        return


async def downloadYapan(tul):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, tul, "yapan")
        await parser(html, tul, "yapan")


async def downloadDaxiao(tul):
    async with aiohttp.ClientSession() as session:
        html = await fetch(session, tul, "daxiao")
        await parser(html, tul, "daxiao")


async def downloadOupei(tul):
    async with aiohttp.ClientSession() as session:
        content = ""
        times = 0
        while content == "" and times < 4:
            try:
                times += 1
                ip = ips[random.randint(0, len(ips) - 1)]
                requestJSONdata = "id=" + tul[
                    0] + "ids=665%2C386%2C90%2C432%2C81%2C115%2C517%2C474%2C82%2C499%2C422%2C80%2C548%2C1023%2C450%2C38%2C738%2C145%2C121%2C60%2C100%2C110%2C545%2C177%2C521%2C826%2C370%2C4%2C97%2C27%2C816%2C104%2C146%2C649%2C158%2C34%2C70%2C71%2C512%2C88%2C9%2C255%2C136%2C482%2C535%2C462%2C156%2C56%2C463%2C871%2C173%2C281%2C381%2C16%2C531%2C841%2C33%2C352%2C601%2C32%2C2%2C54%2C1039%2C659%2C1029%2C866%2C980%2C604%2C755%2C648%2C178%2C970%2C850%2C127%2C266%2C910%2C985%2C315%2C975%2C863%2C1024%2C113%2C974%2C914%2C739%2C708%2C845%2C530%2C460%2C909%2C844%2C529%2C908%2C843%2C133%2C660%2C818%2C719%2C375%2C982%2C527%2C610%2C1022%2C804%2C842%2C822%2C825%2C737%2C904%2C903%2C681%2C1002%2C124%2C680%2C902%2C901%2C559%2C1021%2C706%2C232%2C900%2C899%2C677%2C898%2C466%2C994%2C167%2C840%2C791%2C1019%2C936%2C998%2C897%2C307%2C923%2C30%2C896%2C1030%2C895%2C751%2C894%2C161%2C750%2C646%2C656%2C934%2C19%2C891%2C889%2C749%2C913%2C888%2C632%2C733%2C180%2C997%2C858%2C887%2C991%2C956%2C732%2C886%2C567%2C801%2C520%2C568%2C800%2C596%2C992%2C958%2C884%2C993%2C571%2C849%2C746%2C855%2C836%2C573%2C771%2C921%2C1004%2C657%2C185%2C973%2C717%2C481%2C882%2C1032%2C881%2C574%2C159%2C776%2C949%2C87%2C1007%2C813%2C919%2C577%2C669%2C764%2C480%2C774%2C578%2C745%2C73%2C947%2C624%2C834%2C946%2C799%2C878%2C643%2C918%2C580%2C607%2C983%2C812%2C540%2C945%2C743%2C642%2C854%2C944%2C623%2C798%2C1006%2C832%2C996%2C384%2C876%2C952%2C667%2C1034%2C695%2C686%2C354%2C943%2C874%2C620%2C796%2C715%2C824%2C995%2C382%2C1017%2C538%2C713%2C591%2C829%2C828%2C171%2C780%2C972%2C664%2C794%2C775%2C766%2C937%2C176%2C981%2C506%2C941%2C872%2C721%2C742%2C709%2C827%2C808%2C1010%2C641%2C741%2C1035%2C537%2C464%2C978%2C1009%2C584%2C852%2C134%2C930%2C977%2C616%2C688%2C436%2C772%2C615%2C777%2C976%2C18"
                headers = {"Content-Type": "application/x-www-form-urlencoded",
                           "Origin": "http://op1.win007.com",
                           "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36 Edg/92.0.902.62"}
                try:
                    async with session.post("http://op1.win007.com/ExportExcelNew.aspx", data=requestJSONdata,
                                            headers=headers,
                                            timeout=10, proxy=ip) as content:
                        text = await content.content.read(40000 * 1024)
                        try:
                            path = r"D:\oupei\{}\{}_{}_{}_{}_{}_{}.xls".format(tul[1][0:4], tul[0], tul[2],
                                                                               tul[3], tul[4][0], tul[4][1],
                                                                               tul[5])
                            fp = open(path, "wb")
                            fp.write(text)
                            fp.close()
                            content = "1"
                        except Exception as e:
                            logger.warning("fetch error:222{}", e)
                except:
                    logger.warning("fetch error:timeout")
            except Exception as e:
                failUrlList.add(tul)
                logger.warning("get proxy ip error:,{}", e)
        if content == "":
            failUrlList.add(tul)


def get91vs(year, startMon, endMon):
    global failList, listUrl
    global failUrlList

    start = time.time()
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

    loop = asyncio.get_event_loop()
    for listUrl in list_of_groups(timeList, 12):
        tasks = []
        for timeTul in listUrl:
            tasks.append(asyncio.ensure_future(chooseDay(timeTul)))
        try:
            loop.run_until_complete(asyncio.wait(tasks))
        except Exception as ex:
            logger.warning("run asyncio fail: {}", ex)

    errTimes = 0
    while (failList and errTimes < 8):
        logger.warning("failList: {}", failList)
        errTimes += 1
        errorList = failList
        failList = []
        for listUrl in list_of_groups(errorList, 4):
            tasks = []
            for timeTul in listUrl:
                tasks.append(asyncio.ensure_future(chooseDay(timeTul)))
            try:
                loop.run_until_complete(asyncio.wait(tasks))
            except Exception as ex:
                logger.warning("run asyncio fail: {}", ex)
    end = time.time()
    logger.warning("selenium0000 find allDay time consume: {}", end - start)
    logger.warning(len(urlAlllist))

    loop = asyncio.get_event_loop()
    for listUrl in list_of_groups(list(urlAlllist), 64):
        tasks = [asyncio.ensure_future(downloadYapan(url)) for url in listUrl]
        loop.run_until_complete(asyncio.gather(*tasks))

    errTimes = 0
    while (failUrlList and errTimes < 2):
        logger.warning("failUrlList: {}", failUrlList)
        errorList = failUrlList
        failUrlList = set()
        errTimes += 1
        for listUrl in list_of_groups(list(errorList), 64):
            tasks = [asyncio.ensure_future(downloadYapan(url)) for url in listUrl]
            loop.run_until_complete(asyncio.gather(*tasks))

    # for listUrl in list_of_groups(list(urlAlllist), 64):
    #     tasks = [asyncio.ensure_future(downloadDaxiao(url)) for url in listUrl]
    #     loop.run_until_complete(asyncio.gather(*tasks))
    #
    # errTimes = 0
    # while (failUrlList and errTimes < 6):
    #     logger.warning("failUrlList: {}", failUrlList)
    #     errorList = failUrlList
    #     failUrlList = set()
    #     errTimes += 1
    #     for listUrl in list_of_groups(list(errorList), 64):
    #         tasks = [asyncio.ensure_future(downloadDaxiao(url)) for url in listUrl]
    #         loop.run_until_complete(asyncio.gather(*tasks))

    # for listUrl in list_of_groups(list(urlAlllist), 64):
    #     tasks = [asyncio.ensure_future(downloadOupei(url)) for url in listUrl]
    #     loop.run_until_complete(asyncio.gather(*tasks))
    #
    # errTimes = 0
    # while (failUrlList and errTimes < 6):
    #     logger.warning("failUrlList: {}", failUrlList)
    #     errorList = failUrlList
    #     failUrlList = set()
    #     errTimes += 1
    #     for listUrl in list_of_groups(list(errorList), 64):
    #         tasks = [asyncio.ensure_future(downloadOupei(url)) for url in listUrl]
    #         loop.run_until_complete(asyncio.gather(*tasks))


ips = []


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
        time.sleep(30)


if __name__ == '__main__':
    start = time.time()
    loop = asyncio.get_event_loop()
    t = threading.Thread(target=getIps)
    t.setDaemon(True)
    t.start()
    time.sleep(10)
    get91vs(2021, 1, 2)
    end = time.time()
    logger.warning("find allMatch time consume: {}", end - start)
