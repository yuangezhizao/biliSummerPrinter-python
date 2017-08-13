# biliSummerPrinter-python
屑站夏日绘板活动Python类模块，附赠一个用于分析与操作bitmap的类。由Python3.6恶俗驱动。

**本模块仍未完善，您现在看到的一切内容包括本README都会不停的修改（确信）** 建议你也一起来玩，玩累了就直接睡觉

# 前置模块
本类用到了requests模块，使用本模块前请通过pip安装它。

``` shell
$ pip install requests
```
# 功能特色
### biliSummerPrinter类
- 使用bilibiliID和Cookie实例化本对象
- 在指定坐标绘制指定颜色的像素（`biliSummerPrinter.draw(x坐标，y坐标，字符串格式的屑站定义的颜色名）`，成功返回0，失败返回JSON格式的错误信息）
- 获取单次绘画冷却时间（`biliSummerPrinter.getCDTime()`）
- 获取bitmap
  - `biliSummerPrinter.getRawBitmap()`返回纯字符串格式的bitmap
  - `biliSummerPrinter.getBitmap()`返回经过解析的二维列表格式的bitmap
  
### BiliBitmap类
- 使用一个Bitmap二维列表
- 解析析纯字符串格式的bitmap为二维列表（静态方法）
- 自我裁剪（`BiliBitmap.cut(x,y,长度,宽度)`参数要切出的区域左上角第一个像素的x，y坐标，以及要切出区域的长度与宽度。）（还有一个静态裁剪方法，用法差不多）
- 批量填充颜色
- 按坐标操作颜色
- 更多功能请阅读代码注释。
- 该类目前并**不**完善

### 解析返回的bitmap二维列表使用说明
- **重要说明**：与屑站前端处理坐标的方式相同，以画板最左上角的像素为原点（0，0），最左下角的坐标为（1179，719）
- 第一个下标对应夏日绘版中的y值（高），第二个下表对应x值（长），对应的值为颜色名。可能为int，请自行转换。
- 


# 快速上手

``` python
from biliSummerPrinter import biliSummerPrinter,BiliBitmap #导入本模块,使用此格式导入可享受VSCode之自动完成特性。

you = biliSummerPrinter('yourID', 'yourCookie') #实例化一个Printer（必须步骤）
cdTime = you.getCDTime() #获取剩余时间
print('倒计时:' + cdTime) #打印倒计时
you.draw(0,0,'0') #在整个画布左上角画一个黑色像素
```

# 其他用法
由于时间仓促，其余内容请阅读代码中的注释，3Q2X

# 鸣谢
部分请求方法参考自：[Bili-AutoDraw](https://github.com/BBleae/Bili-AutoDraw)、[bili_huiban_helper](https://github.com/shugen002/bili_huiban_helper)
