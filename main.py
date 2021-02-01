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
            self.click(653,132)
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
                self.click(833,140)
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
        
        
    # def find_map_by_shop(self):
    #     tpl = self.Print_screen()
    #     start_pos = [285,196,532,244] #第一个摊位
    #     conversion = [285,196,532,244]
    #     #self.show(tpl)
    #     tu_shop = list()
    #     xret = list()
    #     jump = False
    #     xret.clear()
    #     for i in range(0,5):
    #         if jump:
    #             break
    #         conversion[1] = start_pos[1] + i*144
    #         conversion[3] = start_pos[3] + i*144
    #         for j in range(0,4):
    #             conversion[0] = start_pos[0] + j*341
    #             conversion[2] = start_pos[2] + j*341
    #             #print("conversion{0}".format(conversion))
    #             e_shop_emty = self.findMultiColorInRegionFuzzyByTable(shop_emty,90,conversion[0],conversion[1],conversion[2],conversion[3])                
    #             if e_shop_emty[0] == State.OK:
    #                 print("发现空摊位")
    #                 jump = True
    #                 break
    #             tu_shop = self.tsOcrText(tpl,tu_text_features,conversion[0],conversion[1],conversion[2],conversion[3]) 
    #             if len(tu_shop):
    #                 print("ret:{0}".format(tu_shop))
    #                 xret.append(tu_shop[0])
    #     return xret
    
    # def buy_map(self):
    #     #点击系统界面
    #     self.click(673,1025)
    #     time.sleep(2)
    #     self.click(1260,729)
    #     time.sleep(2)
    #     tpl = self.Print_screen()
    #     max_page = int(self.OcrText(tpl,1411, 921, 1447, 962,config=('--oem 1 -l chi_sim --psm 7 '))[0][0])
    #     print(max_page)
    #     for i in range(1,max_page+1):
    #       shop_pos_list = self.find_map_by_shop()
    #       if len(shop_pos_list):
    #          print("发现摊位坐标:{0}".format(shop_pos_list))
    #          for j in shop_pos_list:
    #             x = j[1]
    #             y = j[2]
    #             print("点击摊位坐标:({0},{1})".format(x,y))
    #             self.click(x,y)
    #             time.sleep(2)
    #             self.click(1700,82)
    #             time.sleep(2)
    #       if i >= max_page:
    #             continue
    #       else:
    #             print("点击下一页")   
    #             self.click(1549,937) 
    #             time.sleep(2)
                
    
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
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        
        self.click(1121, 673)
        
        time.sleep(1)
        tpl = self.Print_screen()
        target = cv2.imread("./images/tu.png")
        start_pos = (604,179,680,255)
        convert_pos = [604,179,680,255]
        tu_list = list()
        for i in range(0,5):
            time.sleep(0.5)
            convert_pos[0] = start_pos[0] + i*97
            convert_pos[2] = start_pos[2] + i*97
            for j in range(0,4):
                time.sleep(0.5)
                print(j)
                convert_pos[1] = start_pos[1] + j*97
                convert_pos[3] = start_pos[3] + j*97
                self.click(convert_pos[0]+5,convert_pos[1]+5)
                time.sleep(0.5)
                tpl = self.Print_screen()
                #self.show(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]])
                x,y = self.matchTemplate(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]],target,0.13)
                if x != -1:
                    print("找到宝图")
                    while True:
                       if self.rgb_array(da.ditu_show["道具栏显示地图字体"]) == State.OK:
                           break
                       else:
                           time.sleep(1)
                    #这里判断下提示框
                    tpl = self.Print_screen()
                    #检测字体
                    data = self.x_Ocrtext(da.ditu,"00E804,011805#03DC07,032006#08DD0B,072009",297,338,394,366)
                    print(data)                    
                    if data:
                        if len(data)>3:
                            pos = self.Ocrtext("06BE0B,06420B#00E804,011805#03DC07,032006#08DD0B,072009",
                                               401,  343,480,  364,ril=RIL.TEXTLINE,
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
                                                ,401,  343,480,  364,)
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
                                               ,379,343,455,365,ril=RIL.TEXTLINE,
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
                                                ,379,343,455,365,)
                                if len(pos):
                                    postr = pos.replace("\n","")
                                    try:
                                        _x = int(postr.split(',')[0])
                                        _y = int(postr.split(',')[1])
                                        tu_list.append((data,_x,_y,convert_pos[0]+5,convert_pos[1]+5))
                                    except Exception as e:
                                        print("字库解析异常")
                                
        return  tu_list
    
    
    #前往长寿村
    def go_to_CSC(self):
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.feixingfu_jiemian)
            if status==status.OK:
                time.sleep(0.7)
                self.click(512,202)
                time.sleep(0.7)
                break
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往长寿村")
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(0.5)
            elif status==status.OK:
                print("抵达长寿村")
                break
        return True
    
    #TAPP 计算坐标
    def TAPP(self,D,xx,yy):
        rx = da.Table_梦幻[D]["坐标计算"][0] +  (((da.Table_梦幻[D]["坐标计算"][2] - da.Table_梦幻[D]["坐标计算"][0]) / da.Table_梦幻[D]["坐标计算"][4]) * xx+0)
        ry = da.Table_梦幻[D]["坐标计算"][3] - (((da.Table_梦幻[D]["坐标计算"][3] - da.Table_梦幻[D]["坐标计算"][1]) / da.Table_梦幻[D]["坐标计算"][5]) * yy+0)
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
    # def go_to_CSJW(self):
    #     ok = self.go_to_CSC()
    #     if ok:
    #         pass
        
    def tap_(self,D,X,Y):
        while True:
            ##self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            if status==status.NOTMATCH:
                x,y=self.TAPP(D,X,Y)
                self.click(x,y)
                time.sleep(1)
                self.click(da.Table_梦幻[D]["返回"][0],da.Table_梦幻[D]["返回"][1])
                time.sleep(2)
                break
        print("监控坐标")
        while True:
            #C4CED1,3C322E
            #self.queue.put("check")
            # pos = self.Ocrtext("C4CED1,3C322E",116,62,192,84,
            #                     lang='eng',oem=1,
            #                     attribute=["tessedit_char_whitelist", 
            #                     "0123456789,"],THRESH_GAUSSIAN=False)
            pos = self.z_Ocrtext(da.pos_feature,"CFE3E9,311D17",119,62,192,84,M=0.26)
            if len(pos):
                #pos = pos[0]["text"]
                if pos[0] == ",":
                    pos = pos[1:]
                if pos[len(pos)-1]==",":
                    pos = pos[:len(pos)-1]
                    
                postr = pos.replace("\n","")
                postr = pos.replace(",,",",")
                
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
        
    #前往长寿郊外    
    def go_to_CSJW(self):
        #确保道具栏没有被收起来
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
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
        self.click(125,45)
        time.sleep(1)        
#        if self.rgb_array(da.map_feature["长寿村"])==State.OK:
        self.tap_("长寿村",144,6)   
        time.sleep(0.5)
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            if status==status.NOTMATCH:
                time.sleep(0.5)        
            else:
                self.mask_(True)
                self.click(1052,648)
                time.sleep(0.5)
                self.mask_(False)
                break
        while True:
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "长寿郊外" in reponse:
                print("抵达长寿郊外")
                break
    
    #前往朱紫国         
    def go_to_ZZG(self):
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.feixingfu_jiemian)
            if status==status.OK:
                time.sleep(0.7)
                self.click(573,483)
                time.sleep(0.7)
            if status==status.NOTMATCH:
                break
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往朱紫国")
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(2)
            elif status==status.OK:
                while True:
                    reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
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
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
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
        self.click(125,45)
        time.sleep(1)        
        #if self.rgb_array(da.map_feature["朱紫国"])==State.OK:
        
        self.tap_("朱紫国",6,4)   
        time.sleep(0.5)
        
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            if status==status.NOTMATCH:
                time.sleep(0.5)        
            else:
                self.click(42,656)   
                time.sleep(0.5)
                break             
        while True:
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "大唐境外" in reponse:
                print("抵达大唐境外")
                break
            else:
                time.sleep(0.5)
    #前往墨家村
    def TotheMJC(self):
        self.TotheDTJW()
        self.click(125,45)
        time.sleep(1)
        # while True:
        #     if self.rgb_array(da.map_feature["大唐境外A"])==State.OK:
        #         print("OK")
        #         break
        #     else:        
        #         time.sleep(0.5)
        self.tap_("大唐境外",233,109)
        
        
        self.mask_(True)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.map_feature["火焰山土地"]["坐标"])
            if status == status.NOTMATCH:
                time.sleep(0.5)
            else:
                self.click(785,174)
                time.sleep(0.5)
                break
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.map_feature["送我进墨家村"]["坐标"])
            if status == status.NOTMATCH:
                time.sleep(0.5)
            else:
                self.click(1045,246)
                time.sleep(0.5)
                break
        self.mask_(False)
            
        while True:
            ##self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "墨家村" in reponse:
                print("抵达目的地")
                return
    #前往大唐国境        
    def ToDTGJ(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
        time.sleep(0.2)        
        self.flag_transfer("red")
        time.sleep(0.5)
        q = False
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.flag_jiemian)
            if status==status.NOTMATCH:
                if q:
                    self.click(1070,54)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
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
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "大唐国境" in reponse:
                print("抵达目的地")
                return
            
    #前往麒麟山
    def TotheQLS(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
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
        self.click(125,45)
        time.sleep(1)        

        self.tap_("朱紫国",3,111)   
        time.sleep(0.5)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            if status==status.NOTMATCH:
                time.sleep(0.5)
            else:
                break
        self.mask_(True)
        self.click(14,98)
        time.sleep(0.5)
        self.mask_(False)
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "麒麟山" in reponse:
                print("抵达目的地")
                return
                        
                        
                        
    #前往狮驼岭
    def TotheSTL(self):
        self.TotheDTJW()
        self.click(125,45)
        time.sleep(1)
        self.tap_("大唐境外",7,49)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            if status==status.NOTMATCH:
                time.sleep(0.5)
            else:
                break
        self.click(18,348)
        time.sleep(0.5)
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "狮驼岭" in reponse:
                print("抵达目的地")
                return
            
                    
    #前往东海湾        
    def ToTheDHW(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
        time.sleep(0.2)        
        self.flag_transfer("yellow")
        time.sleep(0.5)
        q = False
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.flag_jiemian)
            if status==status.NOTMATCH:
                if q:
                    self.click(1070,54)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                    if status==status.NOTMATCH:
                        time.sleep(0.5)
                    else:
                        break
            else:
                q = True
                self.click(815,558)
                time.sleep(0.2)
                
        # time.sleep(1)
        # self.click(949,609)
        # time.sleep(1)
        
        
        self.mask_(True)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.map_feature["驿站老板"]["坐标"])
            if status == status.NOTMATCH:
                time.sleep(0.5)
            else:
                self.click(640,405)
                time.sleep(0.5)
                break
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.map_feature["我要去"]["坐标"])
            if status == status.NOTMATCH:
                time.sleep(0.5)
            else:
                self.click(1062,340)
                time.sleep(0.5)
                break
        self.mask_(False) 
                 
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "东海湾" in reponse:
                print("抵达目的地")
                return
    
    #前往江南野外        
    def ToTheJNYW(self):
        while True:
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
        time.sleep(0.2)        
        self.flag_transfer("red")
        time.sleep(0.5)
        q = False
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.flag_jiemian)
            if status==status.NOTMATCH:
                if q:
                    self.click(1070,54)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                    if status==status.NOTMATCH:
                        time.sleep(0.5)        
                    else:
                        break
            else:
                q = True
                self.click(1069,604)
                time.sleep(0.2)
                
        self.mask_(True)
        self.click(1190,697)
        time.sleep(0.5)
        self.mask_(False)
        while True:
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "江南野外" in reponse:
                print("抵达目的地")
                break            
        while True:
            if self.no_prop():
                self.click(1220, 679)
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
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
        time.sleep(0.2)        
        self.flag_transfer("yellow")
        time.sleep(0.5)
        q = False
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.flag_jiemian)
            if status==status.NOTMATCH:
                if q:
                    self.click(1070,54)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
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
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "花果山" in reponse:
                print("抵达目的地")
                return
    #前往傲来国        
    def ToTheALG(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
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
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.feixingfu_jiemian)
            if status==status.OK:
                time.sleep(0.7)
                self.click(1525,788)
                time.sleep(0.7)
                break
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往傲来国")
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(1)
            elif status==status.OK:
                while True:
                    reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
                    if  "傲来国" in reponse:
                        print("抵达傲来国")
                        break
                break
        return True
    
    #前往五庄观
    def ToTheWZG(self):
        self.ToDTGJ()
        #打开地图
        time.sleep(1)
        self.click(125,45)
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
        
        self.click(125,45)
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
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "五庄观" in reponse:
                print("抵达五庄观")
                break
                
    def open_prop(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
        
        
    #前往普陀山
    def ToThePTS(self):
        self.ToDTGJ()
        time.sleep(1)
        self.click(125,45)
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
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "普陀山" in reponse:
                print("抵达普陀山")
                break
            
    def Orb(self):
        #当前场景
        scenario = ""
        tulist = self.check_map()
        mapInfomation = {"tu":tulist}
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            if status==status.NOTMATCH:
                break
            else:
                self.click(1609,85)
                time.sleep(1)
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
                    if not place in scenario:
                        self.go_to_CSJW()
                    scenario = "长寿郊外"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)
                    self.tap_("长寿郊外",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break
                elif place in "大唐国境":
                    if not place in scenario:
                        self.ToDTGJ()
                    scenario = "大唐国境"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("大唐国境",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break
                elif place in "大唐境外":
                    if not place in scenario:
                        self.TotheDTJW()
                    scenario = "大唐境外"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("大唐境外",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break
                elif place in "麒麟山":
                    if not place in scenario:
                        self.TotheQLS()
                    scenario = "麒麟山"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("麒麟山",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break
                elif place in "狮驼岭":
                    if not place in scenario:
                        self.TotheSTL()
                    scenario = "狮驼岭"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("狮驼岭",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break    
                elif place in "朱紫国":
                    if not place in scenario:
                        while True:
                            #self.queue.put("check")
                            if self.no_prop():
                                self.click(1220, 679)
                                time.sleep(0.5)
                                if not self.no_prop():
                                    break
                            else:
                                break
                            time.sleep(2)
                        self.click(1121, 673)
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
                        self.go_to_ZZG()
                    scenario = "朱紫国"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("朱紫国",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break
                elif place in "花果山":
                    if not place in scenario:
                        self.ToTheHGS()
                    scenario = "花果山"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("花果山",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break
                elif place in "东海湾":
                    if not place in scenario:
                        self.ToTheDHW()
                    scenario = "东海湾"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("东海湾",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break
                elif place in "江南野外":
                    if not place in scenario:
                        self.ToTheJNYW()
                    scenario = "江南野外"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("江南野外",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break     
                elif place in "傲来国":
                    if not place in scenario:
                        self.ToTheALG()
                    scenario = "傲来国"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("傲来国",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break
                elif place in "北俱芦洲":
                    if not place in scenario:
                        self.TotheBJLZ()
                    scenario = "北俱芦洲"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("北俱芦洲",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break
                elif place in "普陀山":
                    if not place in scenario:
                        self.ToThePTS()
                    scenario = "普陀山"
                    time.sleep(1)
                    self.click(125,45)
                    time.sleep(1)   
                    self.tap_("普陀山",place_x,place_y)
                    self.open_prop()
                    #判断提示框是否出现
                    while True:
                        status,ag= self.findMultiColorInRegionFuzzyByTable(da.prompt_box)
                        if status==status.NOTMATCH:
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                            self.click(backpack_x,backpack_y)
                        else:
                            self.click(1609,85)
                            time.sleep(0.2)                            
                            status,ag= self.findMultiColorInRegionFuzzyByTable(da.failjiemian)
                            if status==status.NOTMATCH:
                                pass
                            else:
                                time.sleep(1)
                                self.click(1600,80)
                                time.sleep(1)
                                self.queue.put("check")
                                self.queue.join()
                            break                                
                else:
                    print("所在地址没找到")
                    os._exit(0)
    #前往西凉女国
    def ToTheXLNG(self):
        #确保道具栏没有被收起来
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
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
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.feixingfu_jiemian)
            if status==status.OK:
                time.sleep(0.7)
                self.click(755,446)
                time.sleep(0.7)
                break
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往西梁女国")
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(0.5)
            elif status==status.OK:
                print("抵达西梁女国")
                break
        return True
    
    #前往北俱芦洲
    def TotheBJLZ(self):
        self.ToTheHGS()
        self.click(804,333)
        time.sleep(1)
        self.click(125,45)
        time.sleep(1)
        while True:
            if self.rgb_array(da.map_feature["花果山"])==State.OK:
                print("OK")
                break
            else:        
                time.sleep(0.5)        
        self.tap_("花果山",32,94)
        self.mask_(True)
        while True:
            if self.rgb_array(da.map_feature["花果山土地"])==State.OK:
                print("OK")
                break
            else:        
                time.sleep(0.5) 
        self.click(834,271)
        while True:
            if self.rgb_array(da.map_feature["是的"])==State.OK:
                print("OK")
                break
            else:        
                time.sleep(0.5)   
        self.click(1550,552)
        time.sleep(0.5) 
        self.mask_(False)
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "北俱芦洲" in reponse:
                print("抵达目的地")
                break
    
    #前往女儿村
    def TotheNEC(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
        time.sleep(0.2)        
        self.flag_transfer("yellow")
        time.sleep(0.5)
        q = False
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.flag_jiemian)
            if status==status.NOTMATCH:
                if q:
                    self.click(1070,54)
                    time.sleep(0.5)
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                    if status==status.NOTMATCH:
                        time.sleep(0.5)        
                    else:
                        break
            else:
                q = True
                self.click(476,258)
                time.sleep(0.2)
        time.sleep(1)
        self.mask_(True)
        self.click(115,225)
        time.sleep(0.1)  
        self.mask_(False)     
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "女儿村" in reponse:
                print("抵达目的地")
                break
        
            
     
    #前往建邺城
    def TotheJYC(self):
        while True:
            #self.queue.put("check")
            if self.no_prop():
                self.click(1220, 679)
                time.sleep(0.5)
                if not self.no_prop():
                    break
            else:
                break
            time.sleep(2)
        self.click(1121, 673)
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
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.feixingfu_jiemian)
            if status==status.OK:
                time.sleep(0.7)
                self.click(1223,659)
                time.sleep(0.7)
                break
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往建邺国")
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(2)
            elif status==status.OK:
                while True:
                    reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
                    if  "建邺城" in reponse:
                        print("抵达建邺城")
                        break
                break
        return True
        
    
    def get_maps(self):
        self.ToTheXLNG()
        time.sleep(0.5)
        self.mask_(True)
        time.sleep(1)
        while True:
            if self.rgb_array(da.cangku["西凉_仓库管理员"])==State.OK:
                self.click(959,288)
                break
            else:
                time.sleep(0.5)
        
        time.sleep(1)
        while True:
            if self.rgb_array(da.cangku["仓库操作"])==State.OK:
                self.click(1604,643)
                break
            else:
                time.sleep(0.5) 
        while True:
            if self.rgb_array(da.cangku["仓库界面"])==State.OK:
                break
        n,nn,nnn,nnnn=None,None,None,None
        time.sleep(1)
        tpl = self.Print_screen()
        target = cv2.imread("./images/tu.png")
        map_number = 0
        for i in range(0,13):
            tpl = self.Print_screen()
            #self.show(tpl[314:831,205:881])
            x,y = self.matchTemplate(tpl[314:831,205:881],target,0.15)
            if x != -1:
                print("找到宝图")
                time.sleep(0.5)
                self.click(205+x,314+y)
                self.click(205+x,314+y)
                self.click(205+x,314+y)
                time.sleep(0.5)
                map_number +=1
            else:
                break
        self.click(1601,76) #界面返回  
        time.sleep(0.5)
        self.mask_(False)
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            time.sleep(0.5)
            if status==status.OK:
                break       
        time.sleep(0.5)
        return  map_number
    
    def mask_(self,ON=True):
        if ON:
            while True:
                if self.rgb_array(da.mask["是否屏蔽"])==State.OK:
                    break
                else:
                    self.click(45,252) 
                    time.sleep(0.6)

            while True:
                if self.rgb_array(da.mask["已经屏蔽玩家"])==State.OK:
                    break
                else:
                    self.click(47,362)
                    time.sleep(0.6)
               
            while True:
                if self.rgb_array(da.mask["已经隐藏摊位"])==State.OK:
                    break
                else:
                    self.click(49,468)
                    time.sleep(0.6)
         
            while True:
                if self.rgb_array(da.mask["已经隐藏界面"])==State.OK:
                    break
                else:
                    self.click(47,562)
                    time.sleep(0.6)
        else:
            while True:
                if self.rgb_array(da.mask["是否屏蔽"])==State.OK:
                    self.click(42,656)
                    time.sleep(0.6) 
                else:
                    time.sleep(0.7)
                    break
                
    def estimate_map(self,name):             
        if name == "建邺城":
            return da.map_name.JYC
        elif name == "朱紫国":
            return da.map_name.ZZG    
        elif name == "女儿村":   
            return da.map_name.NEC 
        elif name == "东海湾":
            return da.map_name.DHW 
        elif name == "长寿郊外":
            return da.map_name.CSJW 
        elif name == "大唐国境":
            return da.map_name.DTGJ 
        elif name == "江南野外":
            return da.map_name.JNYW
        elif name == "五庄观":
            return da.map_name.WZG
        elif name == "北俱芦洲":
            return da.map_name.BJLZ
        elif name == "普陀山":
            return da.map_name.PTS
        elif name == "麒麟山":    
            return da.map_name.QLS
        elif name == "狮驼岭":
            return da.map_name.STL
        elif name == "大唐境外":
            return da.map_name.DTJW
        elif name == "墨家村":
            return da.map_name.MJC
        elif name == "花果山":
            return da.map_name.HGS
        
    #排序仓库顺序存图，取图
    def get_set_map(self,G):
        if G:
            print("取图")
            
        else:
            print("存图") 
            tpl = self.Print_screen()
            target = cv2.imread("./images/tu.png")
            start_pos = (948,312,1060,427)
            convert_pos = [948,312,1060,427]
            tu_list = list()
            for i in range(0,5):
                time.sleep(0.5)
                convert_pos[0] = start_pos[0] + i*97
                convert_pos[2] = start_pos[2] + i*97
                for j in range(0,4):
                    time.sleep(0.5)
                    print(j)
                    convert_pos[1] = start_pos[1] + j*97
                    convert_pos[3] = start_pos[3] + j*97
                    self.click(convert_pos[0]+5,convert_pos[1]+5)
                    time.sleep(0.5)
                    tpl = self.Print_screen()
                    #self.show(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]])
                    x,y = self.matchTemplate(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]],target,0.15)
                    if x != -1:
                        print("找到宝图")
                        while True:
                            if self.rgb_array(da.ditu_show["仓库道具栏显示地图字体"]) == State.OK:
                                break
                            else:
                                time.sleep(1)
                        #这里判断下提示框
                        tpl = self.Print_screen()
                        #检测字体
                        name = self.x_Ocrtext(da.ditu,"00E804,011805#03DC07,032006#08DD0B,072009",546,549,692,591)
                        if name == "":
                            print("无法识别字体")
                            continue
                        print(name)
                        map_da = self.estimate_map(name) 
                        c__x,c__y = da.CK[map_da]
                        #检测是否开启仓库选择栏
                        while True:
                            if self.rgb_array(da.cangku["仓库选择界面"])==State.OK:
                                break
                            else:
                                self.click(421,928)
                                time.sleep(0.7)
                        while True:
                            if self.rgb_array(da.cangku["仓库选择界面"])==State.OK:
                                self.click(c__x,c__y)
                                time.sleep(0.6) 
                            else:
                                time.sleep(0.7)
                                break
                            
                        while True:
                            tpl = self.Print_screen()  
                            x,y = self.matchTemplate(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]],target,0.15)
                            if x != -1:
                                self.click(convert_pos[0]+5,convert_pos[1]+5)
                                self.click(convert_pos[0]+5,convert_pos[1]+5)
                            else:
                                break
                        print("已经存取好地图到仓库中")
                    
zoom_count = 1.0

    
def test_TotheJYC():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)    
    Robot.TotheJYC()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()
    
def test_ToNEC():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)    
    Robot.TotheNEC()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()
                  
def test_check_pet_HP():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)    
    Robot.check_thePetHealth()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()
    
def test_get_set_map():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    
    m1.start()
    Robot = action(q,zoom_count=zoom_count)    
    Robot.get_set_map(False)
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()  
    

def test_check_map():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)    
    Robot.check_map()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit() 
    
def test_go_to_CSC():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)   
    #确保道具栏没有被收起来
    while True:
        #self.queue.put("check")
        if Robot.no_prop():
            Robot.click(1220, 679)
            time.sleep(0.5)
            if not Robot.no_prop():
                break
        else:
            break
        time.sleep(2)
    Robot.click(1121, 673)
    time.sleep(1)
    status,x,y= Robot.discover_feixingfu()
    if status == status.OK:
        print(x,y)
    Robot.click(x,y)
    time.sleep(1)
    tpl = Robot.Print_screen()
    target = cv2.imread("./images/shiyong.png")
    x,y = Robot.matchTemplate(tpl,target)
    if x != -1:
        Robot.click(x,y)
    else:
        print("飞行符没有使用")
        return
    time.sleep(1)    
     
    Robot.go_to_CSC()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit() 

def test_go_to_CSJW():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)    
    Robot.go_to_CSJW() 
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit() 
    
        
def test_x_ocrtext():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)    
    while True:
        reponse = Robot.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
        if  "长寿郊外" in reponse:
            print("抵达长寿郊外")
            break
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()       

    
    
#           
def test_tap():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)   
    time.sleep(1)
    Robot.click(125,45)
    time.sleep(1)        
    Robot.tap_("朱紫国",89,94)
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()  
    
def test_DTJW():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)   
    Robot.TotheDTJW()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()
def test_display():
    s = "010000000000000110000000000000110000000000000110000000000000110000111111111110011111000000111110000000000111100000000000011000000000000"
    display(s,9,15,"")        
         
         
def test_NPC_HYS():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)   

    Robot.mask_(True)
    while True:
        status,ag= Robot.findMultiColorInRegionFuzzyByTable(da.map_feature["火焰山土地"]["坐标"])
        if status == status.NOTMATCH:
            time.sleep(0.5)
        else:
            Robot.click(785,174)
            time.sleep(0.5)
            break
    while True:
        #self.queue.put("check")
        status,ag= Robot.findMultiColorInRegionFuzzyByTable(da.map_feature["送我进墨家村"]["坐标"])
        if status == status.NOTMATCH:
            time.sleep(0.5)
        else:
            Robot.click(1045,246)
            time.sleep(0.5)
            break
    Robot.mask_(False)         
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit() 
    
#测试东海湾驿站老板           
def test_NPC_YZLB():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)   

    Robot.mask_(True)
    while True:
        status,ag= Robot.findMultiColorInRegionFuzzyByTable(da.map_feature["驿站老板"]["坐标"])
        if status == status.NOTMATCH:
            time.sleep(0.5)
        else:
            Robot.click(640,405)
            time.sleep(0.5)
            break
    while True:
        #self.queue.put("check")
        status,ag= Robot.findMultiColorInRegionFuzzyByTable(da.map_feature["我要去"]["坐标"])
        if status == status.NOTMATCH:
            time.sleep(0.5)
        else:
            Robot.click(1062,340)
            time.sleep(0.5)
            break
    Robot.mask_(False)         
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit() 
    
#测试东海湾  
def test_ToTheDHW():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)       
    Robot.ToTheDHW()   
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()
    


#测试江南野外
def test_ToTheJNYW():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)           
    Robot.ToTheJNYW()        
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()
    
#测试麒麟山
def test_TotheQLS():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)          
    Robot.TotheQLS()    
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit() 
    
#测试狮驼岭       
def test_TotheSTL():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)          
    Robot.TotheSTL()    
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()     
    
def main():
    test_TotheSTL()
    
    
    
if __name__ == "__main__":
    main()