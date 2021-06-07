
# pyAutomated
The project is designed to simulate key-and-mouse clicking on the Android virtual machine (I use VBox) across platforms to achieve automation.



### Project Advantages:  

1. Image based data provided to machine learning has a good action interface


3. It does not call the API of the Guest system, but calls the virtual machine interface from outside the host, which has a strong invisibility

4. Cross-platform. There's nothing better than that  



Demo video:[ pyAutomated demo](https://www.bilibili.com/video/BV1Ev411t7B1/)

Match the pictures and OCRText engine.
The core engine is inspired by the [ touchsprite.com ](https://www.touchsprite.com/),So you need its tools to be developed to touchsprite syntax.


If you have any better ideas or questions, please contact me at email

ljl260435988@gmail.com


## System Runtime environment:
    ubuntu 20.04 or windows 7/10
    vbox 6.1.22 (you need to enable webservice)
    conda python3.7.9

## Python Runtime environment：
    numpy>=1.18.5
    numba>=0.50.1
    Pillow>=8.1.1
    pynput>=1.7.1
    pytesseract>=0.3.6
    opencv-python>=4.4.0.46
    func_timeout>=4.3.5
    remotevbox>=1.0.1

## Enable Virtualbox webservice
[ Enable Virtualbox webservice on windows7/10 ](https://www.how2shout.com/how-to/how-create-virtualbox-webservice-as-system-service-on-windows-10-7.html)   

[ Enable Virtualbox webservice on Linux](https://www.virtualbox.org/manual/ch09.html#vboxwebsrv-daemon)


 

# instructions

1.Init object
```python
blRobot=Robot()
blRobot.Get_GameHwnd(Simulator_Name="vbox",game_width=1280,game_height=720)
```

2.example

### The Function Ocrtext
```python
xstr=blRobot.Ocrtext(test,"00E804,011805#03DC07,032006#08DD0B,072009",444,506,589,560)

--------------------------
pirnt("xstr=",xstr)
xstr="helloWorld"

```
### The Function findMultiColorInRegionFuzzy:
```python
status,ag= blRobot.findMultiColorInRegionFuzzy( "0xef6fdc", "24|5|0xffeecb,-7|30|0x2fb7ff", 90, 0, 0, 1919, 1079)
-------------------------------------------
pirnt("ag=",ag)
ag=(667,1015)
```

### The Function findMultiColorInRegionFuzzyByTable:
```python
zhujiemian = (667,1015,'0xefc250'),(782,1024,'0xd89825'),(907,1022,'0xea8f4f'),(1022,1017,'0xf8cf48'),(1124,1020,'0xb75715')
status,ag=self.findMultiColorInRegionFuzzyByTable(zhujiemian)
-------------------------------------------
pirnt("ag=",ag)
ag=(667,1015)
```

### The Function mouse click:
```python
blRobot.click(125,33)
```


### How About use of tools and learn touchsprite syntax?
Answer: The use of tools and learn touchsprite syntax.You need to be very good in Chinese to read the instructions on the website: [https://helpdoc.touchsprite.com/dev_docs/598.html](https://helpdoc.touchsprite.com/dev_docs/598.html).    
Those tools were developed on Windows, so the experience on Linux was poor.
At present, I can use Wine to successfully run the touchsprite ColorTools, but the Word Finding Tool cannot run successfully. At present, there is no convenient solution. I am waiting for the secondary development of new tools when I am free. If you're interested in wasting your time here, please contact me about your assistives development project, or give me a cup of coffee to keep me motivated.




