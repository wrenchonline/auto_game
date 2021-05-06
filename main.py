# -*- coding: utf-8 -*-

import Robot as rb
import time
from utils import *
import Robot_help as rh
import math
import queue
from goto import with_goto
import json
import os
import data as da
from func_timeout import func_set_timeout

zoom_count = 1.5


utils_list = [
    da.utils["飞行符"],
    da.utils["红旗"],
    da.utils["绿旗"],
    da.utils["黄旗"],
    da.utils["白旗"],
    da.utils["红罗羹"],
    da.utils["绿芦羹"],
    da.utils["摄妖香"]
    ] 




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
                status = self.Found_do(da.utils["红旗"]["基点"],da.utils["红旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="红旗")
                if status == status.OK:
                    break
                else:
                    goto .end
            elif color == "yellow":
                status = self.Found_do(da.utils["黄旗"]["基点"],da.utils["黄旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="黄旗")
                if status == status.OK:
                    break
                else:
                    goto .end
            elif color == "blue":
                status = self.Found_do(da.utils["蓝旗"]["基点"],da.utils["蓝旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="蓝旗")
                if status == status.OK:
                    break
                else:
                    goto .end
            elif color == "green":
                status = self.Found_do(da.utils["绿旗"]["基点"],da.utils["绿旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="绿旗")
                if status == status.OK:
                    break
                else:
                    goto .end
            elif color == "white":
                status = self.Found_do(da.utils["白旗"]["基点"],da.utils["白旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="白旗")
                if status == status.OK:
                    break
                else:
                    goto .end
            else:
                label .end
                #没找到，去行囊里面找
                self.click(833,140)
                time.sleep(0.5)
                while True:
                    if color == "red":
                        status = self.Found_do(da.utils["红旗"]["基点"],da.utils["红旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="红旗")
                        if status == status.OK:
                            break
                    elif color == "yellow":
                        status = self.Found_do(da.utils["黄旗"]["基点"],da.utils["黄旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="黄旗")
                        if status == status.OK:
                            break
                    elif color == "blue":
                        status = self.Found_do(da.utils["蓝旗"]["基点"],da.utils["蓝旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="蓝旗")
                        if status == status.OK:
                            break
                    elif color == "green":
                        status = self.Found_do(da.utils["绿旗"]["基点"],da.utils["绿旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="绿旗")
                        if status == status.OK:
                            break
                    elif color == "white":
                        status = self.Found_do(da.utils["白旗"]["基点"],da.utils["白旗"]["偏移"], 90,592,170, 1057,538,ischlik=2,name="白旗")
                        if status == status.OK:
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
            
    #测试保存物品
    def save_the_prize(self):
        # self.ToTheXLNG()
        # time.sleep(0.5)
        # self.mask_(True)
        # time.sleep(1)
        # while True:
        #     if self.rgb_array(da.cangku["西凉_仓库管理员"])==State.OK:
        #         self.click(642,110)
        #         break
        #     else:
        #         time.sleep(0.5)
        # time.sleep(1)
        # while True:
        #     if self.rgb_array(da.cangku["仓库操作"])==State.OK:
        #         self.click(1017,424)
        #         break
        #     else:
        #         time.sleep(0.5) 
        # while True:
        #     if self.rgb_array(da.cangku["仓库界面"])==State.OK:
        #         break
        # time.sleep(1)
        self.find_items()
            
            
    #
    def map_items(self,convert_pos:list,da_items:dict):
        time.sleep(0.1)
        #print("check items_name:{0}".format(da_items["物品名"]))
        _,x,y = self.findMultiColorInRegionFuzzy(da_items["基点"], da_items["偏移"], 75, convert_pos[0], convert_pos[1], convert_pos[2], convert_pos[3])
        if x != -1:
            print("found items_name:{0} x:{1} y:{2}".format(da_items["物品名"],x,y)) 
            return True
        else: return False
        
    '''
    发现道具栏物品，如果是非识别物品，先存入仓库中
    '''
    def find_items(self):
        start_pos = ( 625,213,708,279)
        convert_pos = [ 625,213,708,279]
        for i in range(0,5):
            time.sleep(0.5)
            convert_pos[0] = start_pos[0] + i*93
            convert_pos[2] = start_pos[2] + i*93
            for j in range(0,4):
                time.sleep(0.5)
                convert_pos[1] = start_pos[1] + j*90
                convert_pos[3] = start_pos[3] + j*90
                self.click(convert_pos[0]+5,convert_pos[1]+5)
                timc = [convert_pos[0],convert_pos[1],convert_pos[2],convert_pos[3]]
                # tpl = self.Print_screen()
                # self.show(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]])
                #发现的物品
                items_name_list = map(self.map_items,[timc for i in range (len(utils_list))],utils_list)
                tmp = [b for b in items_name_list]
                if True in tmp:
                    continue
                else:
                    #print("double click on the items bar i:{0} j:{1}".format(i,j)) 
                    self.click(convert_pos[0]+5,convert_pos[1]+5)
                    self.click(convert_pos[0]+5,convert_pos[1]+5)
                    status = self.Found_do(da.utils["道具栏空白"]["基点"],da.utils["道具栏空白"]["偏移"], 
                                           90,convert_pos[0], convert_pos[1], convert_pos[2], convert_pos[3],
                                           ischlik=2,timeout=1.5,
                                           name="道具栏空白")
                    if status == status.OK: continue
                    else:
                        print("the blank items is not Found")
                        self.click(366,621)
                        time.sleep(1.5)
                        self.click(convert_pos[0]+5,convert_pos[1]+5)
                        self.click(convert_pos[0]+5,convert_pos[1]+5)
    
    '''
    在各主城增加了仓库管理员NPC，坐标分别为：长安城（346，244）、长安城（224，141）、建邺城（54，32)、傲来国（143，101）、长寿村（111，62）、朱紫国（126，90）
    '''
    #check_map 打开道具栏遍历宝图
    def check_map(self):
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
        # tpl = self.Print_screen()
        # target = cv2.imread("./images/tu.png")
        start_pos = (600,175,683,257)
        convert_pos = [600,175,683,257]
        tu_list = list()
        for i in range(0,5):
            time.sleep(0.5)
            convert_pos[0] = start_pos[0] + i*90
            convert_pos[2] = start_pos[2] + i*90
            for j in range(0,4):
                time.sleep(0.5)
                print(j)
                convert_pos[1] = start_pos[1] + j*90
                convert_pos[3] = start_pos[3] + j*90
                self.click(convert_pos[0]+5,convert_pos[1]+5)
                time.sleep(0.5)
                tpl = self.Print_screen()
                _,x,y = self.findMultiColorInRegionFuzzy( da.daoju["普通宝图A"]["基点"], da.daoju["普通宝图A"]["偏移"], 75, convert_pos[0], convert_pos[1], convert_pos[2], convert_pos[3])
                #self.show(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]])
                # x,y = self.matchTemplate(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]],target,0.13)
                if x != -1:
                    print("找到宝图")
                    while True:
                       if self.rgb_array(da.ditu_show["道具栏显示地图字体"]) == State.OK:
                           break
                       else:
                           time.sleep(1)
                    #检测字体
                    data = self.x_Ocrtext(da.ditu,"00E804,011805#03DC07,032006#08DD0B,072009",297,338,394,366,similarity=0.4)
                    print(data)                    
                    if data:
                        if len(data)>3:
                                pos = self.z_Ocrtext(da.map_font,"06BE0B,06420B#03E105,031E05#00E804,011805#03DC07,032006#08DD0B,072009"
                                                ,401,343,485,364,M=0.2)
                                print("postr:",pos)
                                if len(pos):
                                    if pos[0] == "?":
                                        pos = pos[1:]
                                    if pos[len(pos)-1]=="?":
                                        pos = pos[:len(pos)-1]
                                    postr = pos.replace("\n","")
                                    postr = pos.replace("??","?")
                                    try:
                                        _x = int(postr.split('?')[0])
                                        _y = int(postr.split('?')[1])
                                        tu_list.append((data,_x,_y,convert_pos[0]+5,convert_pos[1]+5,convert_pos[2],convert_pos[3]))
                                    except Exception as e:
                                        print("字库解析异常")
                        else:
                                pos = self.z_Ocrtext(da.map_font,"06BE0B,06420B#03E105,031E05#00E804,011805#03DC07,032006#08DD0B,072009"
                                                ,370,339,485,364,M=0.2)
                                print("postr:",pos)
                                if len(pos):
                                    if pos[0] == "?":
                                        pos = pos[1:]
                                    if pos[len(pos)-1]=="?":
                                        pos = pos[:len(pos)-1]
                                    postr = pos.replace("\n","")
                                    postr = pos.replace("??","?")
                                    try:
                                        _x = int(postr.split('?')[0])
                                        _y = int(postr.split('?')[1])
                                        tu_list.append((data,_x,_y,convert_pos[0]+5,convert_pos[1]+5,convert_pos[2],convert_pos[3]))
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
            pos = self.z_Ocrtext(da.pos_feature,"CFE3E9,311D17#F8DDCE,072331",100,60,206,85,M=0.26)
            if len(pos):
                #pos = pos[0]["text"]
                if pos[0] == "?":
                    pos = pos[1:]
                if pos[len(pos)-1]=="?":
                    pos = pos[:len(pos)-1]

                postr = pos.replace("\n","")
                postr = pos.replace("??","?")
                
                try:
                    _x = int(postr.split('?')[0])
                    _y = int(postr.split('?')[1])
                    time.sleep(1)
                    print("当前坐标(x:{0},y:{1})----实际坐标(x:{2},y:{3})".format(str(_x),str(_y),str(X),str(Y)))
                    if (abs(X-_x)<=3) and (abs(Y-_y)<=3):
                        break
                except Exception as e:
                    print(postr)
                    
                    
    def discover_feixingfu(self):
        status = State.NOTMATCH
        status = self.Found_do(da.utils["飞行符"]["基点"],da.utils["飞行符"]["偏移"], 80,592,170, 1057,538,name="道具栏飞行符")
        return status
    
    def no_prop(self):
        status,x,y = self.findMultiColorInRegionFuzzy( da.prompt_box["道具栏展开"]["基点"], da.prompt_box["道具栏展开"]["偏移"], 80,1186,648, 1248,706)
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
        time.sleep(1)
        self.click(1121, 673)
        time.sleep(1)
        status = self.discover_feixingfu()
        if status == status.OK:
            print("发现飞行符")
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
            self.open_map()
            time.sleep(1)        
            self.tap_("长寿村",144,6)   
            time.sleep(0.5)
            while True:
                #self.queue.put("check")
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                if status==status.NOTMATCH:
                    time.sleep(0.5)        
                else:
                    break
            while True:
                reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
                if  "长寿郊外" in reponse:
                    print("抵达长寿郊外")
                    break
                else:
                    self.mask_(True)
                    self.click(1038,600)
                    time.sleep(0.5)
                    self.mask_(False)
            return True
        else:
            return False    
                    
    #前往朱紫国         
    def go_to_ZZG(self):
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.feixingfu_jiemian,degree=80)
            if status==status.OK:
                time.sleep(0.7)
                self.click(573,483)
                time.sleep(0.7)
            if status==status.NOTMATCH:
                break
        while True:
            #self.queue.put("check")
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian,degree=80)
            time.sleep(0.5)
            if status==status.NOTMATCH:
                print("前往朱紫国")
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.fanhui)
                if status==status.OK:
                    self.click(ag[0],ag[1])
                time.sleep(2)
            elif status==status.OK:
                while True:
                    reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,24,208,51,similarity=0.3)
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
        status = self.discover_feixingfu()
        if status == status.OK:
            print("发现飞行符")
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
            self.open_map()
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
        self.open_map()
        time.sleep(1)
        # while True:
        #     if self.rgb_array(da.map_feature["大唐境外A"])==State.OK:
        #         print("OK")
        #         break
        #     else:        
        #         time.sleep(0.5)
        self.tap_("大唐境外",233,109)
        
        
        self.mask_(True)
        time.sleep(0.5)
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
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.map_feature["送我进墨家村"]["坐标"],degree=80)
            if status == status.NOTMATCH:
                time.sleep(0.5)
            else:
                self.click(1045,246)
                time.sleep(0.5)
                break
        time.sleep(0.5)
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
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian,degree=80)
                    if status==status.NOTMATCH:
                        time.sleep(0.5)        
                    else:
                        break
            else:
                q = True
                self.click(185,602)
                time.sleep(0.2)

        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "大唐国境" in reponse:
                print("抵达目的地")
                return
            else:
                time.sleep(0.5)
                self.click(12,704)
                time.sleep(0.5)

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
        status = self.discover_feixingfu()
        if status == status.OK:
            print("发现飞行符")
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
            self.open_map()
            time.sleep(1)        

            self.tap_("朱紫国",3,111)   
            time.sleep(0.5)
            while True:
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                if status==status.NOTMATCH:
                    time.sleep(0.5)
                else:
                    break

        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "麒麟山" in reponse:
                print("抵达目的地")
                return
            else:
                self.mask_(True)
                self.click(14,98)
                time.sleep(0.5)
                self.mask_(False)

    #前往狮驼岭
    def TotheSTL(self):
        self.TotheDTJW()
        self.open_map()
        time.sleep(1)
        self.tap_("大唐境外",7,49)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
            if status==status.NOTMATCH:
                time.sleep(0.5)
            else:
                break

        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "狮驼岭" in reponse:
                print("抵达目的地")
                return
            else:
                self.click(18,348)
                time.sleep(0.5)                

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
        while True:
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "江南野外" in reponse:
                print("抵达目的地")
                break
            else:
                self.mask_(True)
                self.click(1190,697)
                time.sleep(0.5)
                self.mask_(False)
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
                self.click(962,163)
                time.sleep(0.2)
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "花果山" in reponse:
                print("抵达目的地")
                return
            else:
                self.mask_(True)
                time.sleep(1)
                self.click(1241,80)
                time.sleep(1) 
                self.mask_(False)  
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
        status = self.discover_feixingfu()
        if status == status.OK:
            print("发现飞行符")
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
                    self.click(1010,521)
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
        self.open_map()
        time.sleep(1)
        self.tap_("大唐国境",5,79)
        time.sleep(0.5)
        self.mask_(True)
        self.click(16,195)
        time.sleep(0.5)
        self.mask_(False)
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "大唐境外" in reponse:
                print("抵达大唐境外")
                break
            else:
                time.sleep(1)
        time.sleep(1)
        self.open_map()
        time.sleep(1)                
        self.tap_("大唐境外",633,76)
        while True:
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "五庄观" in reponse:
                print("抵达五庄观")
                break
            else:
                self.mask_(True)
                self.click(1245,200)
                time.sleep(0.2)
                self.mask_(False) 
                
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
        time.sleep(0.5)
        self.click(1121, 673)
        while True:
            status,x,y=self.findMultiColorInRegionFuzzy(da.prompt_box["打开地图界面"]["基点"],da.prompt_box["打开地图界面"]["偏移"], 88,  622,3, 1207,  307)
            if status == State.NOTMATCH:
                print("当前没有打开道具栏")
                time.sleep(0.5)
                self.click(1121, 673)
            else:
                print("已经打开道具栏")
                break
        
    #前往普陀山
    def ToThePTS(self):
        self.ToDTGJ()
        time.sleep(1)
        self.open_map()      
        time.sleep(1)
        self.tap_("大唐国境",228,58)
        time.sleep(0.5)        
        self.mask_(True)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.map_feature["传送仙女"]["坐标"])
            if status == status.NOTMATCH:
                time.sleep(0.5)
            else:
                self.click(508,  254)
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
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "普陀山" in reponse:
                print("抵达普陀山")
                break
    
    def config_load(self):
        load_dict = None
        time.sleep(1)
        with open("./角色信息.json", 'r',encoding="utf-8") as f:
            load_dict  = json.load(f)
        return load_dict

    def config_save(self,maps):
        load_dict = dict()
        #maps.remove(m)
        load_dict["tu"]=maps
        with open("./角色信息.json", 'w',encoding="utf-8") as f:
            json.dump(load_dict,f,ensure_ascii=False,indent = 4)


    def orb_(self,place,place_x,place_y,x1,y1,x2,y2):
        time.sleep(1)
        self.open_map()
        time.sleep(1)
        self.tap_(place,place_x,place_y)
        self.open_prop()
        time.sleep(1)
        #判断提示框是否出现
        while True:
            # tpl = self.Print_screen()
            # tpl = tpl[y1-5:y2,x1-5:x2]
            # self.show(tpl)
            status,x,y = self.findMultiColorInRegionFuzzy( da.daoju["普通宝图A"]["基点"], da.daoju["普通宝图A"]["偏移"], 70,x1-5,y1-5,x2,y2)
            #status,x,y = self.findMultiColorInRegionFuzzy( da.prompt_box["提示框"]["基点"], da.prompt_box["提示框"]["偏移"], 80, 231,4, 287,62)
            if status==status.OK:
                self.click(x1+5,y1+5)
                self.click(x1+5,y1+5)
                self.click(x1+5,y1+5)
            else:
                while True:
                    status,x,y=self.findMultiColorInRegionFuzzy(da.prompt_box["打开地图界面"]["基点"],da.prompt_box["打开地图界面"]["偏移"], 80,  1029,   22, 1098,94)
                    if status == State.OK:
                        self.click(1072,54) #界面返回 
                        time.sleep(0.5)
                        break
                while True:
                    time.sleep(1)
                #没回到主界面直接代表进入战斗界面
                    status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian,degree=80)
                    if status==status.NOTMATCH:
                        self.queue.put("check")
                        self.queue.join()
                        time.sleep(2)
                        break
                    else:
                        break
                time.sleep(0.5)
                return
        
        
    def Orb(self,b_only_load_config=False):
        #当前场景
        scenario = ""
        if not b_only_load_config:
            tulist = self.check_map()
            while True:
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                if status==status.NOTMATCH:
                    break
                else:
                    self.click(1072,54) #界面返回 
                    time.sleep(1)
            self.config_save(tulist)
  
        #加载配置文件
        load_dict = self.config_load()
        maps =  load_dict["tu"]
        if isinstance(maps,list):
            while len(maps):
                m = maps.pop(0)
                place = m[0]
                place_x = m[1]
                place_y = m[2]
                backpack_x1 = m[3]
                backpack_y1 = m[4]
                backpack_x2 = m[5]
                backpack_y2 = m[6]
                if place in "长寿郊外":
                    if not place in scenario:
                        b = self.go_to_CSJW()
                        if not b:
                            print("没有发现飞行符，无法前往长寿郊外")
                            return 
                    scenario = "长寿郊外"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "大唐国境":
                    if not place in scenario:
                        self.ToDTGJ()
                    scenario = "大唐国境"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "大唐境外":
                    if not place in scenario:
                        self.TotheDTJW()
                    scenario = "大唐境外"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "麒麟山":
                    if not place in scenario:
                        self.TotheQLS()
                    scenario = "麒麟山"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "狮驼岭":
                    if not place in scenario:
                        self.TotheSTL()
                    scenario = "狮驼岭"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)    
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
                        status = self.discover_feixingfu()
                        if status == status.OK:
                            print("发现飞行符")
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
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "花果山":
                    if not place in scenario:
                        self.ToTheHGS()
                    scenario = "花果山"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "东海湾":
                    if not place in scenario:
                        self.ToTheDHW()
                    scenario = "东海湾"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "江南野外":
                    if not place in scenario:
                        self.ToTheJNYW()
                    scenario = "江南野外"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "傲来国":
                    if not place in scenario:
                        self.ToTheALG()
                    scenario = "傲来国"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "北俱芦洲":
                    if not place in scenario:
                        self.TotheBJLZ()
                    scenario = "北俱芦洲"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "普陀山":
                    if not place in scenario:
                        self.ToThePTS()
                    scenario = "普陀山"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "五庄观":
                    if not place in scenario:
                        self.ToTheWZG()
                    scenario = "五庄观"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)
                elif place in "女儿村":
                    if not place in scenario:
                        self.TotheNEC()
                    scenario = "女儿村"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)   
                elif place in "墨家村":
                    if not place in scenario:
                        self.TotheMJC()
                    scenario = "墨家村"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps) 
                elif place in "建邺城":
                    if not place in scenario:
                        self.TotheJYC()
                    scenario = "建邺城"
                    self.orb_(scenario,place_x,place_y,backpack_x1,backpack_y1,backpack_x2,backpack_y2)
                    self.config_save(maps)                     
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
        status = self.discover_feixingfu()
        if status == status.OK:
            print("发现飞行符")
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
                    self.click(500,291)
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
        #self.click(804,333)
        self.open_map()
        time.sleep(1)
        self.tap_("花果山",32,94)
        self.mask_(True)
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.map_feature["花果山土地"]["坐标"])
            if status == status.NOTMATCH:
                time.sleep(0.5)
            else:
                self.click(552,193)
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
        
        time.sleep(0.5)
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
                self.click(320,172)
                time.sleep(0.2)
        time.sleep(1)
        while True:
            #self.queue.put("check")
            reponse = self.x_Ocrtext(da.scenario,"1C1D21,1B1C20",94,  24,208,   51)
            if  "女儿村" in reponse:
                print("抵达目的地")
                break
            else:
                self.mask_(True)
                self.click(115,225)
                time.sleep(0.2)  
                self.mask_(False)  
                    
     
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
        status = self.discover_feixingfu()
        if status == status.OK:
            print("发现飞行符")
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
                    self.click(812,440)
                    time.sleep(0.7)
                    break
            while True:
                #self.queue.put("check")
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                time.sleep(0.5)
                if status==status.NOTMATCH:
                    print("前往建邺城")
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

    
    #获取宝图
    def get_maps(self):
        self.ToTheXLNG()
        time.sleep(0.5)
        self.mask_(True)
        time.sleep(1)
        while True:
            if self.rgb_array(da.cangku["西凉_仓库管理员"])==State.OK:
                self.click(642,110)
                break
            else:
                time.sleep(0.5)
        time.sleep(1)
        while True:
            if self.rgb_array(da.cangku["仓库操作"])==State.OK:
                self.click(1017,424)
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
            x,y = self.matchTemplate(tpl[205:559,140:587],target,0.15)
            if x != -1:
                print("找到宝图")
                time.sleep(0.5)
                self.click(140+x,205+y)
                self.click(140+x,205+y)
                self.click(140+x,205+y)
                time.sleep(0.5)
                map_number +=1
            else:
                break
        self.click(1072,54) #界面返回  
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
                    print("没有屏蔽，点击")
                    self.click(37,250)
                    time.sleep(1)
                    break
                else:
                    time.sleep(2) 
                    break
            while True:
                if self.rgb_array(da.mask["是否屏蔽"])==State.OK:
                    print("已经屏蔽界面")
                    break
                else:
                    print("没有屏蔽界面")
                    self.click(45,252) 
                    time.sleep(2)
            while True:
                if self.rgb_array(da.mask["已经屏蔽玩家"])==State.OK:
                    print("已经屏蔽玩家")
                    break
                else:
                    print("没有屏蔽玩家，点击")
                    self.click(47,362)
                    time.sleep(2)
               
            while True:
                if self.rgb_array(da.mask["已经隐藏摊位"])==State.OK:
                    print("已经隐藏摊位")
                    break
                else:
                    print("没有隐藏摊位，点击")
                    self.click(49,468)
                    time.sleep(2) 
        else:
            time.sleep(2)
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
        elif name == "傲来国":
            return da.map_name.ALG

    def open_map(self):
        self.click(125,45)
        time.sleep(0.5)
        while True:
            status,x,y=self.findMultiColorInRegionFuzzy(da.prompt_box["打开地图界面"]["基点"],da.prompt_box["打开地图界面"]["偏移"], 80,  622,3, 1207,307)
            if status == State.NOTMATCH:
                print("NOTMATCH")
                time.sleep(0.5)
                self.click(125,45)
            else:
                print("openning the map")
                self.click(125,45)
                break

    def VerifyRange(self,x,y,x1,y1,x2,y2,x_range,y_range):
        start_pos = (x1,y1,x2,y2)
        convert_pos = [x1,y1,x2,y2]
        tu_list = list()
        for i in range(0,5):
            convert_pos[0] = start_pos[0] + i*x_range
            convert_pos[2] = start_pos[2] + i*x_range
            for j in range(0,4):
                convert_pos[1] = start_pos[1] + j*y_range
                convert_pos[3] = start_pos[3] + j*y_range
                if convert_pos[0] < x < convert_pos[2] and convert_pos[1] < y < convert_pos[3]:
                    return convert_pos[0],convert_pos[1],convert_pos[2],convert_pos[3]
        return -1,-1,-1,-1
    
    
    #排序仓库顺序存图，取图
    def get_set_map(self,GetOrSet='get',togo=False):
        if togo:
            self.ToTheXLNG()
            time.sleep(0.5)
            self.mask_(True)
            time.sleep(1)
            while True:
                if self.rgb_array(da.cangku["西凉_仓库管理员"])==State.OK:
                    self.click(642,110)
                    break
                else:
                    time.sleep(0.5)
            time.sleep(1)
            while True:
                if self.rgb_array(da.cangku["仓库操作"])==State.OK:
                    self.click(1017,424)
                    break
                else:
                    time.sleep(0.5) 
            while True:
                if self.rgb_array(da.cangku["仓库界面"])==State.OK:
                    break
        if GetOrSet=='get':
            n,nn,nnn,nnnn=None,None,None,None
            time.sleep(1)
            map_number = 0
            while True:
                time.sleep(1)
                _,x,y = self.findMultiColorInRegionFuzzy( da.daoju["普通宝图A"]["基点"], da.daoju["普通宝图A"]["偏移"],60,x1=140,y1=205,x2=587,y2=559)
                time.sleep(1)
                if x !=-1:
                    time.sleep(0.5)
                    self.click(140+x,205+y)
                    self.click(140+x,205+y)
                    self.click(140+x,205+y)
                    time.sleep(0.5)
                    map_number+=1
                    print("仓库里找到宝图,map_number=",map_number)
                    if map_number == 12:  #默认取12张宝图挖宝
                        break
                else:
                    time.sleep(0.5)
                    self.click(360,624)
                    time.sleep(1)
            self.click(1072,54) #界面返回  
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
        else:
            print("存图") 
            #tpl = self.Print_screen()
            #target = cv2.imread("./images/tu.png")
            # start_pos = (627,207,709,287)
            # convert_pos = [627,207,709,287]
            #self.show(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]])
            while True:
                _,x,y = self.findMultiColorInRegionFuzzy( da.daoju["普通宝图A"]["基点"], da.daoju["普通宝图A"]["偏移"],60, 628,201,1073,558)
                if x ==-1:
                    break
                x = 628 + x
                y = 201 + y
                while True:
                    if self.rgb_array(da.ditu_show["仓库道具栏显示地图字体"]) == State.OK:
                        break
                    else:
                        time.sleep(1)
                        self.click(x+5,y+5)
                #这里判断下提示框
                tpl = self.Print_screen()
                #检测字体
                name = self.x_Ocrtext(da.ditu,"00E804,011805#03DC07,032006#08DD0B,072009",355,367,461,395)
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
                        self.click(263,  623)
                        time.sleep(0.7)
                while True:
                    if self.rgb_array(da.cangku["仓库选择界面"])==State.OK:
                        self.click(c__x,c__y)
                        time.sleep(0.6) 
                    else:
                        time.sleep(0.7)
                        break

                c1,c2,c3,c4 = self.VerifyRange(x,y,627,207,709,287,90,90)
                while True:
                    time.sleep(1)
                    tpl = self.Print_screen()                          
                    if c1:
                        _,x,y = self.findMultiColorInRegionFuzzy( da.daoju["普通宝图A"]["基点"], da.daoju["普通宝图A"]["偏移"],60, c1,c2,c3,c4)
                    #x,y = self.matchTemplate(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]],target,0.1)
                        if x != -1:
                            self.click(c1+5,c2+5)
                            self.click(c1+5,c2+5)
                        else:
                            break
                print("已经存取好地图到仓库中")
                
            while True:
                #self.queue.put("check")
                status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                time.sleep(0.5)
                if status==status.OK:
                    break
                else:
                    self.click(1072,54) #界面返回 
    
    #出售垃圾装备
    def Sell_Garbage_Equipment(self):
        pass


                




#测试前往建邺城    
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

#测试前往女儿村    
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

#测试存图    
def test_get_set_map(getorset='get'):
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)    
    Robot.get_set_map(getorset)
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
    status = Robot.discover_feixingfu()
    if status == status.OK:
        print("发现飞行符")
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
    
#测试长寿郊外
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

    
    
#测试地图           
def test_tap():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)   
    time.sleep(1)
    Robot.click(125,45)
    time.sleep(1)        
    Robot.tap_("大唐境外",633,76)
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

#测试大唐境外    
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
         
#测试墨家村NPC火焰山土地         
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


#测试北俱芦洲 花果山土地
def test_NPC_HGSTD():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)   
    Robot.mask_(True)
    while True:
        status,ag= Robot.findMultiColorInRegionFuzzyByTable(da.map_feature["花果山土地"]["坐标"])
        if status == status.NOTMATCH:
            time.sleep(0.5)
        else:
            Robot.click(552,193)
            time.sleep(0.5)
            break
    while True:
        #self.queue.put("check")
        status,ag= Robot.findMultiColorInRegionFuzzyByTable(da.map_feature["是的"]["坐标"])
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

#测试大唐国境 传送仙女         
def test_NPC_CSXN():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)   
    Robot.mask_(True)
    while True:
        status,ag= Robot.findMultiColorInRegionFuzzyByTable(da.map_feature["传送仙女"]["坐标"])
        if status == status.NOTMATCH:
            time.sleep(0.5)
        else:
            Robot.click(508,  254)
            #Robot.click(552,193)
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
    
#测试前往北俱芦洲(顺便测试前往花果山)
def test_TotheBJLZ():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)      
    Robot.TotheBJLZ()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

#测试前往大唐国境
def test_ToDTGJ():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)      
    Robot.ToDTGJ()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

#测试前往普陀山
def test_ToThePTS():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)        
    Robot.ToThePTS()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

#测试前往五庄观
def test_ToTheWZG():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)        
    Robot.ToTheWZG()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()
    
#测试前往建邺城
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

#测试前往西凉女国    
def test_ToTheXLNG():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    Robot.ToTheXLNG()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

def test_orb(b_only_load_config=False):
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    while True:
        value = input("是否加载配置文件并忽略道具栏读取图信息(Y/N):")
        if 'Y' == value.upper():
            b_only_load_config = True
            break
        elif 'N' == value.upper():
            b_only_load_config = False
            break
        else:
            continue
    Robot.Orb(b_only_load_config)
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

def test_box():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)        
    status,x,y= Robot.findMultiColorInRegionFuzzy(da.prompt_box["挖图失败"]["基点"],da.prompt_box["挖图失败"]["偏移"], 80, 283,18,781,51)
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

#测试打开地图
def test_openmap():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    Robot.click(125,45)
    time.sleep(0.5)
    while True:
        status,x,y=Robot.findMultiColorInRegionFuzzy(da.prompt_box["打开地图界面"]["基点"],da.prompt_box["打开地图界面"]["偏移"], 80,  622,3, 1207,  307)
        if status == State.NOTMATCH:
            print("NOTMATCH")
            time.sleep(0.5)
            Robot.click(125,45)
        else:
            print("openning the map")
            break
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit() 

#测试配置文件
def test_config():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    load_dict = Robot.config_load()
    maps =  load_dict["tu"]
    if isinstance(maps,list):
        while len(maps):
            m = maps.pop(0)
            Robot.config_save(maps)
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

#测试战斗系统
def test_fire():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    Robot.queue.put("check")
    Robot.queue.join()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

#测试打开道具栏
def test_openprop():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    Robot.open_prop()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()

#测试安全提示框
def test_safe_prompt():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    while True:
        pass
    
    
#测试探探
def test_tantan():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    while True:
        time.sleep(5)
        Robot.click(552,1240)
#抢红包
#@func_set_timeout(60*3) 
@with_goto
def Get_Gift1(Robot):
    first = False 
    bJoin = False
    bfGITFT = False
    label .start
    while True:
        if first:
            pass
        else:
            Robot.click(636,157)
            time.sleep(1)
            print("mouse chlik!")
            first = False
            Robot.move_click(636, 1179,636, 139,Stride_y=20) 
        for i in range(0,8):
            time.sleep(2)
            Robot.click(618,139+i*120)
            while True:
                status,x,y=Robot.findMultiColorInRegionFuzzy(da.tantan["红包"]["基点"],da.tantan["红包"]["偏移"], 80, 9,  167,211,246)
                if status == State.NOTMATCH:
                    break
                else:
                    print("Found a gift,Chlik it!")
                    Robot.click(9+x,167+y)
                    Robot.click(9+x,167+y)
                    Robot.click(9+x,167+y)
                    bfGITFT = True
                    break
            time.sleep(2) 
            while True:
                status,x,y=Robot.findMultiColorInRegionFuzzy(da.tantan["一键参与"]["基点"],da.tantan["一键参与"]["偏移"], 80,32, 1188,693, 1248)
                if status == State.NOTMATCH:
                    if bfGITFT:
                        continue
                    else: 
                        break
                else:
                    print("Join it!")
                    Robot.click(32+x,1188+y) 
                    time.sleep(1) 
                    Robot.click(345,653)
                    time.sleep(1) 
                    Robot.click(647,164)
                    time.sleep(1)
                    bJoin = True
                    bfGITFT = False
                    break
            time.sleep(2)
            if bJoin:
                print("bJoin and continue")
                while True:
                    status,x,y=Robot.findMultiColorInRegionFuzzy(da.tantan["我的关注"]["基点"],da.tantan["我的关注"]["偏移"], 80, 580,  141,714,  182)
                    if status == State.NOTMATCH:
                        print("wait for the my aatention end")
                        time.sleep(1.5)
                        break
                    else:
                        Robot.click(636,157)
                        Robot.click(636,157)
                        time.sleep(1.5)
                continue
        while True:
            status,x,y=Robot.findMultiColorInRegionFuzzy(da.tantan["我的关注"]["基点"],da.tantan["我的关注"]["偏移"], 80, 580,  141,714,  182)
            if status == State.NOTMATCH:
                if bJoin:
                    bJoin = False
                    print("Doesn't match my attention")
                    time.sleep(2)
                else:
                    break
            else:
                Robot.click(636,157)
                time.sleep(3)
                goto .start
                
def Get_Gift():
    # start = time.time()
    q = queue.Queue()
    # m1 = rh.MyThread(q,zoom_count=zoom_count)
    # m1.start()
    Robot = action(q,zoom_count=zoom_count)
    while True:
        status,x,y=Robot.findMultiColorInRegionFuzzy(da.tantan["直播动态界面"]["基点"],da.tantan["直播动态界面"]["偏移"], 90,16,56,87,99)
        if status == State.NOTMATCH:
            time.sleep(1)
            while True:
                status,x,y=Robot.findMultiColorInRegionFuzzy(da.tantan["我的关注"]["基点"],da.tantan["我的关注"]["偏移"], 75,577,139,690,181) 
                if status == State.NOTMATCH:
                    time.sleep(1)
                    break
                else:
                    print("Into my attention")
                    Robot.click(629,161)
                    time.sleep(1)
                    Get_Gift1(Robot)
        else:
            print("Enter the dynamic interface")
            Robot.click(358,199)
            time.sleep(1)

#test_save_the_prize 测试存物品            
def test_save_the_prize():
    start = time.time()
    q = queue.Queue()
    m1 = rh.MyThread(q,zoom_count=zoom_count)
    m1.start()
    Robot = action(q,zoom_count=zoom_count)
    Robot.save_the_prize()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    Robot.quit()    
        
def main():
    #test_ToTheDHW()
    #test_orb(b_only_load_config=False)
    test_save_the_prize()
if __name__ == "__main__":
    main()