print("Esu! UNOFFICAL Project \n biliSummerPrinter now initializing!")
import requests
import json


class biliSummerPrinter(object):
    def __init__(self, biliId, biliCookie):
        self.id = biliId
        self.cookie = biliCookie
        self.headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.133 Safari/537.36",
            'referer': 'http://live.bilibili.com/pages/1702/pixel-drawing',
            'Origin': 'http://live.bilibili.com',
            'Cookie': self.cookie
        }

    def getCDTime(self):
        # 本方法用于获取绘画冷却时间
        r = requests.get(
            'http://api.live.bilibili.com/activity/v1/SummerDraw/status', headers=self.headers)
        jDate = r.json()
        if jDate['code'] == 0:
            return jDate['data']['time']
        else:
            print("[ERROR!] \n ID:%s \n RequestBody:%s" % (self.id, r.text))
            return "error!"

    def draw(self, x, y, color):
        # 本方法要求传入的color必须为屑站定义的颜色名，请手动使用colorHex2biliFormat方法转换或自行对照，3Q2X。
        url = "https://api.live.bilibili.com/activity/v1/SummerDraw/draw"
        printData = {
            "x_min": x,
            "y_min": y,
            "x_max": x,
            "y_max": y,
            "color": color
        }
        r = requests.post(url, data=printData, headers=self.headers)
        jDate = r.json()
        if jDate['code'] == 0:
            print("[id:%s]成功绘制像素！X=%s Y=%s Msg=%s" %
                  (self.id, x, y, jDate['msg']))
            return 0
        else:
            print("[id:%s]发生错误：%s \n RequestBody:%s" %
                  (self.id, jDate['msg'], r.text))
            return r.text

    @staticmethod
    def colorHex2biliFormat(hexName):
        # 本静态方法用于将16进制颜色值转换为哔哩哔哩定制的颜色名
        # 返回值为str
        # 仅供参考
        colorMap = json.loads('{"color":{"000000":"0","ffffff":"1","aaaaaa":"2","555555":"3","fed3c7":"4","ffc4ce":"5","faac8e":"6","ff8b83":"7","f44336":"8","e91e63":"9","e2669e":"A","9c27b0":"B","673ab7":"C","3f51b5":"D","004670":"E","057197":"F","2196f3":"G","00bcd4":"H","3be5db":"I","97fddc":"J","167300":"K","37a93c":"L","89e642":"M","d7ff07":"N","fff6d1":"O","f8cb8c":"P","ffeb3b":"Q","ffc107":"R","ff9800":"S","ff5722":"T","b83f27":"U","795548":"V"}}')

        if hexName[0] == "#":
            hexName = hexName[1:]
        try:
            name = colorMap['color'][hexName]
            return name
        except:
            print("[ERROR]:颜色名无对应")
            return None

    def getRawBitmap(self):
        # 返回纯文本形式的bitmap，建议调用decodeBitmap静态方法转换为二维列表（先行后列）
        url = 'http://api.live.bilibili.com/activity/v1/SummerDraw/bitmap'
        print("[INFO]:Getting bitmap...")
        r = requests.get(url, headers=self.headers)
        jDate = r.json()
        return jDate['data']['bitmap']

    def getListBitmap(self):
        # 直接返回人类可用的新鲜bitmap二维列表
        return BiliBitmap.decodeBitmap(self.getRawBitmap())

    def getBitmap(self):
        # 返回一个BiliBitmap对象
        r = BiliBitmap(BiliBitmap.decodeBitmap(self.getRawBitmap()))
        return r


class BiliBitmap():
    def __init__(self, bitmapList):
        try:
            test1 = bitmapList[0][0]
        except:
            print("[ERROR]传入参数应为一个bitmap列表！")
            raise
        else:
            self.bitMap = bitmapList
            self.__RSize__()
            """
            else:
                raise ValueError(
                    '传入参数应为一个由BiliBitmap.createEmptyBitmapList()方法创建或从屑站获取且经过BiliBitmap.decodeBitmap()解析的bitmap列表！')
            """

    def __RSize__(self):
        self.length = len(self.bitMap[0])
        self.width = len(self.bitMap)
        print("Size Reload! \n length:%s \n width:%s" %
              (self.length, self.width))

    @staticmethod
    def decodeBitmap(rawBitmap):
        #Useage: maplist[y][x]
        # 由于屑站死妈原因，返回的maplist二维列表下标先行后列，使用示例参考上一行。
        # 参数为纯字符串的的bitmap比如“00000AIIIIIII0001111”
        print("[INFO]:Bitmap Decoding...")
        mapList = BiliBitmap.createEmptyBitmapList(1280, 720)
        i = 0
        while i < 720:
            i2 = 0
            temp1 = rawBitmap[1280 * i:1280 * (i + 1)]
            while True:
                if i2 == len(temp1):
                    i2 = 0
                    break
                try:
                    mapList[i][i2] = temp1[i2]
                except:
                    print("[ERROR]i=%s,i2=%s,len=%s" % (i, i2, len(temp1)))
                    raise
                i2 += 1
            i += 1
        return mapList

    @staticmethod
    def createEmptyBitmapList(length, width):
        # 传入参数为bitmap的长度与宽度
        # 本静态方法创建一个空的屑站规格的bitmap
        # Useage: maplist[y][x],y和x直接写坐标即可获取对应颜色名
        return [[0 for col in range(length)] for row in range(width)]

    @staticmethod
    def cutBitmap(bitMap, x, y, length, width):
        # 传入参数为您要切割的bitmap，要切出的区域左上角第一个像素的x，y坐标，以及要切出区域的长度与宽度。
        # 返回值仍然是一个bitmap
        print("[INFO]:Bitmap cutting...")
        rr = BiliBitmap.createEmptyBitmapList(length, width)
        i = 0
        while i < width:
            i2 = 0
            while True:
                if i2 == int(length):
                    i2 = 1
                    break
                try:
                    rr[i][i2] = bitMap[y + i][x + i2]
                except:
                    print("[ERROR!] i=%s i2=%s x=%s y=%s" % (i, i2, x, y))
                    raise
                i2 += 1
            i += 1
        return rr

    def cut(self, x, y, length, width):
        # 本方法为自我切割，改变的是对象自身的list，与cutBitmap用法相同但不需传入一个列表参数。
        self.bitMap = BiliBitmap.cutBitmap(self.bitMap, x, y, length, width)
        self.__RSize__()

    def setColor(self, x, y, color):
        # 本方法要求键入的颜色名必须是屑站定义的颜色名
        # 用途：设定指定坐标的颜色
        self.bitMap[y][x] = color

    def fillColor(self, x, y, length, width, color):
        # 本方法用相同的颜色填充指定区域
        self.__RSize__()
        print("[INFO]:Corlor filling...")
        i = 0
        while i < width:
            i2 = 0
            while i2 < length:
                try:
                    self.bitMap[y + i][x + i2] = color
                except:
                    print("[ERROR!]i=%s i2=%s" % (i, i2))

                i2 += 1
            i += 1

    def json(self):
        # 返回json文本
        r = json.dumps(self.bitMap)
        return r

    @staticmethod
    def decodeJSON(jsonStr):
        # 用于将json化的bitmap解码并返回一个BiliBitmap对象
        raw = json.loads(jsonStr)
        r = BiliBitmap(raw)
        # r.__init__(BiliBitmap.decodeBitmap(raw))
        return r

    def printf(self):
        # 打印一行有格式的bitmap
        self.__RSize__()
        print("[BitMap Format Print Start!]")
        i = 0
        while i < self.width:
            i2 = 0
            line = ""
            while i2 < self.length:
                line += str(self.bitMap[i][i2])
                i2 += 1
            print(line)
            i += 1
        print("[BitMap Format Print END!]")


if __name__ == '__main__':
    print("我谔谔")
    bitmap3 = BiliBitmap(BiliBitmap.createEmptyBitmapList(5, 5))
    bitmap3.fillColor(0, 0, 5, 5, 'B')
    bitmap3.fillColor(1, 2, 3, 2, "A")
    bit4 = object
    bit4raw = ''
    with open('z4hdMap.json', 'r') as f:
        bit4raw = f.read()
    bitmap3.printf()
    sb = biliSummerPrinter('yourBilibiliID', 'yourCookie')  # 填入你的屑站ID和Cooke
    b2 = sb.getListBitmap()  # 获取bitmap列表
    print(b2[719][1279])
    print(b2[1][1])
    sb.draw(1279, 719, '0')  # 在指定位置（画布右下角）绘画一个黑色像素
    bit4 = BiliBitmap.decodeJSON(bit4raw)
    bit4.printf()
