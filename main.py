# -*- coding: utf-8 -*-
from os import error

from numba.cuda.decorators import convert_types
import Robot as rb
import time
import pytesseract as pytes
from utils import *
from tesserocr import RIL
import Robot_help as rh
import math
import queue
from goto import with_goto
import json
import os
import data as da


pos_feature = (
    "0f800f1f801f3f003f3e007f7800fff001fff003eff007cff00f8ff01f0ff03e0f787c0f3ff80f3ff00f0fc007$2$185$24$15",
    "0e00fc1e007e3e003f7c001ff8380ff0380ff03c07f03c07f03c07f07c0ff07c0f78fe1f3ffffe3feffc0fc3fc0701f8$3$201$24$16",
    "0400001c00003e00003e00007fffffffffff7fffff$1$84$24$7",
    "700000700000f00000f00000f00000f003fff03ffff0fffffbff00fff800ffc000ff0000fe00007c0000700000$7$131$24$15",
    "07f8100ffc3c3ffe3e3fff1f780f0ff80f0ff00707f00707f00f0ff80f0f7c0f1f3e3fff3ffffe1ffffc03ffc000ff00$9$223$24$16",
    "0787f81fcffc3ffffe7fffff78fe0ff07c0ff03c07f03c07f03c07f87c0f78fc0f7ffe1f3ffffe1fcffc0703f80001f0$8$234$24$16",
    "03ffe00ffff83ffffc3ffffe7c000ff8000ff0000ff00007f0000ff8000f7c001f3e003f3ffffe1ffffc03ffe0$0$195$24$15",
    "0000c00003e00007e0001fe0003fe000fee001fce007f0e00fe0e03f80e07ffffcffffff7fffff3ffffe0001f00000e0000040$4$178$24$17",
    "03fff00ffff83ffffe3fffff78780ff8780ff0f00ff0f007f0f00ff0f00ff8f80f7c7c3f3e3ffe1c1ffc000ff0$6$216$24$15",
    "3ffc387ffc3cfffc3efffc1ff8f80ff0f00ff0f007f0e007f0e00ff0f00ff0f81ff07c3f703ffe701ffc0007e0$5$205$24$15",
    "700000700000f00000f00000f00000f001fff03ffff0fffffbff00fffc00ffc000ff8000fe00007c0000700000$7$132$24$15",
    "180fffffffc7f@000$,$39$11$5"
)



tu_text_features = ['图','T']
shop_emty = (727,651,"0x3f4a53"),(663,644,"0x3f4a53"),(623,645,"0x3f4a53"),(720,616,"0x3f4a53"),(718,683,"0x3f4a53"),(797,679,"0x3f4a53"),(855,675,"0x3f4a53"),(852,637,"0x3f4a53")
tu_money = 27999

feixingfu_jiemian = (1309,382, '0x0c5a9b'),(839,272, '0x1064a7'),(689,370, '0x1367a9'),(814,536, '0x166baa'),(927,669, '0x1160a0'),(1138,597, '0x196ca6'),(1432,674, '0x0c4e95'),(755,423, '0xe879aa'),(1165,550, '0xf0ce08'),(770,292, '0xebf200')
zhujiemian = (667,1015,'0xefc250'),(782,1024,'0xd89825'),(907,1022,'0xea8f4f'),(1022,1017,'0xf8cf48'),(1124,1020,'0xb75715')
fanhui = (1600,80, '0x183850'),(1586,67, '0x204057'),(1585,97, '0x18324a'),(1617,65, '0x183a4f'),(1616,95, '0x18324c'),(1620,82, '0x305b80'),(1603,63, '0x497fa3'),(1586,81, '0x305c80'),(1600,95, '0x32638c'),(1601,83,'0x183850')
start_map = (143,79)

flag_jiemian = (554,83,0x111830),(720,146,0x182428),(720,146,0x182428),(1411,93,0x11182f)


#"坐标计算": (609,226,1550,932,192,144)  609,226 是实际地图左上角的坐标 1550,932是实际地图右下角的坐标   192,144 是长和宽
Table_梦幻 = {
	"无名鬼蜮":{ "坐标计算":(712,304,1445,855,192,144),"返回":(1473,195)},
	"大唐国境":{ "坐标计算" : (624,146,1533,1013,352,336), "返回" :(1560,37)},
    "长安城":{ "坐标计算" :(266,187,1653,892,550,280),"返回" :(1674,86) },
	"地府" : { "坐标计算" : (596,218,1561,941,160,120), "返回" : (1588,108) },
	"地狱迷宫一层"  : { "坐标计算" : (608,226,1551,933,120,90), "返回" : (1578, 115) },
	"地狱迷宫二层" : { "坐标计算" : (604,222,1555,935,120,90), "返回" : (1582, 114) },
	"地狱迷宫三层" : { "坐标计算" : (598,218,1561,939,120,90), "返回" : (1590, 110) },
	"地狱迷宫四层" : { "坐标计算" : (598,218,1559,939,120,90), "返回" : (1584, 111) },
	"花果山" : {"坐标计算" : (611,227,1546,932,160,120),"返回" : (1571,120)},
    "北俱芦洲": {"坐标计算":(604,218,1554,938,228,170),"返回" :(1579,118)},
	"女娲神迹" : {"坐标计算": (609,226,1550,932,192,144), "返回" :(1583,128)},
	"大雁塔六层":{"坐标计算":(296,169,1623,908,138,77),"返回":(1647,68)},
	"大唐境外" : {"坐标计算":(187,393,1750,684,640,120), "返回":(1753,296)},
    "墨家村" : { "坐标计算" :(849,177,1310,982,96,168), "返回" :(1329,77)},
	"狮驼岭" : { "坐标计算" :(598,216,1558,938,132,99), "返回":(1575,117)},
	"普陀山" : { "坐标计算" :(605,223,1553,935,96,72), "返回" :(1577,120)},
	"五庄观" : { "坐标计算" :(605,223,1552,934,100,75), "返回":(1570,114)},
	"女儿村" : { "坐标计算" :(800,266,1358,892,128,144), "返回" :(1386,162)},
	"东海湾" : { "坐标计算" :(727,227,1432,932,120,120), "返回":(1454,123)},
	"建邺城" : { "坐标计算" :(250,185,1669,894,288,144), "返回" :(1702,81)},
	"傲来国" : { "坐标计算" :(431,183,1486,894,224,151), "返回":(1512,77)},
	"朱紫国" : { "坐标计算" :(382,175,1537,901,192,120), "返回":(1565,72)},
	"江南野外" : { "坐标计算":(601,221,1556,938,160,120), "返回":(1582,118)},
	"长寿郊外" : { "坐标计算":(677,227,1480,930,192,168), "返回" :(1505,124)},
	"长寿村" : { "坐标计算" :(797,210,1362,950,160,210), "返回":(1400,101)},
	"麒麟山" : { "坐标计算" :(597,227,1561,930,191,143), "返回":(1586,127)},
}






class action(rb.Robot):

    def __init__(self,q,class_name="subWin",title_name="sub",zoom_count=1.5):
        rb.Robot.__init__(self,class_name=class_name,title_name=title_name,zoom_count=zoom_count)
        self.Get_GameHwnd()
        self.cx = None
        self.error = list()
        if isinstance(q,queue.Queue):
            self.queue = q
        else:
            raise("参数2不是队列")
        
    @with_goto    
    def flag_transfer(self,color):
        while True:
            time.sleep(0.5)
            self.click(973,205)
            time.sleep(0.5)
            tpl = self.Print_screen()
            if color == "red":
                target = cv2.imread("./images/red_flag.png")
                x,y = self.matchTemplate(tpl,target,0.13)
                if x != -1:
                    self.click(x,y)
                    self.click(x,y)
                    break
                else:
                    goto .end
            elif color == "yellow":
                target = cv2.imread("./images/yellow_flag.png")
                x,y = self.matchTemplate(tpl,target,0.13)
                if x != -1:
                    self.click(x,y)
                    self.click(x,y)
                    break
                else:
                    goto .end
            elif color == "blue":
                target = cv2.imread("./images/blue_flag.png")
                x,y = self.matchTemplate(tpl,target,0.13)
                if x != -1:
                    self.click(x,y)
                    self.click(x,y)
                    break
                else:
                    goto .end
            elif color == "green":
                target = cv2.imread("./images/green_flag.png")
                x,y = self.matchTemplate(tpl,target,0.13)
                if x != -1:
                    self.click(x,y)
                    self.click(x,y)
                    break
                else:
                    goto .end
            elif color == "white":
                target = cv2.imread("./images/white_flag.png")
                x,y = self.matchTemplate(tpl,target,0.13)
                if x != -1:
                    self.click(x,y)
                    self.click(x,y)
                    break
                else:
                    goto .end
            else:
                label .end
                #没找到，去行囊里面找
                self.click(1252,203)
                time.sleep(0.5)
                tpl = self.Print_screen()
                while True:
                    if color == "red":
                        target = cv2.imread("./images/red_flag.png")
                        x,y = self.matchTemplate(tpl,target,0.05)
                        if x != -1:
                            self.click(x,y)
                            self.click(x,y)
                            break
                    elif color == "yellow":
                        target = cv2.imread("./images/yellow_flag.png")
                        x,y = self.matchTemplate(tpl,target,0.05)
                        if x != -1:
                            self.click(x,y)
                            self.click(x,y)
                            break
                    elif color == "blue":
                        target = cv2.imread("./images/blue_flag.png")
                        x,y = self.matchTemplate(tpl,target,0.05)
                        if x != -1:
                            self.click(x,y)
                            self.click(x,y)
                            break
                    elif color == "green":
                        target = cv2.imread("./images/green_flag.png")
                        x,y = self.matchTemplate(tpl,target,0.05)
                        if x != -1:
                            self.click(x,y)
                            self.click(x,y)
                            break
                    elif color == "white":
                        target = cv2.imread("./images/white_flag.png")
                        x,y = self.matchTemplate(tpl,target,0.05)
                        if x != -1:
                            self.click(x,y)
                            self.click(x,y)
                            break
                    else:
                        print("not found flags")
                        return State.NOTMATCH
        return State.OK
        
        
    def find_map_by_shop(self):
        tpl = self.Print_screen()
        start_pos = [285,196,532,244] #第一个摊位
        conversion = [285,196,532,244]
        #self.show(tpl)
        tu_shop = list()
        xret = list()
        jump = False
        xret.clear()
        for i in range(0,5):
            if jump:
                break
            conversion[1] = start_pos[1] + i*144
            conversion[3] = start_pos[3] + i*144
            for j in range(0,4):
                conversion[0] = start_pos[0] + j*341
                conversion[2] = start_pos[2] + j*341
                #print("conversion{0}".format(conversion))
                e_shop_emty = self.findMultiColorInRegionFuzzyByTable(shop_emty,90,conversion[0],conversion[1],conversion[2],conversion[3])                
                if e_shop_emty[0] == State.OK:
                    print("发现空摊位")
                    jump = True
                    break
                tu_shop = self.tsOcrText(tpl,tu_text_features,conversion[0],conversion[1],conversion[2],conversion[3]) 
                if len(tu_shop):
                    print("ret:{0}".format(tu_shop))
                    xret.append(tu_shop[0])
        return xret
    
    def buy_map(self):
        #点击系统界面
        self.click(673,1025)
        time.sleep(2)
        self.click(1260,729)
        time.sleep(2)
        tpl = self.Print_screen()
        max_page = int(self.OcrText(tpl,1411, 921, 1447, 962,config=('--oem 1 -l chi_sim --psm 7 '))[0][0])
        print(max_page)
        for i in range(1,max_page+1):
          shop_pos_list = self.find_map_by_shop()
          if len(shop_pos_list):
             print("发现摊位坐标:{0}".format(shop_pos_list))
             for j in shop_pos_list:
                x = j[1]
                y = j[2]
                print("点击摊位坐标:({0},{1})".format(x,y))
                self.click(x,y)
                time.sleep(2)
                self.click(1700,82)
                time.sleep(2)
          if i >= max_page:
                continue
          else:
                print("点击下一页")   
                self.click(1549,937) 
                time.sleep(2)
                
    
    def run_with_callback(self,fun,fun_param,pre_fun1,fun1_param,post_fun2,fun2_param):
        try:
            print("start pre_fun1")
            ret = pre_fun1(fun_param)
            ret = fun(ret,fun1_param)
            ret = post_fun2(ret,fun2_param)
            self.cx = ret
        except Exception as identifier:
            self.error.append(identifier)
    '''
    在各主城增加了仓库管理员NPC，坐标分别为：长安城（346，244）、长安城（224，141）、建邺城（54，32)、傲来国（143，101）、长寿村（111，62）、朱紫国（126，90）
    '''
    #check_map 打开道具栏遍历宝图
    def check_map(self):
        n,nn,nnn,nnnn=None,None,None,None
        #打开道具栏
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1028)
        time.sleep(1)
        tpl = self.Print_screen()
        target = cv2.imread("./images/tu.png")
        start_pos = (902,269,1013,378)
        convert_pos = [902,269,1013,378]
        tu_list = list()
        for i in range(0,5):
            time.sleep(0.5)
            convert_pos[0] = start_pos[0] + i*134
            convert_pos[2] = start_pos[2] + i*134
            for j in range(0,4):
                time.sleep(0.5)
                print(j)
                convert_pos[1] = start_pos[1] + j*134
                convert_pos[3] = start_pos[3] + j*134
                self.click(convert_pos[0]+5,convert_pos[1]+5)
                time.sleep(0.5)
                tpl = self.Print_screen()
                #self.show(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]])
                x,y = self.matchTemplate(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]],target,0.15)
                if x != -1:
                    print("找到宝图")
                    time.sleep(0.5)
                    data = self.x_Ocrtext(da.ditu,"00E804,011805#03DC07,032006#08DD0B,072009",444,506,589,560)
                    print(data)                    
                    if data:
                        if len(data)>3:
                            pos = self.Ocrtext("06BE0B,06420B#00E804,011805#03DC07,032006#08DD0B,072009",
                                               591,511,732,547,ril=RIL.TEXTLINE,
                                               lang='eng',oem=1,
                                               attribute=["tessedit_char_whitelist", 
                                                "0123456789,"])[0]
                            print(pos)
                            try:
                                pos['text'] = pos['text'].replace("\n","")
                                _x = int(pos['text'].split(',')[0])
                                _y = int(pos['text'].split(',')[1])
                                tu_list.append((data,_x,_y,convert_pos[0]+5,convert_pos[1]+5))
                            except:
                                print("使用tesseract解析字体异常，正在使用字库")
                                postr = self.z_Ocrtext(da.map_font,"06BE0B,06420B#03E105,031E05#00E804,011805#03DC07,032006#08DD0B,072009"
                                                ,555,513,693,548,)
                                if len(pos):
                                    postr = pos.replace("\n","")
                                    try:
                                        _x = int(postr.split(',')[0])
                                        _y = int(postr.split(',')[1])
                                        tu_list.append((data,_x,_y,convert_pos[0]+5,convert_pos[1]+5))
                                    except Exception as e:
                                        print("字库解析异常") 
                                
                        else:
                            pos = self.Ocrtext("06BE0B,06420B#03E105,031E05#00E804,011805#03DC07,032006#08DD0B,072009"
                                               ,555,513,693,548,ril=RIL.TEXTLINE,
                                               lang='eng',oem=1,
                                               attribute=["tessedit_char_whitelist",
                                                "0123456789,"])[0]
                            print(pos)
                            try:
                                _x = int(pos['text'].split(',')[0])
                                _y = int(pos['text'].split(',')[1])
                                tu_list.append((data,_x,_y,convert_pos[0]+5,convert_pos[1]+5))
                            except:
                                print("使用tesseract解析字体异常，正在使用字库")
                                postr = self.z_Ocrtext(da.map_font,"06BE0B,06420B#03E105,031E05#00E804,011805#03DC07,032006#08DD0B,072009"
                                                ,555,513,693,548,)
                                if len(pos):
                                    postr = pos.replace("\n","")
                                    try:
                                        _x = int(postr.split(',')[0])
                                        _y = int(postr.split(',')[1])
                                        tu_list.append((data,_x,_y,convert_pos[0]+5,convert_pos[1]+5))
                                    except Exception as e:
                                        print("字库解析异常")
                                
        return  tu_list
    
    
    def go_to_CSC(self):
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(feixingfu_jiemian)
            if status==status.OK:
                time.sleep(0.7)
                self.click(762,309)
                time.sleep(0.7)
                break
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往长寿村")
                status,ag= self.findMultiColorInRegionFuzzyByTable(fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(0.5)
            elif status==status.OK:
                print("抵达长寿村")
                break
        return True
    #TAPP 计算坐标
    def TAPP(self,D,xx,yy):
        rx = Table_梦幻[D]["坐标计算"][0] +  (((Table_梦幻[D]["坐标计算"][2] - Table_梦幻[D]["坐标计算"][0]) / Table_梦幻[D]["坐标计算"][4]) * xx+0)
        ry = Table_梦幻[D]["坐标计算"][3] - (((Table_梦幻[D]["坐标计算"][3] - Table_梦幻[D]["坐标计算"][1]) / Table_梦幻[D]["坐标计算"][5]) * yy+0)
        _min,_max = math.modf(rx)
        if _min>=0.5:
            rx = _max+1
        else:
            rx = _max                                                                                                                                                                                                                        
        _miny,_maxy = math.modf(ry) 
        if _miny>=0.5:
            ry = _maxy+1
        else:
            ry = _maxy
        return rx,ry
        
    def rgb_array(self,table_name):
        ddegree = table_name["范围参数"][0]
        x1 = table_name["范围参数"][1]
        y1 =  table_name["范围参数"][2]
        x2 =  table_name["范围参数"][3]
        y2 =  table_name["范围参数"][4]
        status,ag= self.findMultiColorInRegionFuzzyByTable(table_name["坐标"],ddegree,x1,y1,x2,y2)
        if status==status.OK:
            return status.OK
        else:
            return status.NOTMATCH
        
    #前往长寿郊外
    def go_to_CSJW(self):
        ok = self.go_to_CSC()
        if ok:
            pass
    def tap_(self,D,X,Y):
        while True:
            ##self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
            if status==status.NOTMATCH:
                x,y=self.TAPP(D,X,Y)
                self.click(x,y)
                time.sleep(1)
                self.click(Table_梦幻[D]["返回"][0],Table_梦幻[D]["返回"][1])
                time.sleep(2)
                break
        print("监控坐标")
        while True:
            #self.queue.put("check")
            # pos = self.Ocrtext("C4CED1,3C322E",158, 93, 284, 126,
            #                     lang='eng',oem=1,
            #                     attribute=["tessedit_char_whitelist", 
            #                     "0123456789,"],THRESH_GAUSSIAN=False)
            pos = self.z_Ocrtext(pos_feature,"C4CED1,3C322E",158, 93, 284, 126)
            if len(pos):
                postr = pos.replace("\n","")
                try:
                    _x = int(postr.split(',')[0])
                    _y = int(postr.split(',')[1])
                    time.sleep(1)
                    print("当前坐标(x:{0},y:{1})----实际坐标(x:{2},y:{3})".format(str(_x),str(_y),str(X),str(Y)))
                    if (abs(X-_x)<3) and (abs(Y-_y)<3):
                        break
                except Exception as e:
                    print(postr)
                    
                    
    def discover_feixingfu(self):
        tpl = self.Print_screen()
        status = State.NOTMATCH
        target = cv2.imread("./images/feixingfu.png")
        x,y = self.matchTemplate(tpl,target,0.15)
        if x != -1:
            print("发现飞行符")
            return State.OK,x,y
        return State.NOTMATCH,x,y
    
    def no_prop(self):
        tpl = self.Print_screen()
        target = cv2.imread("./images/daojulanzhankai.png")
        x,y = self.matchTemplate(tpl,target,tolerance=0.1)
        if x != -1:
            return True
        else:
            return False  
    def quit(self):
        self.queue.put("exit")
        
    #去往长寿郊外    
    def Tothecountryside(self):
        #确保道具栏没有被收起来
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1015)
        time.sleep(1)
        status,x,y= self.discover_feixingfu()
        if status == status.OK:
            print(x,y)
        self.click(x,y)
        time.sleep(1)
        tpl = self.Print_screen()
        target = cv2.imread("./images/shiyong.png")
        x,y = self.matchTemplate(tpl,target)
        if x != -1:
            self.click(x,y)
        else:
            print("飞行符没有使用")
            return
        time.sleep(1)
        self.go_to_CSC()
        #打开地图
        time.sleep(1)
        self.click(60,81)
        time.sleep(1)        
        if self.rgb_array(da.map_feature["长寿村"])==State.OK:
            self.tap_("长寿村",144,6)   
            time.sleep(0.5)
            while True:
                #self.queue.put("check")
                status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
                if status==status.NOTMATCH:
                    time.sleep(0.5)        
                else:
                    time.sleep(1)
                    self.click(61,378) #屏蔽玩家
                    time.sleep(1)
                    self.click(64,844) #屏蔽界面
                    time.sleep(1)
                    self.click(1849,1018) 
                    time.sleep(1)
                    self.click(64,844) 
                    time.sleep(1)
                    while True:
                        #self.queue.put("check")
                        reponse = self.Ocrtext("1C1D21,1B1C20",151, 36, 307, 77,THRESH_GAUSSIAN=False)[0]
                        reponse = reponse["text"].replace("\n","")
                        reponse = reponse.replace(" ","")
                        if  reponse in "长寿郊外":
                            print("抵达目的地")
                            return
                        
                
    def go_to_ZZG(self):
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(feixingfu_jiemian)
            if status==status.OK:
                time.sleep(0.7)
                self.click(860,729)
                time.sleep(0.7)
                break
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往朱紫国")
                status,ag= self.findMultiColorInRegionFuzzyByTable(fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(2)
            elif status==status.OK:
                while True:
                    reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
                    if  "朱紫国" in reponse:
                        print("抵达朱紫国")
                        break
                break
        return True
    
    #去往大唐境外
    def TotheDTJW(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1015)
        time.sleep(1)
        status,x,y= self.discover_feixingfu()
        if status == status.OK:
            print(x,y)
        self.click(x,y)
        time.sleep(1)
        tpl = self.Print_screen()
        target = cv2.imread("./images/shiyong.png")
        x,y = self.matchTemplate(tpl,target)
        if x != -1:
            self.click(x,y)
        else:
            print("飞行符没有使用")
            return
        #self.click(654,669)
        time.sleep(1)
        self.go_to_ZZG()
        #打开地图
        time.sleep(1)
        self.click(60,81)
        time.sleep(1)        
        if self.rgb_array(da.map_feature["朱紫国"])==State.OK:
            self.tap_("朱紫国",6,4)   
            time.sleep(0.5)
            while True:
                #self.queue.put("check")
                status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
                if status==status.NOTMATCH:
                    time.sleep(0.5)        
                else:
                    time.sleep(1)
                    self.click(61,378) #屏蔽玩家
                    time.sleep(1)
                    self.click(64,844) #屏蔽界面
                    time.sleep(1)
                    self.click(104,1000) 
                    time.sleep(1)
                    self.click(104,1000)
                    time.sleep(1)
                    while True:
                        ##self.queue.put("check")
                        reponse = self.Ocrtext("1C1D21,1B1C20",151, 36, 307, 77,THRESH_GAUSSIAN=False)[0]
                        reponse = reponse["text"].replace("\n","")
                        reponse = reponse.replace(" ","")
                        if  reponse in "大唐境外":
                            print("抵达目的地")
                            return
    #前往墨家村
    def TotheMJC(self):
        self.TotheDaTangJingWai()
        self.click(60,81)
        time.sleep(1)
        while True:
            if self.rgb_array(da.map_feature["大唐境外A"])==State.OK:
                print("OK")
                break
            else:        
                time.sleep(0.5)
        self.tap_("大唐境外",233,109)
        self.click(1136,220)
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.map_feature["送我进墨家村"]["坐标"])
            if status == status.NOTMATCH:
                time.sleep(0.5)
            else:
                self.click(1562,376)
                time.sleep(0.5)
                break
        while True:
            ##self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
            if  "墨家村" in reponse:
                print("抵达目的地")
                return
    #前往大唐国境        
    def ToDTGJ(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1015)
        time.sleep(0.2)        
        self.flag_transfer("red")
        time.sleep(0.5)
        q = False
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(flag_jiemian)
            if status==status.NOTMATCH:
                if q:
                    self.click(1609,85)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
                    if status==status.NOTMATCH:
                        time.sleep(0.5)        
                    else:
                        break
            else:
                q = True
                self.click(271,900)
                time.sleep(0.2)
        time.sleep(1)
        self.click(61,378) #屏蔽玩家
        time.sleep(1)
        self.click(64,844) #屏蔽界面
        time.sleep(1)
        self.click(104,1000) 
        time.sleep(1)
        self.click(104,1000)
        time.sleep(1)
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
            if  "大唐国境" in reponse:
                print("抵达目的地")
                return
            
    #前往麒麟山
    def TotheQLS(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1015)
        time.sleep(1)
        status,x,y= self.discover_feixingfu()
        if status == status.OK:
            print(x,y)
        self.click(x,y)
        time.sleep(1)
        tpl = self.Print_screen()
        target = cv2.imread("./images/shiyong.png")
        x,y = self.matchTemplate(tpl,target)
        if x != -1:
            self.click(x,y)
        else:
            print("飞行符没有使用")
            return
        #self.click(654,669)
        time.sleep(1)
        self.go_to_ZZG()
        #打开地图
        time.sleep(1)
        self.click(60,81)
        time.sleep(1)        
        if self.rgb_array(da.map_feature["朱紫国"])==State.OK:
            self.tap_("朱紫国",3,111)   
            time.sleep(0.5)
            while True:
                status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
                if status==status.NOTMATCH:
                    time.sleep(0.5)
                else:
                    time.sleep(1)
                    self.click(61,378) #屏蔽顽疾
                    time.sleep(1)
                    self.click(64,844) #屏蔽界面
                    time.sleep(1)
                    self.click(83,222) 
                    time.sleep(1)
                    self.click(64,844) 
                    time.sleep(1)
                    while True:
                        #self.queue.put("check")
                        reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
                        if  "麒麟山" in reponse:
                            print("抵达目的地")
                            return
    #前往狮驼岭
    def TotheSTL(self):
        self.TotheDaTangJingWai()
        self.click(60,81)
        time.sleep(1)
        while True:
            if self.rgb_array(da.map_feature["大唐境外A"])==State.OK:
                print("OK")
                break
            else:        
                time.sleep(0.5)
        self.tap_("大唐境外",7,49)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
            if status==status.NOTMATCH:
                time.sleep(0.5)
            else:
                time.sleep(1)
                self.click(61,378) 
                time.sleep(1)
                self.click(64,844) #屏蔽界面
                time.sleep(1)
                self.click(104,1000)
                time.sleep(1)
                self.click(191,562)
                time.sleep(1)
                while True:
                    #self.queue.put("check")
                    reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
                    if  "狮驼岭" in reponse:
                        print("抵达目的地")
                        return
    #前往东海湾        
    def ToTheDHW(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1015)
        time.sleep(0.2)        
        self.flag_transfer("yellow")
        time.sleep(0.5)
        q = False
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(flag_jiemian)
            if status==status.NOTMATCH:
                if q:
                    self.click(1609,85)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
                    if status==status.NOTMATCH:
                        time.sleep(0.5)        
                    else:
                        break
            else:
                q = True
                self.click(1224,840)
                time.sleep(0.2)
        time.sleep(1)
        self.click(949,609)
        time.sleep(1)
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.map_feature["我要去"]["坐标"])
            if status == status.NOTMATCH:
                time.sleep(0.5)
            else:
                self.click(1449,509)
                time.sleep(0.5)
                break        
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
            if  "东海湾" in reponse:
                print("抵达目的地")
                return
    #前往江南野外        
    def ToTheJNYW(self):
        while True:
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1015)
        time.sleep(0.2)        
        self.flag_transfer("red")
        time.sleep(0.5)
        q = False
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(flag_jiemian)
            if status==status.NOTMATCH:
                if q:
                    self.click(1609,85)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
                    if status==status.NOTMATCH:
                        time.sleep(0.5)        
                    else:
                        break
            else:
                q = True
                self.click(1603,907)
                time.sleep(0.2)
        time.sleep(1)
        self.click(949,609)
        time.sleep(1)
        self.click(1828,1020)
        time.sleep(1)
        self.click(1713,1057)
        while True:
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
            if  "江南野外" in reponse:
                print("抵达目的地")
                break            
        while True:
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
    #前往花果山
    def ToTheHGS(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1015)
        time.sleep(0.2)        
        self.flag_transfer("yellow")
        time.sleep(0.5)
        q = False
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(flag_jiemian)
            if status==status.NOTMATCH:
                if q:
                    self.click(1609,85)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
                    if status==status.NOTMATCH:
                        time.sleep(0.5)        
                    else:
                        break
            else:
                q = True
                #
                self.click(1448,243)
                time.sleep(0.2)
        time.sleep(1)
        self.click(1658,105)
        time.sleep(1)      
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
            if  "花果山" in reponse:
                print("抵达目的地")
                return
            
    def ToTheALG(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1015)
        time.sleep(1)
        status,x,y= self.discover_feixingfu()
        if status == status.OK:
            print(x,y)
        self.click(x,y)
        time.sleep(1)
        tpl = self.Print_screen()
        target = cv2.imread("./images/shiyong.png")
        x,y = self.matchTemplate(tpl,target)
        if x != -1:
            self.click(x,y)
        else:
            print("飞行符没有使用")
            return
        time.sleep(1)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(feixingfu_jiemian)
            if status==status.OK:
                time.sleep(0.7)
                self.click(1525,788)
                time.sleep(0.7)
                break
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(zhujiemian)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往傲来国")
                status,ag= self.findMultiColorInRegionFuzzyByTable(fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(1)
            elif status==status.OK:
                while True:
                    reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
                    if  "傲来国" in reponse:
                        print("抵达傲来国")
                        break
                break
        return True
    
    def ToTheWZG(self):
        self.ToDTGJ()
        #打开地图
        time.sleep(1)
        self.click(60,81)
        time.sleep(1)
        while True:
            if self.rgb_array(da.map_feature["大唐国境"])==State.OK:
                print("OK")
                break
            else:        
                time.sleep(0.5)
        time.sleep(1)
        self.tap_("大唐国境",5,79)
        time.sleep(0.5)
        self.click(61,378) 
        time.sleep(1)
        self.click(64,844) #屏蔽界面
        time.sleep(1)
        self.click(14,316)
        time.sleep(1)
        self.click(64,844) #屏蔽界面
        time.sleep(1)
        
        self.click(60,81)
        time.sleep(1)        
        while True:
            if self.rgb_array(da.map_feature["大唐境外A"])==State.OK:
                print("OK")
                break
            else:        
                time.sleep(0.5)
        
        time.sleep(1)
        self.tap_("大唐境外",633,76)
        time.sleep(0.5)
        self.click(61,378) 
        time.sleep(1)
        self.click(64,844) #屏蔽界面
        time.sleep(1)
        self.click(1722,176)
        time.sleep(1)
        self.click(64,844) #屏蔽界面
        time.sleep(1)
        while True:
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
            if  "五庄观" in reponse:
                print("抵达五庄观")
                break
                
    def open_prop(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1828,1020)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1695,1015)
        
    #前往普陀山
    def ToThePTS(self):
        self.ToDTGJ()
        time.sleep(1)
        self.click(60,81)
        time.sleep(1)
        while True:
            if self.rgb_array(da.map_feature["大唐国境"])==State.OK:
                print("OK")
                break
            else:        
                time.sleep(0.5)        
        time.sleep(1)
        self.tap_("大唐国境",228,58)
        time.sleep(0.5)        
        while True:
            if self.rgb_array(da.map_feature["传送仙女"])==State.OK:
                print("OK")
                self.click(760,392)
                time.sleep(0.5)
                break
            else:        
                time.sleep(0.5)    
        while True:
            if self.rgb_array(da.map_feature["我要去"])==State.OK:
                print("OK")
                self.click(1579,509)
                time.sleep(0.5)
                break
            else:        
                time.sleep(0.5)
        while True:
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",151, 36, 307, 77)
            if  "普陀山" in reponse:
                print("抵达普陀山")
                break
    
            
                                      
    def Orb(self):
        tulist = self.check_map()
        mapInfomation = {"tu":tulist}
        with open("./角色信息.json", 'w',encoding="utf-8") as f:
            json.dump(mapInfomation,f,ensure_ascii=False,indent = 4)
        load_dict = None
        time.sleep(1)
        with open("./角色信息.json", 'r',encoding="utf-8") as f:
            load_dict  = json.load(f)
        maps =  load_dict["tu"]
        if isinstance(maps,list):
            for m in maps:
                place = m[0]
                place_x = m[1]
                place_y = m[2]
                backpack_x = m[3]
                backpack_y = m[4]
                if place in "长寿郊外":
                    self.Tothecountryside()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("长寿郊外",place_x,place_y)
                    self.open_prop()
                    self.click(backpack_x,backpack_y)
                    self.click(backpack_x,backpack_y)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                elif place in "大唐国境":
                    self.ToDTGJ()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("大唐国境",place_x,place_y)
                    self.open_prop()
                    self.click(backpack_x,backpack_y)
                    self.click(backpack_x,backpack_y)
                    self.click(1609,85)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                elif place in "大唐境外":
                    self.TotheDTJW()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("大唐境外",place_x,place_y)
                    self.open_prop()
                    self.click(backpack_x,backpack_y)
                    self.click(backpack_x,backpack_y)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                elif place in "麒麟山":
                    self.TotheQLS()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("麒麟山",place_x,place_y)
                    self.open_prop()
                    self.click(backpack_x,backpack_y)
                    self.click(backpack_x,backpack_y)
                    time.sleep(1)   
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                elif place in "狮驼岭":
                    self.TotheSTL()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("狮驼岭",place_x,place_y)
                    self.open_prop()
                    self.click(backpack_x,backpack_y)
                    self.click(backpack_x,backpack_y)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                elif place in "朱紫国":
                    self.go_to_ZZG()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("朱紫国",place_x,place_y)
                    self.open_prop()
                    self.click(backpack_x,backpack_y)
                    self.click(backpack_x,backpack_y)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                elif place in "花果山":
                    self.ToTheHGS()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("花果山",place_x,place_y)
                    self.open_prop()
                    self.click(backpack_x,backpack_y)
                    self.click(backpack_x,backpack_y)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                elif place in "东海湾":
                    self.ToTheDHW()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("东海湾",place_x,place_y)
                    self.open_prop()
                    self.click(backpack_x,backpack_y)
                    self.click(backpack_x,backpack_y)
                    self.click(1609,85)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                elif place in "江南野外":
                    self.ToTheJNYW()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("江南野外",place_x,place_y)
                    self.open_prop()
                    self.click(backpack_x,backpack_y)
                    self.click(backpack_x,backpack_y)
                    self.click(1609,85)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                elif place in "傲来国":
                    self.ToTheALG()
                    time.sleep(1)
                    self.click(60,81)
                    time.sleep(1)   
                    self.tap_("傲来国",place_x,place_y)
                    self.open_prop()
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                        if status == State.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            time.sleep(1)
                            self.click(1609,85)
                            break
                        else:
                            time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                    if status==status.NOTMATCH:
                        pass
                    else:
                        time.sleep(1)
                        self.click(1600,80)
                        time.sleep(1)
                        self.queue.put("check")
                        self.queue.join()
                else:
                    print("所在地址没找到")
                    os._exit(0)
                    
                    
                    
def main():
    zoom_count = 1.5
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    Robot.ToThePTS()

    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()
    
    
if __name__ == "__main__":
    main()