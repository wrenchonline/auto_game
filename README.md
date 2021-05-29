
# pyAutomated
项目设计目的是在跨平台上模拟键鼠点击安卓虚拟机(我使用vbox),实现自动化。

### 此项目的优势有:
1.基于图片的提供数据给机器学习有很好的调试接口点  
2.不需要触动精灵的年费授权，您可以免费的使用本代码  
3.不调用Guest系统的api,从host外部调用虚拟机接口,具有极强的隐蔽性
4.跨平台使用，没有比这个更棒的事情

演示视频:[python重写触动精灵核心引擎演示](https://www.bilibili.com/video/BV1Ev411t7B1/)

此代码重新实现了触动精灵核心功能,分别是找色函数findMultiColorInRegionFuzzy,findMultiColorInRegionFuzzyByTable与识字函数Ocrtext,可以和官网上的找色工具与识字工具配合开发。(代码原理说不尽，等有空更新文档)


两个函数的关键使用与触动精灵差别不大，如果你有什么更好的想法或者问题，请联系我的邮箱ljl260435988@gmail.com

## 运行环境:
    ubuntu 20.04
    vbox 6.1.22
    conda python3.7.9

## python运行环境：
    numpy>=1.18.5
    numba>=0.50.1
    Pillow>=8.1.1
    pynput>=1.7.1
    pytesseract>=0.3.6
    opencv-python>=4.4.0.46
    func_timeout>=4.3.5
    remotevbox>=1.0.1

 

# 使用说明

1.初始化对象
```python
blRobot=Robot()
blRobot.Get_GameHwnd()
```

接下来可以使用部分功能了，还有很多其他方式的实现就不一一说明

### 识字函数(可以和触动精灵字库使用):
```python
xstr=blRobot.Ocrtext(test,"00E804,011805#03DC07,032006#08DD0B,072009",444,506,589,560)

--------------------------
pirnt("xstr=",xstr)
xstr="helloWorld"
```
### 找色函数 findMultiColorInRegionFuzzy（可以和触动精灵官网的找色工具配合）:
```python
status,ag= blRobot.findMultiColorInRegionFuzzy( "0xef6fdc", "24|5|0xffeecb,-7|30|0x2fb7ff", 90, 0, 0, 1919, 1079)
-------------------------------------------
pirnt("ag=",ag)
ag=(667,1015)
```

### 找色函数 findMultiColorInRegionFuzzyByTable（可以和触动精灵官网的找色工具配合）:
```python
zhujiemian = (667,1015,'0xefc250'),(782,1024,'0xd89825'),(907,1022,'0xea8f4f'),(1022,1017,'0xf8cf48'),(1124,1020,'0xb75715')
status,ag=self.findMultiColorInRegionFuzzyByTable(zhujiemian)
-------------------------------------------
pirnt("ag=",ag)
ag=(667,1015)
```

### 模拟虚拟机鼠标左键点击:
```python
blRobot.click(125,33)
```



### 已知问题:
    1.findMultiColorInRegionFuzzy 参数2不能为空字符串 "" ,也就是说找色必须要有两个点以上才行,待优化。

### 关于找色找字辅助工具：
      目前使用wine能成功运行触动精灵找色工具，找字工具不能成功运行，目前没有什么方便的方案解决，等待我有空进行辅助工具的二次开发.如果你有兴趣在这浪费时间话，麻烦联系我你辅助工具的开发项目，或者给我一杯咖啡的资助，让我有动力进行开发.

### 相关回答
    1.之前项目使用在windows平台与虚拟机互动，为什么经过大量的修改导致与原先的项目生态大变化？
    Answer:有太多原因,其中最主要的是我获得了新技能，我使用vbox重新定制了一款可从源代码操控的自由操作系统，此技能不再依赖于商业产品.所以我有更多的扩展空间，当然问题是一些陈旧的代码我不得不慢慢修改完善.
    2.还维护之前项目的逻辑代码么?变动太大操作人员无法重新适配新的自动化环境.
    Answer:不好意思，已经不维护上一个版本，必须以这个版本为主,新环境在所难免.

