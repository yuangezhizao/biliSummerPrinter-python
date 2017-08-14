from biliSummerPrinter import BiliBitmap

zMap = BiliBitmap(BiliBitmap.createEmptyBitmapList(25, 7))
zMap.fillColor(0, 0, 25, 7, "0")


def xSet(y, color, *x):
    for i in x:
        zMap.setColor(i, y, color)


# 第一行
for i in range(1, 6):
    zMap.setColor(i, 1, 'I')
for i in range(19, 23):
    zMap.setColor(i, 1, 'I')
# 10,13,17
zMap.setColor(10, 1, 'I')
zMap.setColor(13, 1, 'I')
zMap.setColor(17, 1, 'I')

# 第二行
xSet(2, 'I', 4, 9, 10, 13, 17, 19, 23)

# 3
xSet(3, 'I', 3, 8, 10, 13, 14, 15, 16, 17, 19, 23)

# 4
for i in range(7, 12):
    zMap.setColor(i, 4, 'I')

xSet(4, 'I', 2, 13, 17, 19, 23)

# 5
for i in range(1, 6):
    zMap.setColor(i, 5, 'I')
for i in range(19, 23):
    zMap.setColor(i, 5, 'I')
xSet(5, 'I', 10, 13, 17)

zMap.printf()

with open('z4hdMap.json','w') as f:
    f.write(zMap.json())
