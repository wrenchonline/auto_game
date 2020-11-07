# auto_game
项目设计目的是在windows系统上模拟键鼠点击安卓虚拟机(我使用夜神模拟器6.6.1.2)实现自动化.  

此代码重新实现了触动精灵核心功能,分别是找色函数findMultiColorInRegionFuzzy与识字函数Ocrtext,可以和官网上的找色工具与识字工具配合开发  

两个函数的关键使用与触动精灵差别不大，如果你有什么更好的想法或者问题，请联系我的邮箱ljl260435988@gmail.com

## 运行环境:
    windows10(150%放大倍数)
    夜神模拟器6.6.1.2(分辨率1920x1080)
# 使用说明

首先初始化对象并获取窗口句柄

```python
blRobot=Robot(class_name="subWin",title_name="sub",zoom_count=1.5)

blRobot.Get_GameHwnd()
```
接下来可以使用部分功能了，还有很多其他方式的实现就不一一说明

### 识字函数:
```python
xstr = blRobot.Ocrtext(tab,"303137,2F3036",173, 40, 285, 76)
```

### 找色函数:
```python
x,y = blRobot.findMultiColorInRegionFuzzy( "0xef6fdc", "24|5|0xffeecb,-7|30|0x2fb7ff", 90, 0, 0, 1919, 1079)
```

### 模拟虚拟机鼠标点击:

```python
blRobot.click(125,33)
```

# 已知问题:
1.已知手机界面的横竖模式会的x,y轴特有的显示方式可能会改变的核心代码处理逻辑,待优化  
2.findMultiColorInRegionFuzzy 参数2不能为空字符串 "" ,也就是说找色必须要有两个点以上才行,待优化