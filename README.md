# auto_game
项目设计目的是在windows系统上模拟键鼠点击安卓虚拟机(我使用夜神模拟器6.6.1.2)实现自动化.  

此代码重新实现了触动精灵核心功能,分别是找色函数findMultiColorInRegionFuzzy与识字函数Ocrtext,可以和官网上的找色工具与识字工具配合开发  



两个函数的关键使用与触动精灵差别不大，如果你有什么更好的想法或者问题，请联系我的邮箱ljl260435988@gmail.com

## 运行环境:
    windows10(150%放大倍数)
    夜神模拟器6.6.1.2(分辨率1920x1080)
    conda python3.7.9
## python运行环境：
    numpy==1.18.5
    numba==0.50.1
    pywin32==227
    Pillow==8.0.1
    pynput==1.7.1
    pytesseract==0.3.6
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

首先初始化对象并获取窗口句柄

```python
blRobot=Robot(class_name="subWin",title_name="sub",zoom_count=1.5)

blRobot.Get_GameHwnd()
```
接下来可以使用部分功能了，还有很多其他方式的实现就不一一说明

### 识字函数(可以和触动精灵字库使用,目前用得比较少，等待完善):
```python
xstr = blRobot.x_Ocrtext(tab,"303137,2F3036",173, 40, 285, 76)
```
tesseract版本识字效果识别图片只有一行字的效果比较理想
### 识字函数1(tesseract版):
```python
tpl = blRobot.Print_screen() 
xstr = blRobot.Ocrtext(tpl,173, 40, 285, 76)
```

### 识字函数2(tesseract版,查找关键字并返回坐标):
```python
tu_text_features = ['图','T']
tpl = blRobot.Print_screen() 
xstr = blRobot.tsOcrtext(tpl,tu_text_features,173, 40, 285, 76，lang='chi_sim',psm=7, oem=1)
```

### 找色函数（可以和触动精灵官网的找色工具配合）:
```python
x,y = blRobot.findMultiColorInRegionFuzzy( "0xef6fdc", "24|5|0xffeecb,-7|30|0x2fb7ff", 90, 0, 0, 1919, 1079)
```

### 模拟虚拟机鼠标点击:

```python
blRobot.click(125,33)
```

# 已知问题:
1.findMultiColorInRegionFuzzy 参数2不能为空字符串 "" ,也就是说找色必须要有两个点以上才行,待优化