# -*- coding: utf-8 -*-
from os import error

from numba.cuda.decorators import convert_types
import Robot as rb
import time
import pytesseract as pytes
from utils import *

'''
    
    while True:
        x,y = blRobot.findMultiColorInRegionFuzzy("0x202020","2|2|0x202020", 90, 52, 1131, 1024 ,1406)
        if x!=-1:
            print("posx:{0},posy:{1}".format(x,y))
            blRobot.click(x+1,y+1)
        else:
            print("not found")
'''

tu_text_features = ['图','T']
shop_emty = (727,651,"0x3f4a53"),(663,644,"0x3f4a53"),(623,645,"0x3f4a53"),(720,616,"0x3f4a53"),(718,683,"0x3f4a53"),(797,679,"0x3f4a53"),(855,675,"0x3f4a53"),(852,637,"0x3f4a53")
tu_money = 27999

class action(rb.Robot):

    def __init__(self,class_name="subWin",title_name="sub",zoom_count=1.5):
        rb.Robot.__init__(self,class_name=class_name,title_name=title_name,zoom_count=zoom_count)
        self.Get_GameHwnd()
        self.cx = None
        self.error = list()
        
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
    #打开道具栏遍历宝图
    def check_map(self):
        n,nn,nnn,nnnn=None,None,None,None
        #打开道具栏
        self.click(1695,1015)
        time.sleep(1)
        tpl = self.Print_screen()
        target = cv2.imread("./images/tu.png")
        start_pos = (902,269,1013,378)
        convert_pos = [902,269,1013,378]
        tu_list = list()
        for i in range(0,5):
            time.sleep(0.5)
            print(i)
            convert_pos[0] = start_pos[0] + i*139
            convert_pos[2] = start_pos[2] + i*139
            tpl = self.Print_screen()
            self.click(convert_pos[0]+5,convert_pos[1]+5)
            # width = abs(convert_pos[2]-convert_pos[0])
            # height = abs(convert_pos[3]-convert_pos[1])
            #self.show(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]])
            x,y = self.matchTemplate(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]],target)
            if x != -1:
                print("找到宝图")
            for j in range(0,4):
                time.sleep(0.5)
                print(j)
                convert_pos[1] = start_pos[1] + j*134
                convert_pos[3] = start_pos[3] + j*134
                self.click(convert_pos[0]+5,convert_pos[1]+5)
                tpl = self.Print_screen()
                # _width = abs(convert_pos[2]-convert_pos[0])
                # _height = abs(convert_pos[3]-convert_pos[1])
                #self.show(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]])
                x,y = self.matchTemplate(tpl[convert_pos[1]:convert_pos[3],convert_pos[0]:convert_pos[2]],target)
                if x != -1:
                    print("找到宝图")

            
        
            
            
    
        

def main():
    #blRobot.Get_GameHwnd()
    start = time.time()
    Robot = action()
    Robot.check_map()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    
if __name__ == "__main__":
    main()