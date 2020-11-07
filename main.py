# -*- coding: utf-8 -*-
from os import error
import Robot as rb
import Robot
import time
import pytesseract as pytes
import cv2

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


class action(rb.Robot):
    
    def __init__(self,class_name="subWin",title_name="sub",zoom_count=1.5):
        rb.Robot.__init__(self,class_name=class_name,title_name=title_name,zoom_count=zoom_count)
        self.Get_GameHwnd()
        self.cx = None
        self.error = list()
        
    def find_map_by_shop(self):
        #tpl = self.Print_screen()
        start_pos = [285,196,532,244] #第一个摊位
        conversion = [285,196,532,244]
        tu_shop = list()
        jump = False
        for i in range(0,4):
            conversion[1] = start_pos[1] + i*144
            conversion[3] = start_pos[3] + i*144
            for j in range(0,3):
                conversion[0] = start_pos[0] + j*341
                conversion[2] = start_pos[2] + j*341
                print("conversion{0}".format(conversion))
                ret = self.tsOcrText(tu_text_features,conversion[0],conversion[1],conversion[2],conversion[3],config=('--oem 1 -l chi_sim --psm 7')) 
                if len(ret):
                    print("OK")
                
            
    def run_with_callback(self,fun,fun_param,pre_fun1,fun1_param,post_fun2,fun2_param):
        try:
            print("start pre_fun1")
            ret = pre_fun1(fun_param)
            ret = fun(ret,fun1_param)
            ret = post_fun2(ret,fun2_param)
            self.cx = ret
        except Exception as identifier:
            self.error.append(identifier)
            

        
        

def main():


    #blRobot.Get_GameHwnd()
    start = time.time()
    Robot = action()
    Robot.find_map_by_shop()
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    
if __name__ == "__main__":
    main()
    
    
    