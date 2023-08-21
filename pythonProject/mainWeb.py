import os.path
import sys
import time
from PyGameAuto.Dm import RegDm


def buildList(l):
    newList = []
    for i in l.strip().split(' '):
        for j in i.split('-'):
            newList.append(j.strip().lower())
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
        return float(num) / len(x_list)
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
        self.jine = "1234567890"
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

    def login(self):
        print("login start")
        self.dm.MoveTo(1664, 309)
        self.dm.LeftClick()
        time.sleep(5)
        self.dm.MoveTo(743, 527)
        self.dm.LeftClick()
        time.sleep(1)
        self.dm.SendString(self.hwnd, "qw8146657#")
        time.sleep(1)
        self.dm.MoveTo(594, 604)
        self.dm.LeftClick()
        self.dm.MoveTo(828, 689)
        self.dm.LeftClick()

    def logOut(self):
        print("logOut start")
        self.dm.MoveTo(1686, 313)
        self.dm.LeftClick()
        time.sleep(5)
        MouseDrag(self.dm, 1706, 923, 1706, 679)
        time.sleep(2)
        self.dm.MoveTo(1315, 936)
        self.dm.LeftClick()

    def goBetList(self, matchList):
        print("goBetList start")

        self.dm.MoveTo(660, 291)
        for i in range(10):
            time.sleep(0.1)
            self.dm.LeftClick()
        time.sleep(5)
        self.dm.MoveTo(789, 285)
        for i in range(10):
            time.sleep(0.1)
            self.dm.LeftClick()
        print("goBetList end")

        times = 10
        while times > 0:
            ret = self.dm.FindColor(560, 540, 1018, 961, "e5ca23-111111", 0.8, 0)
            if ret[0] == 1:
                print("load success")
                time.sleep(2)
                break
            time.sleep(1)
            times -= 1

        time.sleep(10)
        ret = self.dm.FindPic(780, 596, 972, 686, "close.bmp", "222222", 0.7, 0)
        if ret[0] == 0:
            self.dm.MoveTo(ret[1], ret[2])
            self.dm.LeftClick()

        times = 20
        while times > 0:
            time.sleep(0.1)
            self.dm.Capture(371, 343, 415, 890, "\\tmp\\item111" + str(times) + ".bmp")
            ret = self.dm.FindPicEx(371, 343, 415, 890, "item.bmp", "102030", 0.85, 0)
            print("find matches", times, ret)
            if ret != '':
                xyList = ret.split('|')
                matchList = self.findMatch(xyList, matchList)
            else:
                print("end find match")
                return "True"
            MouseDrag(self.dm, 1064, 893, 1064, 347)
            time.sleep(0.1)
            print("MouseDrag")
            if len(matchList) == 2:
                print("match is going")
                return "False"
            if len(matchList) == 0:
                print("len matchList zero")
                return "True"
            times -= 1

        return "False"

    def butJin(self):
        for i in self.jine:
            zerobut = self.dm.FindPic(486, 497, 1114, 762, str(i) + ".bmp", "111111", 0.8, 0)
            print(i, zerobut)
            if str(i) == "2":
                self.dm.MoveTo(798, 527)
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

        donebut = self.dm.FindPic(1152, 564, 1230, 639, "done.bmp", "102030", 0.85, 0)
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
                self.dm.MoveTo(zuobiao[0] + 50, zuobiao[1])
                self.dm.LeftClick()
                self.dm.Capture(89, 244, 1322, 949, "\\tmp\\button2" + zhuDui + ".bmp")
            time.sleep(10)
            self.dm.Capture(89, 244, 1322, 949, "\\tmp\\button3" + zhuDui + ".bmp")
            ret = self.dm.FindPic(479, 777, 527, 823, "Set.bmp", "102030", 0.85, 0)
            print(ret, "button3")
            if ret[0] == 0:
                print("bet find button success")
                self.dm.MoveTo(ret[1], ret[2])
                self.dm.LeftClick()
                time.sleep(2)
                # 金额
                self.dm.Capture(486, 497, 1114, 762, "jine.bmp")
                self.butJin()
                # 确认
                # threeBut = self.dm.FindPic(486, 497, 1114, 762, "3.bmp", "102030", 0.85, 0)
                # print(threeBut)
                # if threeBut[0] == 0:
                #     self.dm.MoveTo(threeBut[1], threeBut[2] - 30)
                #     self.dm.LeftClick()

                # done
                times = 10
                print("done start")
                self.dm.Capture(517, 229, 1233, 905, "\\tmp\\doneStart" + zhuDui + ".bmp")

                while times > 0:
                    time.sleep(1)
                    self.dm.Capture(517, 229, 1233, 905, "\\tmp\\done" + zhuDui + ".bmp")
                    donebut = self.dm.FindPic(517, 229, 1233, 905, "done.bmp", "102030", 0.85, 0)
                    print("done but", donebut)
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

        donebut = self.dm.FindPic(1152, 564, 1230, 639, "done.bmp", "102030", 0.85, 0)
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
            # self.dm.Capture(x - 270, y - 15, x, y + 10, "1tmp" + i.split(',')[1] + i.split(',')[2] + ".bmp")
            self.dm.Capture(x - 250, y - 15, x, y + 10, "1tmp" + ".bmp")

            byte = (self.path + "1tmp" + ".bmp").encode()
            self.socket.send(byte)
            text1 = self.socket.recv().decode()
            # self.dm.Capture(x - 270, y + 5, x, y + 45, "2tmp" + i.split(',')[1] + i.split(',')[2] + ".bmp")
            self.dm.Capture(x - 250, y + 5, x, y + 45, "2tmp" + ".bmp")
            byte = (self.path + "2tmp" + ".bmp").encode()
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
                        if matchZhu or matcKe:
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

                            self.bet((x + 150, y), zhuDui)
                            self.history[zhuDui + keDui] = 1
                            matchList.remove(item)
        return matchList

    def quit(self):
        self.dm.UnBindWindow()


if __name__ == '__main__':
    bot = BetBot()
    # bot.logOut()
    # bot.login()
    bot.goBetList([("fc", "oaxaca", 1.75)])

    # import time
    # import zmq
    #
    # context = zmq.Context()
    # socket = context.socket(zmq.REP)
    # socket.bind("tcp://*:11116")
    # print("start success")
    # while True:
    #     message = socket.recv()
    #     sendList = message.decode('utf-8', 'ignore')
    #     matchList = []
    #     for i in sendList.split('|'):
    #         item = i.split(",")
    #         print("recive: " + message.decode('utf-8', 'ignore'))
    #         try:
    #             matchList.append((item[0], item[1], float(item[2])))
    #         except Exception as ex:
    #             print(ex)
    #         if len(matchList) != 0:
    #             bot.goBetList(matchList)
    #     socket.send_string("ok!")
