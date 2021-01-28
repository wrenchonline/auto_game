# pyAutomated
项目设计目的是在windows系统上模拟键鼠点击安卓虚拟机(我使用夜神模拟器7.0.0.6)实现自动化。  
### 此项目的优势有:  
1.基于图片的提供数据给机器学习有很好的调试接口点  
2.不需要触动精灵的年费授权，您可以免费的使用本代码  
3.不调用Guest系统的api,从host外部调用虚拟机接口,具有极强的隐蔽性


演示视频:[python重写触动精灵核心引擎演示](https://www.bilibili.com/video/BV1Ev411t7B1/)

此代码重新实现了触动精灵核心功能,分别是找色函数findMultiColorInRegionFuzzy,findMultiColorInRegionFuzzyByTable与识字函数Ocrtext,可以和官网上的找色工具与识字工具配合开发。(代码原理说不尽，等有空更新文档)




两个函数的关键使用与触动精灵差别不大，如果你有什么更好的想法或者问题，请联系我的邮箱ljl260435988@gmail.com

## 运行环境:
    windows10(150%放大倍数)
    夜神模拟器7.0.0.6(分辨率1280x720)
    conda python3.7.9
## python运行环境：
    numpy==1.18.5
    numba==0.50.1
    pywin32==227
    Pillow==8.0.1
    pynput==1.7.1
    pytesseract==0.3.6
    goto-statement==1.2
    opencv-python==4.4.0.46
## conda安装tesserocr:
    conda install -c conda-forge tesserocr
识字函数比较喜欢基于采用tesseract-ocr来进行识字需要安装conda以及其环境tesserocr,（采用conda安装的tesserocr自带tesseract-ocr环境）并把chi_sim.traineddata模型包放入tessdata文件夹中（此文件夹是程序tesseract字库的路径） 
 C:\\Users\(用户名)\\.conda\\envs\\(你的环境名)\\Library\\bin\\tessdata
 
### 复制成功后以管理员cmd启动验证方式
    conda activate {your env}
    tesseract --list-langs

    看到有 chi_sim 就代表添加成功
    (OCR) C:\WINDOWS\system32>tesseract --list-langs
    List of available languages (3):
    chi_sim
    eng
    osd


# 使用说明

首先初始化对象并获取窗口句柄,目前只自持夜神模拟器的窗口句柄，7.0.0.6真正的窗口句柄名称是"sub",获得窗口句柄才能截图和发送键鼠信息。目前此代码仅支持这种控制安卓模拟器的方式,后续会添加vbox控制方式。

```python
blRobot=Robot(class_name="subWin",title_name="sub",zoom_count=1.5)
blRobot.Get_GameHwnd()
```
接下来可以使用部分功能了，还有很多其他方式的实现就不一一说明

### 识字函数(可以和触动精灵字库使用):
```python
xstr = blRobot.x_Ocrtext(ditu,"00E804,011805#03DC07,032006#08DD0B,072009",444,506,589,560)
--------------------------------------------------------------
pirnt("xstr=",xstr)
xstr="helloWorld"

```
tesseract版本识字效果识别图片只有一行字的效果比较理想
### 识字函数1(tesseract版):
```python
tpl = blRobot.Print_screen() 
xstr = blRobot.Ocrtext("06BE0B,06420B#00E804,011805#03DC07,032006#08DD0B,072009",
                    591,511,732,547,ril=RIL.TEXTLINE,
                    lang='eng',oem=1,
                    attribute=["tessedit_char_whitelist", 
                    "0123456789,")
--------------------------------------------------------------
pirnt("xstr=",xstr)
xstr=[{"text":"helloWorld","left":xxx,"top":xxx,"boxes2":xxx,"boxes3":xxx},]

```

### 识字函数2(tesseract版,查找关键字并返回坐标):
```python
tu_text_features = ['图','T']
tpl = blRobot.Print_screen() 
xstr = blRobot.tsOcrtext(tpl,tu_text_features,173, 40, 285, 76，lang='chi_sim',psm=7, oem=1)
--------------------------------------------------
pirnt("xstr=",xstr)
xstr=["图图图图",179,56]

```

### 找色函数1（可以和触动精灵官网的找色工具配合）:
```python
status,ag= blRobot.findMultiColorInRegionFuzzy( "0xef6fdc", "24|5|0xffeecb,-7|30|0x2fb7ff", 90, 0, 0, 1919, 1079)
-------------------------------------------
pirnt("ag=",ag)
ag=(667,1015)
```

### 找色函数2（可以和触动精灵官网的找色工具配合）:
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

### 模拟虚拟机左键点击鼠标移动:
```python
blRobot.move_click(125,33,555,555)
```

### 已知问题:
1.findMultiColorInRegionFuzzy 参数2不能为空字符串 "" ,也就是说找色必须要有两个点以上才行,待优化  
## 优化思路:
1.因为环境搭建比较麻烦,不过都是python包，我会考虑部署到Anaconda环境上,尽量让开发者一键安装环境。  
2.目前仅能控制夜神模拟器,其他安卓模拟器没有试过,获取窗口句柄代码需要修改,后续会支持控制vbox虚拟机(有接口)。Vmware不支持,我查到的是根据官方说法为了安全没开接口。