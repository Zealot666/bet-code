import threading
import time


def inList(A, B):
    ret = []
    for i in A:
        if A == "FC" or A == "United" or A == "U23" or A == "U19" or A == "U21" or A == "Women":
            continue
        if i in B:
            ret.append(i)
    if len(ret) > 0:
        return True
    return False


def buildList(l):
    newList = []
    for i in l.strip().split(' '):
        for j in i.split('-'):
            newList.append(j)
    return newList


a = "Netherlands Women"
b = "Netherlands "
print(buildList(a))
print(buildList(b))
print(inList(a, b))

g_num = True


def work1():
    global g_num
    while 1:
        timeDate = (time.localtime(time.time()))  # 打印本地时间
        print(timeDate.tm_hour == 10)
        print('in work1 g_num is : %d' % g_num)


if __name__ == '__main__':
    timeDate = time.localtime(time.time()).tm_hour
    t1 = threading.Thread(target=work1)
    t1.start()
    while 1:
        print(g_num)
