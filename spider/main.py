import random
import time

import requests
import zmq
from pyquery import PyQuery as pq
from selenium import webdriver

from predict.processor import Processor

context = zmq.Context()
socket = context.socket(zmq.REQ)
socket.connect("tcp://localhost:11116")

failList = []
failListMap = {}
history = {}
testMap = {}
failDateList = []
successMap = {}
testList = set()
pre = Processor()

failMatch = []
failMap = {}
# smtplib 用于邮件的发信动作
import smtplib
# email 用于构建邮件内容
from email.mime.text import MIMEText
# 构建邮件头
from email.header import Header

# 发信方的信息：发信邮箱，QQ 邮箱授权码
from_addr = '2452532669@qq.com'
password = 'iddbrcakvinbebic'
# 收信方邮箱
to_addr = '2452532669@qq.com'
# 发信服务器
smtp_server = 'smtp.qq.com'


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


def parseMatch(tul, html):
    doc = pq(html)
    col = {}
    yapan = []

    query = {"time": tul[1],
             "place": tul[0],
             "midMasterGoal": tul[2][0],
             "midGuestGoal": tul[2][1],
             "lianShai": tul[3]
             }

    for td in doc('td').items():
        if "即" in td.text():
            for a in td.parent().items():
                yapan.append(a.text().strip().split())

    yapan = yapan[1:]
    if len(yapan) != 0:
        startInfo = yapan[len(yapan) - 1][:3]
        entInfo = yapan[0][:3]
        col["masterOdd_Start" + "_" + "Ji" + "_" + tul[4]] = float(startInfo[0])
        col["pankou_Start" + "_" + "Ji" + "_" + tul[4]] = (startInfo[1])
        col["guestOdd_Start" + "_" + "Ji" + "_" + tul[4]] = float(startInfo[2])
        col["masterOdd_End" + "_" + "Ji" + "_" + tul[4]] = float(entInfo[0])
        col["pankouOdd_End" + "_" + "Ji" + "_" + tul[4]] = (entInfo[1])
        col["guestOdd_End" + "_" + "Ji" + "_" + tul[4]] = float(entInfo[2])

    yapan = []
    for td in doc('td').items():
        if "中场" in td.text():
            for a in td.parent().items():
                yapan.append(a.text().strip().split()[2:])

    yapan = yapan[1:]
    if len(yapan) != 0:
        startInfo = yapan[len(yapan) - 1][:3]
        entInfo = yapan[0][:3]
        col["masterOdd_Start" + "_" + "Zhong" + "_" + tul[4]] = float(startInfo[0])
        col["pankou_Start" + "_" + "Zhong" + "_" + tul[4]] = (startInfo[1])
        col["guestOdd_Start" + "_" + "Zhong" + "_" + tul[4]] = float(startInfo[2])
        col["masterOdd_End" + "_" + "Zhong" + "_" + tul[4]] = float(entInfo[0])
        col["pankouOdd_End" + "_" + "Zhong" + "_" + tul[4]] = (entInfo[1])
        col["guestOdd_End" + "_" + "Zhong" + "_" + tul[4]] = float(entInfo[2])

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
        if num == len(numMap) and len(numMap) >= 2:
            col["lastTime"] = firstGoal[0]
            col["lastBifeng"] = firstGoal[1]

        yapan = []
        for td in doc('td').items():
            if "滚" in td.text():
                for a in td.parent().items():
                    info = a.text().strip().split()
                    try:
                        sum1 = 0
                        for j in info[1].split('-'):
                            sum1 += int(j)

                        if daxiao_num(info[3]) - sum1 == 0.5 and float(info[0]) >= float(col['lastTime']):
                            yapan.append(info)
                    except Exception as ex:
                        pass

        info = yapan[len(yapan) - 1]
        col["lastTime75"] = info[0]
        col["lastBifeng75"] = info[1]
        col["masterOdd_End" + "_" + "75" + "_" + tul[4]] = float(info[2])
        col["pankouOdd_End" + "_" + "75" + "_" + tul[4]] = (info[3])
        col["guestOdd_End" + "_" + "75" + "_" + tul[4]] = float(info[4])

        yapan = []
        for td in doc('td').items():
            if "滚" in td.text():
                for a in td.parent().items():
                    info = a.text().strip().split()
                    try:
                        sum1 = 0
                        for j in info[1].split('-'):
                            sum1 += int(j)

                        if daxiao_num(info[3]) - sum1 == 0.5 and float(info[2]) >= 1.00 and float(info[0]) >= float(
                                col['lastTime75']) \
                                and daxiao_num(info[3]) >= daxiao_num(col['pankouOdd_End_75_3']):
                            yapan.append(info)
                    except Exception as ex:
                        pass

        yapan = yapan[1:]
        info = yapan[len(yapan) - 1]

        col["lastTime130"] = info[0]
        col["lastBifeng130"] = info[1]
        col["masterOdd_End" + "_" + "130" + "_" + tul[4]] = float(info[2])
        col["pankouOdd_End" + "_" + "130" + "_" + tul[4]] = info[3]
        col["guestOdd_End" + "_" + "130" + "_" + tul[4]] = float(info[4])

        list65 = []
        for i in xiaList:
            try:
                if int(i[0]) == 60:
                    list65.append(i)
            except:
                pass
        info = list65[0]
        col["lastBifeng60"] = info[1]
        col["masterOdd_End" + "_" + "60" + "_" + tul[4]] = float(info[2])
        col["pankouOdd_End" + "_" + "60" + "_" + tul[4]] = (info[3])
        col["guestOdd_End" + "_" + "60" + "_" + tul[4]] = float(info[4])

        list65 = []
        for i in xiaList:
            try:
                if int(i[0]) == 75:
                    list65.append(i)
            except:
                pass
        info = list65[0]
        col["lastBifeng752"] = info[1]
        col["masterOdd_End" + "_" + "752" + "_" + tul[4]] = float(info[2])
        col["pankouOdd_End" + "_" + "752" + "_" + tul[4]] = (info[3])
        col["guestOdd_End" + "_" + "752" + "_" + tul[4]] = float(info[4])

        firstGoal = xiaList[0]
        col["lastBifengNow"] = firstGoal[1]

    query.update(col)
    return query


def get_html(tul, typeA):
    html = ""
    retry_count = 1
    time.sleep(1)
    # def get_proxy():
    #     return requests.get("http://127.0.0.1:5010/get/", timeout=10).json()
    #
    # def delete_proxy(proxy):
    #     requests.get("http://127.0.0.1:5010/delete/?proxy={}".format(proxy))
    #
    # proxy = get_proxy().get("proxy")
    # proxies = {"http": "http://{}".format(proxy), "https": "https://{}".format(proxy)}

    while retry_count > 0:
        url = "http://vip.titan007.com/changeDetail/overunder.aspx?id=" + tul[0] + "&companyid=3&l=0"
        try:
            # resp = requests.get(url, proxies=proxies, headers=header(), timeout=5)
            resp = requests.get(url, headers=header(), timeout=5)
            resp.encoding = 'gb18030'
            html = resp.text
            if resp.status_code != 200:
                # delete_proxy(proxy)
                error = 1 / 0
            if "操作太频繁了，请先歇一歇" in html:
                error = 1 / 0
            if html != "":
                break
        except Exception as ex:
            if "HTTPConnectionPool" in str(ex):
                pass
                # delete_proxy(proxy)
            retry_count -= 1
            pass
    if "变化" not in html:
        if tul[0] + typeA not in successMap.keys() and tul[0] + typeA not in failListMap.keys():
            failList.append(tul)
            failListMap[tul[0] + typeA] = 1
    return html


def get_one_match(tul, typeA):
    global html
    query = {}
    url = "http://vip.titan007.com/changeDetail/overunder.aspx?id=" + tul[0] + "&companyid=3&l=0"
    try:
        time.sleep(1)
        html = get_html(tul, typeA)
        query = parseMatch(tul, html)
        print("1", len(query), query)
        if len(query) == 5:
            history2[tul[0]] = 1
        if len(query) >= 38:
            testList.add(tul[0])
            testMap[tul[0] + typeA] = query
            successMap[tul[0] + typeA] = 1
    except Exception as ex:
        if "封" not in str(ex):
            if tul[0] + typeA not in successMap.keys() and tul[0] + typeA not in failListMap.keys():
                failList.append(tul)
                failListMap[tul[0] + typeA] = 1
        if "HTTPConnectionPool" not in str(ex) and "of range" not in str(ex) and "封" not in str(
                ex) and "lastBifeng" not in str(ex):
            print("get one match error", ex, url)
    return query


def find_matches(urlList, typeB):
    getDaTwo(urlList, typeB)
    errTimes = 3
    global failListMap, failList
    while (failList and errTimes > 0):
        errorList = failList
        failListMap = {}
        failList = []
        errTimes -= 1
        getDaTwo(errorList, typeB)
    failListMap = {}
    failList = []


def getDaTwo(urlList, typeB):
    for url in urlList:
        get_one_match(url, typeB)


history2 = {}


def getDayList(time):
    urlList = []
    try:

        url = "http://bf.titan007.com/football/Over_" + time + ".htm"

        html = ""
        retry_count = 3
        while retry_count > 0:
            resp = requests.get(url, timeout=5)
            try:
                resp.encoding = 'gb18030'
                html = resp.text
                if resp.status_code != 200:
                    error = 1 / 0
                if "操作太频繁了，请先歇一歇" in html:
                    error = 1 / 0
                if html != "":
                    break
            except Exception as ex:
                retry_count -= 1
                pass

        if "赛程赛果" not in html:
            failDateList.append(time)

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
                        midBifeng = (tds[6].text().split('\n')[0], tds[6].text().split('\n')[2])
                        id = list(tds[9]('a').items())[0].attr('onclick')[9:-1]
                        print(id, history2)
                        if id not in history2.keys():
                            urlList.append((id, matchTime, midBifeng, lianShai, "50"))
                except:
                    pass
    except Exception as ex:
        failDateList.append(time)
        print('getDayList error ', ex)
    return urlList


def getUrlList():
    urlList = []
    try:
        from selenium.webdriver.chrome.options import Options
        from selenium import webdriver
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        browser = webdriver.Chrome(options=chrome_options)
        browser.get('http://live.titan007.com/')
        pageSource = browser.page_source
        from pyquery import PyQuery as pq
        doc = pq(pageSource)
        for tr in list(doc('tr').items())[2:]:
            tds = list(tr('td').items())
            tds2 = []
            for i in tds:
                tds2.append(i.text())
            if len(tds) == 11:
                try:
                    timeNow = tds[3].text().strip()
                    if timeNow != "完" and timeNow != "中" and float(timeNow) > 74:
                        lianShai = tds[1].text().strip()
                        midBifeng = (tds[7].text().split('-')[0], tds[7].text().split('-')[1])
                        id = list(tds[8]('a').items())[0].attr('onclick')[9:-1]
                        matchTime = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                        if id not in history2.keys() and id not in history.keys():
                            urlList.append((id, matchTime, midBifeng, lianShai, "3"))
                except Exception as ex:
                    pass
        browser.close()
    except Exception as ex:
        print(ex)
        pass
    return urlList


def daxiao_num(x):
    x_list = str(x).split("/")
    num = 0
    for i in x_list:
        num += float(i)
    return (float(num) / len(x_list))


def realDaxiao(x, master, guest):
    return float(x) - float(master) - float(guest)


def is18(odd1, odd2):
    if odd1 < odd2:
        return 3
    if odd1 > odd2:
        return 0
    if odd1 == odd2:
        return 1


def getEnTeam(teamStr, url):
    try:
        rsp = requests.get(url, headers=header(), timeout=3)
        doc = pq(rsp.text)
        team = (doc(teamStr)("a").attr("href"))
        resp = requests.get(team, headers=header(), timeout=3)
        resp.encoding = "utf-8"
        content = resp.text
        content = content[content.index("<title>") + 7:content.index("</title>")]
        content = content.split("--")[0].split(",")[2].strip()
        newContent = content.replace("\n", "").replace("(中)", "").replace("(女)", "") \
            .replace("(后备)", "").replace("U19", "").replace("U21", "").replace("(w)", "").replace("U20", "").strip()
        return newContent
    except Exception as ex:
        print("getEnTeam", ex)
        return ""


def find_good_matchv2(idList):
    test = []
    for id in idList:
        if id not in history.keys():
            test.append(testMap.get(id + "daxiao", {}))
    if len(test) == 0:
        return 0
    try:
        res = pre.getPerOneDaxiao(test)
        num = 0
        matchList = []
        for i in res.to_dict(orient='records'):
            sum1 = 0
            for j in i["lastBifengNow"].split('-'):
                sum1 += int(j)
            if i["per"] >= 0.50:
                print(i)
        print(res)

        for i in res.to_dict(orient='records'):
            sum1 = 0
            for j in i["lastBifengNow"].split('-'):
                sum1 += int(j)
            if i["per"] >= 0.53 and i["place"] not in history.keys():
                matchList.append(i)
                # if int(i["lastTime130"]) > 75 and i["lastBifengNow"] == i["lastBifeng130"]:
                #     history[i["place"]] = 1
                #     matchList.append(i)
                # if int(i["lastTime130"]) <= 75 and i["lastBifengNow"] == i["lastBifeng752"]:
                #     history[i["place"]] = 1
                #     matchList.append(i)
            if i["per"] >= 0:
                history2[i["place"]] = 1
            num += 1

        if len(matchList) > 0:
            for i in matchList:
                url = "http://vip.titan007.com/OverDown_n.aspx?id=" + i["place"]
                zhuDui = getEnTeam(".home", url)
                keDui = getEnTeam(".guest", url)

                times = 5
                while zhuDui == "" and times > 0:
                    zhuDui = getEnTeam(".home", url)
                    times -= 1

                times = 5
                while keDui == "" and times > 0:
                    keDui = getEnTeam(".guest", url)
                    times -= 1

                if zhuDui != "" and keDui != "":
                    pankou = daxiao_num(i["pankouOdd_End_752_3"])
                    if int(i["lastTime130"]) > 75:
                        pankou = daxiao_num(i["pankouOdd_End_130_3"])
                #
                #     sendList = zhuDui + "," + keDui + "," + str(pankou) + "," + "1" + "|"
                #     print("sendList", sendList)
                #     byte = sendList.encode()
                #     socket.send(byte)
                #     message = socket.recv()  # 接收服务端返回的消息，注：是byte类型
                #     print("sendList", message)

                url = "http://vip.titan007.com/OverDown_n.aspx?id=" + i["place"]
                import webbrowser
                webbrowser.open(url)

                try:
                    # 邮箱正文内容，第一个参数为内容，第二个参数为格式(plain 为纯文本)，第三个参数为编码
                    msg = MIMEText(url, 'plain', 'utf-8')
                    # 邮件头信息
                    msg['From'] = Header('张三')  # 发送者
                    msg['To'] = Header('李四')  # 接收者
                    subject = 'Python SMTP 邮件测试'
                    msg['Subject'] = Header(subject, 'utf-8')  # 邮件主题

                    smtpobj = smtplib.SMTP_SSL(smtp_server)
                    # 建立连接--qq邮箱服务和端口号（可百度查询）
                    smtpobj.connect(smtp_server, 465)
                    # 登录--发送者账号和口令
                    smtpobj.login(from_addr, password)
                    # 发送邮件
                    smtpobj.sendmail(from_addr, to_addr, msg.as_string())
                    print("邮件发送成功", pankou)
                except smtplib.SMTPException:
                    print("无法发送邮件")
                finally:
                    # 关闭服务器
                    smtpobj.quit()
        print("find match", num)
        del res
    except Exception as ex:
        print(ex, "predict error")
    return 1


def get_timeList(year, startMon, days, daye):
    timeList = []
    try:
        for day in range(days, daye + 1):
            timeList.append(str(year) + str(startMon).zfill(2) + str(day).zfill(2))
    except Exception as ex:
        print("get date error", ex)
    return timeList


if __name__ == '__main__':
    epoch = 0
    while True:
        timeDate = time.localtime(time.time())
        testList = set()
        testMap = {}
        urlList = getUrlList()
        print(urlList)
        find_matches(urlList, "daxiao")
        if len(testList) != 0:
            find_good_matchv2(testList)
        else:
            time.sleep(5)
