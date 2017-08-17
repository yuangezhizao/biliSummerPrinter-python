from biliSummerPrinter import biliSummerPrinter, BiliBitmap
import time
import datetime
import progressbar  # pip install progressbar2
import random
import json
import sys

# 声明全局变量
#account = {}
z4Map = object
printer = object
j = {}
jaccount = {}
useage = """
使用说明:
DEMO.py -c [配置文件路径] -a [账号信息路径]

未指定时默认值分别为：DEMOconfig.json， account.json
"""


def Timmer(cd):
    bar = progressbar.ProgressBar()
    for i in bar(range(cd)):
        time.sleep(1)


def init(confurl='DEMOconfig.json', accounturl='account.json'):
    global j, jaccount, z4Map, printer
    with open(confurl, 'rb') as conf:
        b = conf.read().decode('utf-8')
        j = json.loads(b)
    with open(accounturl, 'rb') as conf:
        b = conf.read().decode('utf-8')
        jaccount = json.loads(b)

    if jaccount['cookie'] == "yourCookie":
        print("[ERROR!]:谢绝默认迫真cookie")
        input("按任意键退出程序>")
        exit()
    with open(j['mapfile'], 'r') as mf:
        z4Map = BiliBitmap.decodeJSON(mf.read())
    print("Print Map...")
    z4Map.printf()
    printer = biliSummerPrinter(jaccount['id'], jaccount['cookie'])
    cd = printer.getCDTime()
    print("cdTime:%s" % cd)
    if cd != 0:
        Timmer(cd)


def checkBitmap(x, y):
    # 参数为要检测的bitmap的左上角像素在整个绘板中的坐标
    try:
        bili = printer.getBitmap()
    except:
        time.sleep(5)
        bili = printer.getBitmap()
    bili.cut(x, y, z4Map.length, z4Map.width)
    bili.printf()
    i = 0
    diff = []
    while i < len(bili.bitMap):
        i2 = 0
        while i2 < len(bili.bitMap[i]):
            if bili.bitMap[i][i2] != z4Map.bitMap[i][i2]:
                # 此处取得的X、y均为相对坐标，应与基础坐标相加来得到绝对坐标。
                diff.append(
                    {'x': i2, 'y': i, 'rightColor': str(z4Map.bitMap[i][i2])})
            i2 += 1
        i += 1
    print(diff)
    return diff


def main():
    argv = sys.argv
    i = 1
    c = "DEMOconfig.json"
    a = "account.json"
    '''
    if len(argv) == 1:
        print(useage)
        exit()
    '''
    while i < len(argv):
        if argv[i] == "-h":
            print(useage)
            exit()
        if argv[i] == "-c":
            c = argv[i + 1]
        if argv[i] == "-a":
            a = argv[i + 1]
        i += 1
    print(j)
    init(c, a)
    print(j)
    while True:
        diff = checkBitmap(int(j['x']), int(j['y']))
        if diff != []:
            target1 = random.choice(diff)
            print("TARGET:" + str(target1))
            printer.draw(int(j['x']) + int(target1['x']), int(j['y']) +
                         int(target1['y']), target1['rightColor'])
            time.sleep(1)
            Timmer(printer.getCDTime())
        else:
            print("[info]:GodJob! Diff is Empty! Waiting 30s for next")
            Timmer(30)


if __name__ == '__main__':
    # try:
    main()
    # finally:
    #    input("Stopped!....Press Any Key To EXIT")
