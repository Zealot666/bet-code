import os.path
import sys
import time
from PyGameAuto.Dm import RegDm


def buildList(l):
    newList = []
    for i in l.strip().split(' '):
        for j in i.split('-'):
            newList.append(j.strip())
    return newList


def inList(A, B):
    ret = []
    for i in A:
        if i in B:
            if i not in ["FC", "United", "U23", "U19", "U21", "Women"]:
                ret.append(i)
    if len(ret) > 0:
        return True
    return False


def daxiao_num(x):
    try:
        x_list = str(x).strip().split(",")
        num = 0
        for i in x_list:
            num += float(i)
        return (float(num) / len(x_list))
    except Exception as ex:
        print(ex, x)
        return 0


def MouseDrag(dm, x1, y1, x2, y2):
    dm.MoveTo(x1, y1)
    dm.LeftDown()
    dm.MoveTo(x2, y2)
    dm.LeftUp()


class BetBot:
    def __init__(self):
        self.jine = "100"
        self.dm = RegDm.reg()
        self.path = os.path.join(sys.path[1] + '') + "\\source\\"

        self.dm.reg("jv965720b239b8396b1b7df8b768c919e86e10f", "jvpwigc9jrxz700")
        hwnd = self.dm.EnumWindow(0, "TheRender", "RenderWindow", 1 + 2)
        hwnd = int(hwnd)
        self.hwnd = hwnd
        self.dm.BindWindowEx(hwnd, "dx.graphic.opengl", "windows", "windows", "", 0)
        self.dm.SetPath(self.path)
        self.dm.SetAero(0)
        self.history = {}

        import zmq
        context = zmq.Context()
        self.socket = context.socket(zmq.REQ)
        self.socket.connect("tcp://localhost:12344")

    def refresh(self):
        print("refresh")
        for i in range(10):
            self.dm.KeyPressChar('esc')
            self.dm.Delay(1000)

        end = self.dm.FindPic(716, 166, 773, 229, "365.bmp", "111111", 0.8, 0)
        print(end, "find 365")
        if end[0] == 0:
            self.dm.MoveTo(end[1], end[2])
            self.dm.LeftClick()
        time.sleep(5)
        self.dm.MoveTo(867, 588)
        self.dm.LeftClick()


    def login(self):
        count = 0
        while 1:
            if count == 60:
                count = 0
                print("logining faild, start refresh")
                self.refresh()

            self.dm.Capture(517, 229, 1233, 905, "x11.bmp")
            ret = self.dm.FindPic(517, 229, 1233, 905, "x.bmp", "111111", 0.8, 0)
            if ret[0] == 0:
                self.dm.MoveTo(ret[1], ret[2])
                self.dm.LeftClick()

            donebut = self.dm.FindPic(517, 229, 1233, 905, "done.bmp", "111111", 0.8, 0)
            if donebut[0] == 0:
                print("done error")
                self.dm.MoveTo(donebut[1], donebut[2])
                self.dm.LeftClick()

            self.dm.Capture(780, 596, 972, 686, "close0000.bmp")
            ret = self.dm.FindPic(780, 596, 972, 686, "close.bmp", "111111", 0.7, 0)
            if ret[0] == 0:
                self.dm.MoveTo(ret[1], ret[2])
                self.dm.LeftClick()

            self.dm.Capture(1688, 45, 1735, 102, "logined111.bmp")
            ret = self.dm.FindPic(1688, 45, 1735, 102, "logined.bmp", "111111", 0.8, 0)
            if ret[0] == 0:
                self.dm.Capture(1599, 59, 1678, 92, "jine.bmp")
                byte = (self.path + "jine.bmp").encode()
                self.socket.send(byte)
                text = self.socket.recv().decode()
                try:
                    self.jine = str(int(float(text) * 0.046))
                except Exception as ex:
                    print("jine error", ex)
                break

            self.dm.Capture(1671, 59, 1716, 94, "loging11.bmp")
            ret = self.dm.FindPic(1671, 59, 1716, 94, "loging.bmp", "111111", 0.8, 0)
            if ret[0] == 0:
                self.dm.MoveTo(ret[1], ret[2])
                self.dm.LeftClick()
                time.sleep(5)
                self.dm.MoveTo(643, 283)
                self.dm.LeftClick()
                time.sleep(3)
                self.dm.SendString(self.hwnd, "qw8146657#")
                time.sleep(1)

                ret = self.dm.FindPic(607, 333, 671, 382, "keep.bmp", "111111", 0.8, 0)
                if ret[0] == 0:
                    self.dm.MoveTo(ret[1], ret[2])
                    self.dm.LeftClick()

                self.dm.MoveTo(823, 443)
                self.dm.LeftClick()
                time.sleep(10)
                ret = self.dm.FindPic(780, 596, 972, 686, "close.bmp", "111111", 0.8, 0)
                if ret[0] == 0:
                    self.dm.MoveTo(ret[1], ret[2])
                    self.dm.LeftClick()

                time.sleep(2)
                ret = self.dm.FindPic(824, 590, 938, 653, "no.bmp", "111111", 0.8, 0)
                if ret[0] == 0:
                    self.dm.MoveTo(ret[1], ret[2])
                    self.dm.LeftClick()
            count += 1
            time.sleep(1)

    def goBetList(self, matchList):
        while 1:
            print("goBetList")
            ret = self.dm.FindPic(780, 596, 972, 686, "close.bmp", "111111", 0.8, 0)
            if ret[0] == 0:
                self.dm.MoveTo(ret[1], ret[2])
                self.dm.LeftClick()

            self.dm.Capture(175, 921, 257, 967, "sports.bmp")
            byte = (self.path + "sports.bmp").encode()
            self.socket.send(byte)
            text = self.socket.recv().decode()
            if text.split('\n')[0] == "Sports":
                print("Go 0")
                self.dm.MoveTo(202, 947)
                self.dm.LeftClick()
                self.dm.LeftClick()
                self.dm.LeftClick()
                time.sleep(1)

                self.dm.Capture(535, 923, 617, 969, "inplay.bmp")
                byte = (self.path + "inplay.bmp").encode()
                self.socket.send(byte)
                text = self.socket.recv().decode()
                if text.split('\n')[0] == "InPlay" or text.split('\n')[0] == "In-Play":
                    print("Go 1")
                    self.dm.MoveTo(522, 944)
                    self.dm.LeftClick()
                    self.dm.LeftClick()
                    self.dm.LeftClick()
                    break
        times = 10
        while times > 0:
            ret = self.dm.FindColor(565, 333, 1083, 818, "e5ca23-111111", 0.8, 0)
            if ret[0] == 1:
                print("load success")
                time.sleep(1)
                break
            time.sleep(1)
            times -= 1

        ret = self.dm.FindPic(780, 596, 972, 686, "close.bmp", "222222", 0.7, 0)
        if ret[0] == 0:
            self.dm.MoveTo(ret[1], ret[2])
            self.dm.LeftClick()

        times = 10000
        while times > 0:
            ret = self.dm.FindPicEx(265,387,307,606, "item.bmp", "102030", 0.85, 0)
            if ret != '':
                xyList = ret.split('|')
                matchList = self.findMatch(xyList, matchList)
            MouseDrag(self.dm, 573, 863, 573, 363)
            if len(matchList) == 2:
                print("match is going")
                return "False"
            if len(matchList) == 0:
                print("len matchList zero")
                return "True"
            end = self.dm.FindPic(76, 294, 522, 871, "end.bmp", "111111", 0.8, 0)
            if end[0] == 0:
                print("find end item")
                return "True"
            times -= 1
        return "False"

    def butJin(self):
        for i in self.jine:
            zerobut = self.dm.FindPic(514, 534, 1231, 830, str(i) + ".bmp", "111111", 0.8, 0)
            print(i, zerobut)
            if str(i) == "2":
                self.dm.MoveTo(878, 559)
                self.dm.LeftClick()
                continue
            if zerobut[0] == 0:
                self.dm.MoveTo(zerobut[1] + 10, zerobut[2])
                self.dm.LeftClick()
            time.sleep(0.3)

    def bet(self, zuobiao, zhuDui):
        print("bet start", zuobiao)
        ret = self.dm.FindPic(517, 229, 1233, 905, "x.bmp", "111111", 0.8, 0)
        if ret[0] == 0:
            self.dm.MoveTo(ret[1], ret[2])
            self.dm.LeftClick()

        donebut = self.dm.FindPic(517, 229, 1233, 905, "done.bmp", "111111", 0.8, 0)
        if donebut[0] == 0:
            print("done error")
            self.dm.MoveTo(donebut[1], donebut[2])
            self.dm.LeftClick()
        self.dm.MoveTo(zuobiao[0] + 50, zuobiao[1])
        self.dm.LeftClick()

        self.dm.Capture(89, 244, 1322, 949, "\\tmp\\button1" + zhuDui + ".bmp")
        times = 5
        while times > 0:
            print("bet find button start")
            if times == 3:
                self.dm.Capture(zuobiao[0], zuobiao[1], zuobiao[0] + 100, zuobiao[1] + 50, zhuDui + "-betOdd.bmp")
                self.dm.MoveTo(zuobiao[0], zuobiao[1])
                self.dm.LeftClick()
            time.sleep(4)
            self.dm.Capture(89, 244, 1322, 949, "\\tmp\\button2" + zhuDui + ".bmp")
            ret = self.dm.FindPic(519, 832, 698, 905, "Set.bmp", "111111", 0.8, 0)
            if ret[0] == 0:
                print("bet find button success")
                self.dm.MoveTo(ret[1], ret[2])
                self.dm.LeftClick()
                time.sleep(2)
                # 金额
                self.dm.Capture(514, 534, 1231, 800, "jine.bmp")
                # 1
                # self.dm.MoveTo(635, 570)
                # self.dm.LeftClick()
                # time.sleep(0.5)
                # 5

                # zerobut = self.dm.FindPic(514, 534, 1231, 830, "5.bmp", "111111", 0.8, 0)
                # print("five", zerobut)
                # if zerobut[0] == 0:
                #     self.dm.MoveTo(zerobut[1], zerobut[2])
                #     self.dm.LeftClick()
                # time.sleep(0.5)

                # zerobut = self.dm.FindPic(514, 534, 1231, 830, "0.bmp", "111111", 0.8, 0)
                # print("zero", zerobut)
                # if zerobut[0] == 0:
                #     self.dm.MoveTo(zerobut[1], zerobut[2])
                #     self.dm.LeftClick()
                # time.sleep(0.5)
                self.butJin()
                # 确认
                threeBut = self.dm.FindPic(514, 534, 1231, 830, "3.bmp", "111111", 0.8, 0)
                print(threeBut)
                if threeBut[0] == 0:
                    self.dm.MoveTo(threeBut[1], threeBut[2] - 30)
                    self.dm.LeftClick()
                # done
                times = 10
                print("done start")
                self.dm.Capture(517, 229, 1233, 905, "\\tmp\\doneStart" + zhuDui + ".bmp")
                while times > 0:
                    time.sleep(1)
                    self.dm.Capture(517, 229, 1233, 905, "\\tmp\\done" + zhuDui + ".bmp")
                    donebut = self.dm.FindPic(517, 229, 1233, 905, "done.bmp", "111111", 0.8, 0)
                    if donebut[0] == 0:
                        print("done success")
                        self.dm.MoveTo(donebut[1], donebut[2])
                        self.dm.LeftClick()
                        break
                    times -= 1
                break
            times -= 1

        ret = self.dm.FindPic(517, 229, 1233, 905, "x.bmp", "111111", 0.8, 0)
        if ret[0] == 0:
            self.dm.MoveTo(ret[1], ret[2])
            self.dm.LeftClick()

        donebut = self.dm.FindPic(517, 229, 1233, 905, "done.bmp", "111111", 0.8, 0)
        if donebut[0] == 0:
            print("done error")
            self.dm.MoveTo(donebut[1], donebut[2])
            self.dm.LeftClick()

        print("bet end")
        time.sleep(2)

    def findMatch(self, xyList, matchList):
        for i in xyList:
            x = int(i.split(',')[1])
            y = int(i.split(',')[2])
            self.dm.Capture(x - 270, y - 30, x, y + 15, "1tmp.bmp")
            byte = (self.path + "1tmp.bmp").encode()
            self.socket.send(byte)
            text1 = self.socket.recv().decode()

            self.dm.Capture(x - 270, y + 10, x, y + 60, "2tmp.bmp")
            byte = (self.path + "2tmp.bmp").encode()
            self.socket.send(byte)
            text2 = self.socket.recv().decode()
            zuobiao = (x + 100, y)
            if text1 != "" and text2 != "":
                for item in matchList:
                    zhuDui = item[0]
                    keDui = item[1]
                    matchZhu = inList(buildList(zhuDui), buildList(text1.split('\n')[0]))
                    matcKe = inList(buildList(keDui), buildList(text2.split('\n')[0]))
                    print(matchZhu, matcKe, buildList(text1.split('\n')[0]), buildList(text2.split('\n')[0]))
                    if zhuDui + keDui not in self.history.keys():
                        matchZhu = inList(buildList(zhuDui), buildList(text1.split('\n')[0]))
                        matcKe = inList(buildList(keDui), buildList(text2.split('\n')[0]))
                        if (matchZhu or matcKe):
                            self.dm.Capture(zuobiao[0], zuobiao[1], zuobiao[0] + 200, zuobiao[1] + 30,
                                            "betOdd.bmp")
                            byte = (self.path + "betOdd.bmp").encode()
                            self.socket.send(byte)
                            text3 = self.socket.recv().decode()
                            print("betOdd", buildList(text1.split('\n')[0]), buildList(text2.split('\n')[0]))
                            print("betOdd", time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())))
                            try:
                                odd = float(text3[-5:].strip())
                                if daxiao_num(text3[:-5]) != item[2]:
                                    print("betOdd", text1, text2, "item not right", daxiao_num(text3[:-5]), item[2])
                                    return matchList + matchList
                                print(text1, text2, "item right", item[2], odd)
                            except Exception:
                                pass

                            print("find match", zhuDui, keDui)
                            ret = self.dm.FindPic(1671, 59, 1716, 94, "loging.bmp", "111111", 0.8, 0)
                            if ret[0] == 0:
                                print("find match but not login", zhuDui, keDui)
                                self.login()
                                self.goBetList(matchList)
                                matchList.remove(item)
                                return matchList

                            self.bet((x + 150, y), zhuDui)
                            self.history[zhuDui + keDui] = 1
                            matchList.remove(item)
        return matchList

    def quit(self):
        self.dm.UnBindWindow()


if __name__ == '__main__':
    bot = BetBot()
    bot.refresh()
    print("su")
    # bot.login()
    # bot.goBetList([("Furth", "FC", 2.5)])
    # bot.quit()

    import time
    import zmq

    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:11115")
    print("start success")
    while True:
        message = socket.recv()
        sendList = message.decode('utf-8', 'ignore')
        matchList = []
        for i in sendList.split('|'):
            item = i.split(",")
            if item[0] != "" and item[1] != '':
                if item[3] == "0":
                    bot.refresh()
                    bot.login()
                else:
                    if item[3] == "2":
                        bot.login()
                    else:
                        print("recive: " + message.decode('utf-8', 'ignore'))
                        try:
                            matchList.append((item[0], item[1], float(item[2])))
                        except Exception as ex:
                            print(ex)
        bot.login()
        start = time.time()
        res = ""
        if len(matchList) != 0:
            res = bot.goBetList(matchList)
        end = time.time()
        socket.send(res.encode('utf-8'))
