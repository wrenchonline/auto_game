# -*- coding: utf-8 -*-
#模板匹配
from re import split
import cv2
import numpy as np
import numpy 
import win32gui 
import win32api
import win32ui
import win32con
import win32con as wcon
import pynput
import time
import ctypes
from ctypes import *
from PIL import ImageGrab,Image
import pytesseract as pytes
from utils import * 
import re 
import random
import string
import traceback
#jit是进行numpy运算
from numba import jit
import tesserocr
from tesserocr import PyTessBaseAPI, PSM, OEM,RIL,iterate_level
from PIL import Image
import data as da

def binstr_to_nparray(hex_2_str,abs_x,abs_y):
    binary = np.zeros((abs_y,abs_x), dtype=np.uint8)
    i = 0
    for j in range(abs_x):
        for k in range(abs_y):
            if hex_2_str[i] == "0":
                binary[k][j]=0
            else:
                binary[k][j]=255
            i+=1
    return binary

def get_window_rect(hwnd):
    try:
        f = ctypes.windll.dwmapi.DwmGetWindowAttribute
    except WindowsError:
        f = None
    if f:
        rect = ctypes.wintypes.RECT()
        DWMWA_EXTENDED_FRAME_BOUNDS = 9
        f(ctypes.wintypes.HWND(hwnd),
          ctypes.wintypes.DWORD(DWMWA_EXTENDED_FRAME_BOUNDS),
          ctypes.byref(rect),
          ctypes.sizeof(rect)
          )
        return rect.left, rect.top, rect.right, rect.bottom

class Robot:
    def __init__(self,class_name,title_name,zoom_count):
        self.class_name = class_name
        self.title_name = title_name
        #窗口坐标
        self.left = 0
        self.top = 0 
        self.right = 0
        self.bottom = 0
        self.hwnd = None
        self.ScreenBoardhwnd = None
        self.game_width = 0
        self.game_height = 0
        self.zoom_count = zoom_count
        self.rollback_list = list() #回滚机制，在于颜色匹配没找到或者卡屏的情况,根据此列表操作步骤重新回滚。
        
    @staticmethod
    @jit
    def __findMultiColor(s_c,expectedRGBColor,tolerance,x1=None,y1=None,x2=None,y2=None):
        pos_x_y = []
        for y in range(y1,y2):
            for x in range(x1,x2):
                b,g,r = s_c[y,x]
                exR, exG, exB = expectedRGBColor[:3]
                if (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance):
                    pos_x_y.append((x,y))
        return pos_x_y
    



    #像素转换成二值化点阵，返回二进制字符串
    @staticmethod
    @jit
    def rgb_to_hexstr_2(image_arrays,binary,MeanRgb,x1,y1,x2,y2):
        for idx ,x in enumerate (range(x1,x2)):
            for idy, y in enumerate (range(y1,y2)):
                b,g,r = image_arrays[y,x]
                # print("r:",r)
                # print("g:",g)
                # print("b:",b)
                for m in MeanRgb:
                    __mean_s_r = m[0]
                    __mean_s_g = m[1]
                    __mean_s_b = m[2]
                    __mean_m_r = m[3]
                    __mean_m_g = m[4]
                    __mean_m_b = m[5]
                    if  r <= (__mean_s_r+__mean_m_r) and  r >= (__mean_s_r-__mean_m_r)  and  g <= (__mean_s_g+__mean_m_g) and g >= (__mean_s_g-__mean_m_g)   and  b <= (__mean_s_b+__mean_m_b) and b >= (__mean_s_b-__mean_m_b):
                        binary[idy,idx] = 255
                        break
                    else:
                        binary[idy,idx] = 0

        return binary


    def Get_GameHwnd(self,Simulator_Name="雷电"):
        if Simulator_Name == "夜神":
            self.hwnd= win32gui.FindWindow('Qt5QWindowIcon','夜神模拟器')
            self.ScreenBoardhwnd = win32gui.FindWindowEx(self.hwnd, 0, 'Qt5QWindowIcon', 'ScreenBoardClassWindow')
        elif Simulator_Name == "雷电":
            self.hwnd= win32gui.FindWindow('LDPlayerMainFrame','雷電模擬器')
            self.ScreenBoardhwnd = win32gui.FindWindowEx(self.hwnd, 0, 'RenderWindow', 'TheRender')            
        self.hwnd = win32gui.FindWindowEx(self.ScreenBoardhwnd, 0, self.class_name, self.title_name)
        print('hwnd=',self.hwnd)
        text = win32gui.GetWindowText(self.hwnd)
        if self.hwnd:
            print("found game hwnd")
            self.left,self.top,self.right,self.bottom = win32gui.GetWindowRect(self.hwnd)
            #窗口坐标
            self.left=int(self.left*self.zoom_count)
            self.top=int(self.top*self.zoom_count )
            self.right=int(self.right*self.zoom_count )
            self.bottom=int(self.bottom*self.zoom_count ) 
            print("The window coordinates: ({0},{1},{2},{3})".format(str(self.left),str(self.top),str(self.right),str(self.bottom)))
            self.game_width = self.right - self.left
            self.game_height = self.bottom - self.top
            # self.game_width = 1920
            # self.game_height = 1080
            
        else:
            print("Not found game hwnd")
    """
    x,y = findMultiColorInRegionFuzzy( "0xed1d60", "14|-7|0xb1cdf0,21|4|0xe2df73", 90, 0, 0, 1279, 719)
    """
    def findMultiColorInRegionFuzzy(self,color,
                                    posandcolor,degree,
                                    x1=None,y1=None,x2=None,y2=None,
                                    tab=None,blist=False):
        x = None
        y = None
        tolerance = 100 - degree
        # width = abs(x2-x1)
        # height = abs(y2-y1)
        r,g,b  = Hex_to_RGB(color)
        tpl = self.Print_screen()
        #self.show(tpl)
        posandcolor_list = list()
        positems = list()
        posandcolors_param = posandcolor.split(",")
        state = State.OK
        pos_x_y_list = self.__findMultiColor(tpl,(r,g,b),tolerance,x1,y1,x2,y2)   
        if pos_x_y_list:
            for p in posandcolors_param:
                __c = p.split("|")
                px = __c[0]
                py = __c[1]
                rgb_hex = __c[2]
                _tmp = {"px":int(px),"py":int(py),"rgb_hex":rgb_hex}
                posandcolor_list.append(_tmp)
            for x,y in pos_x_y_list:
                for p in posandcolor_list:
                    # __px = int(p["px"])
                    # __py = int(p["py"])
                    newY = y+p["px"]
                    newX = x+p["py"]
                    if newY >= self.game_height:
                        continue
                        # print("findMultiColorInRegionFuzzy::检测y越界,返回失败")
                        # return State.NOTMATCH,-1,-1
                    if newX >= self.game_width:
                        continue
                        # print("findMultiColorInRegionFuzzy::检查x越界,返回失败")
                        # return State.NOTMATCH,-1,-1
                    __rgb_hex = p["rgb_hex"]
                    b,g,r = tpl[newY,newX]
                    exR = int(__rgb_hex[2:4],16) 
                    exG = int(__rgb_hex[4:6],16) 
                    exB = int(__rgb_hex[6:8],16) 
                    if (pixelMatchesColor((r, g, b),(exR,exG,exB),tolerance)):
                        state = State.OK
                    else:
                        state = State.NOTMATCH
                        continue
                if state == State.OK:
                   positems.append((x-x1,y-y1))
            if len(positems):
                if not blist:
                    return State.OK,positems[0][0],positems[0][1]
                else:
                    return State.OK,positems
        if not blist:
            return State.NOTMATCH,-1,-1
        else:
            return State.NOTMATCH,positems
    
    def findMultiColorInRegionFuzzyByTable(self,t_Set,degree=90,x1=None,y1=None,x2=None,y2=None):
        tolerance = 100 - degree
        tpl = None
        #目前用不上x1,y1,x2,y2
        #tpl = self.Print_screen()[y1:y2,x1:x2]
        # if x1 and y1 and x2 and y2:
        #     tpl = self.Print_screen()[y1:y2,x1:x2]
        # else:
        tpl = self.Print_screen()
        state = State.NOTMATCH
        for x,y,rgb_16_hex in t_Set:
            #str_rgb = str(rgb_16_hex)
            if isinstance(rgb_16_hex,int):
                rgb_16_hex = '0x{:06X}'.format(rgb_16_hex)
            exR = int(rgb_16_hex[2:4],16)
            exG = int(rgb_16_hex[4:6],16)
            exB = int(rgb_16_hex[6:8],16)
            if y1 and x1:
                if y > y2:
                    continue
                if x > x2:
                    continue

            b,g,r = tpl[y,x]
            if (pixelMatchesColor((r, g, b),(exR,exG,exB),tolerance)):
                state = State.OK
            else:
                state = State.NOTMATCH
                break
        if state == State.OK:
            return State.OK,t_Set[0]
        else:
            return State.NOTMATCH,t_Set[0]
        
    def FC_Clicke(t_Set,x1,y1,x2,y2,R,bool,sim):
        pass

            
    def Print_screen(self):
        
        #返回句柄窗口的设备环境，覆盖整个窗口，包括非客户区，标题栏，菜单，边框
        hWndDC = win32gui.GetWindowDC(self.hwnd)
        #创建设备描述表
        mfcDC = win32ui.CreateDCFromHandle(hWndDC)
        #创建内存设备描述表
        saveDC = mfcDC.CreateCompatibleDC()
        #创建位图对象准备保存图片
        saveBitMap = win32ui.CreateBitmap()
        #为bitmap开辟存储空间
        saveBitMap.CreateCompatibleBitmap(mfcDC,self.game_width,self.game_height)
        #将截图保存到saveBitMap中
        saveDC.SelectObject(saveBitMap)
        #保存bitmap到内存设备描述表
        saveDC.BitBlt((0,0), (self.game_width,self.game_height), mfcDC, (0, 0), win32con.SRCCOPY)
 
        signedIntsArray = saveBitMap.GetBitmapBits(True)
        
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hWndDC)
        
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        
        im_PIL = Image.frombuffer(
            'RGB',
            (self.game_width, self.game_height),
            signedIntsArray, 'raw', 'BGRX', 0, 1)
        # im_PIL.save("C:\\Users\\Wrench\\Desktop\\tmp\\im_opencv_" + salt + ".png")
        # im = Image.open("C:\\Users\\Wrench\\Desktop\\tmp\\im_opencv_" + salt + ".png")
        return cv2.cvtColor(np.array(im_PIL),cv2.COLOR_RGB2BGR)
    
    def doClick(self,cx,cy):
        ctr = pynput.mouse.Controller()
        ctr.move(cx, cy)   #鼠标移动到(x,y)位置
        ctr.press(pynput.mouse.Button.left)  #移动并且在(x,y)位置左击
        ctr.release(pynput.mouse.Button.left) 
    def getCurPos(self):
        return win32gui.GetCursorPos()
    
    def getPos(self):
        while True:
            res = getCurPos()
            print (res)
            time.sleep(1)
            
    def clickLeft(self):
        win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN | win32con.MOUSEEVENTF_LEFTUP, 0, 0)

    def movePos(self,x, y):
        windll.user32.SetCursorPos(x, y)

    def animateMove(self,curPos, targetPos, durTime=1, fps=60):
        x1 = curPos[0]
        y1 = curPos[1]
        x2 = targetPos[0]
        y2 = targetPos[1]
        dx = x2 - x1
        dy = y2 - y1
        times = int(fps * durTime)
        dx_ = dx * 1.0 / times
        dy_ = dy * 1.0 / times
        sleep_time = durTime * 1.0 / times
        for i in range(times):
            int_temp_x = int(round(x1 + (i + 1) * dx_))
            int_temp_y = int(round(y1 + (i + 1) * dy_))
            windll.user32.SetCursorPos(int_temp_x, int_temp_y)
            time.sleep(sleep_time)
        windll.user32.SetCursorPos(x2, y2)
        
    
    def show(self,tpl):
        cv2.namedWindow("Image")
        cv2.imshow("Image", tpl)
        cv2.waitKey (0)

    def animateMoveAndClick(self,curPos, targetPos, durTime=0.5, fps=30, waitTime=0.5):
        x1 = curPos[0]
        y1 = curPos[1]
        x2 = targetPos[0]
        y2 = targetPos[1]
        dx = x2 - x1
        dy = y2 - y1
        times = int(fps * durTime)
        dx_ = dx * 1.0 / times
        dy_ = dy * 1.0 / times
        sleep_time = durTime * 1.0 / times

        for i in range(times):
            int_temp_x = int(round(x1 + (i + 1) * dx_))
            int_temp_y = int(round(y1 + (i + 1) * dy_))
            windll.user32.SetCursorPos(int_temp_x, int_temp_y)
            time.sleep(sleep_time)
        windll.user32.SetCursorPos(x2, y2)
        time.sleep(waitTime)
        self.clickLeft()

    def matchTemplate(self,tpl,target,tolerance=0.2,getone=True):
        methods = [cv2.TM_SQDIFF_NORMED]   #3种模板匹配方法 cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED
        th, tw = target.shape[:2]
        
        for md in methods:
            #result = cv2.matchTemplate(tpl,target, md)
            if getone:  
                try:
                    res =cv2.matchTemplate(tpl,target, md)
                    ok = True
                except cv2.error as e: 
                    ok = False
                    #print("匹配错误")
                    return (-1,-1)
                
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if min_val > tolerance:
                    #print("not match")
                    return (-1,-1)
                else:
                    pass
                    
                if md == cv2.TM_SQDIFF_NORMED:
                    tl = min_loc
                else:
                    tl = max_loc
                br = (tl[0]+tw, tl[1]+th)   #br是矩形右下角的点的坐标
                a=int((tl[0]+int(tw/2)))
                b=int((tl[1]+int(th/2)))
                return a,b
            else:
                res = cv2.matchTemplate(tpl,target,cv2.TM_SQDIFF_NORMED)
                right_bottom_list = list()
                loc = np.where(res <= tolerance)
                for pt in zip(*loc[::-1]):  # *号表示可选参数
                    right_bottom = (int((pt[0]+int(tw/2))), int((pt[1]+int(th/2))))
                    right_bottom_list.append(right_bottom)
                return right_bottom_list
                    #cv2.rectangle(img_rgb, pt, right_bottom, (0, 0, 255), 2)                
        return (-1,-1)
        
    def clike_map(self):
        tpl = self.Print_screen() 
        target = cv2.imread("./images/map.jpg")  
        new_target = self.matchTemplate(tpl,target)    
        self.click(new_target)  
        
        
    def tsOcrText(self,tpl,text_features,x1,y1,x2,y2,lang='chi_sim',psm=7, oem=1):
        _data_list = list()
        tpl = tpl[y1:y2,x1:x2]
        tpl = cv2.cvtColor(tpl,cv2.COLOR_RGB2GRAY)
        img = cv2.adaptiveThreshold(tpl,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2) #经过测试高斯识别效果好
        #numpy转换成PIL格式
        img = Image.fromarray(img)
        #img.show()
        with PyTessBaseAPI(lang='chi_sim',psm=7, oem=1) as api:
                level = RIL.TEXTLINE #以标题为主
                #img = Image.open("C:\\Users\\Wrench\\Nox_share\\ImageShare\\Screenshots\\12121.png")
                api.SetImage(img)
                api.Recognize()
                ri = api.GetIterator()
                for r in iterate_level(ri, level):
                    try: 
                        symbol = r.GetUTF8Text(level)  # r == ri
                        conf = r.Confidence(level) #相似度
                        if symbol:
                            pass
                            #print('symbol {0}  conf: {1}'.format(symbol, conf))
                        boxes = r.BoundingBox(level) #xy等等坐标
                        dict_= {"text":symbol,"left":boxes[0],"top":boxes[1],"weight":boxes[2],"weight":boxes[3]}
                        _data_list.append(dict_)
                    except Exception as e:
                        print("没有字符")
        xz = list()
        for idx, data in enumerate(_data_list):
            for text in  text_features:
                if text in data["text"]:
                    x =  data["left"] + x1
                    y =  data["top"] + y1
                    xz.append((data["text"],x,y))            
        #print("识别结果:{0}".format(xz))
        return xz
    
    # def OcrText(self,tpl,x1,y1,x2,y2,config=('--oem 1 -l chi_sim --psm 7')):
    #     econfig = ('--oem 1 -l eng --psm 6 digits')
    #     cconfig = ('--oem 1 -l chi_sim --psm 6')
    #     _data_list = list()
    #     tpl = tpl[y1:y2,x1:x2]
    #     tpl = cv2.cvtColor(tpl,cv2.COLOR_RGB2GRAY)
    #     img = cv2.adaptiveThreshold(tpl,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2) #经过测试高斯识别效果好
    #     #numpy转换成PIL格式
    #     img = Image.fromarray(img)
    #     #img.show()
    #     with PyTessBaseAPI(lang='chi_sim',psm=7, oem=1) as api:
    #             level = RIL.TEXTLINE #以标题为主
    #             #img = Image.open("C:\\Users\\Wrench\\Nox_share\\ImageShare\\Screenshots\\12121.png")
    #             api.SetImage(img)
    #             api.Recognize()
    #             ri = api.GetIterator()
    #             for r in iterate_level(ri, level):
    #                 try:
    #                     symbol = r.GetUTF8Text(level)  # r == ri
    #                     conf = r.Confidence(level) #相似度
    #                     if symbol:
    #                         pass
    #                         #print('symbol {0}  conf: {1}'.format(symbol, conf))
    #                     boxes = r.BoundingBox(level) #xy等等坐标
    #                     dict_= {"text":symbol,"left":boxes[0],"top":boxes[1],"weight":boxes[2],"weight":boxes[3]}
    #                     _data_list.append(dict_)
    #                 except Exception as e:
    #                     print("没有字符")
    #     return _data_list
    
 
        
    def clike_expr_tool(self):
        tpl = self.Print_screen() 
        target = cv2.imread("./images/expr_tool.jpg")
        x,y = self.matchTemplate(tpl,target)
        self.click(x,y)
        
    def clike_aperture(self):
        # LUA 脚本插件 {1338,949,0x121721} 1338,949 是 x,y这样.  0x121721 是rbg的十六进制码
        im2 = ImageGrab.grab(bbox =(0, 0, 300, 300)) 
        pix = im2.load()
        sc = pix[55,56]
        tpl = self.Print_screen()
        #x,y是这个3维图像的位置. 第一参数是y,第二个是x
        r, g, b = tpl[1079,1919]
        a = (r, g, b)
        print (a)
        
    def look_up_color_by_xy_c(self,x:int,y:int,rgb_hex):
        ret = None
        tpl = self.Print_screen()
        
        rgb_tuple = Hex_to_RGB(str(rgb_hex))

        b,g,r = tpl[y,x]
        hex_str = '%02x%02x%02x' % (r, g, b)
        print(hex_str)
        hex_a = int(hex_str,16)
        if pixelMatchesColor((r, g, b),(78,48,17),10):
            print ("Matches Color")
            ret = State.OK
        else:
            print ("Not Found! Rollback it")
            ret = State.ROLLBACK
        return ret

        
    
    def click(self,x:int=None,y:int=None,DOUBLE=False):
        """Click at pixel xy."""
        x = int(x/self.zoom_count)#1.5是缩放比例
        y = int(y/self.zoom_count)
        lParam = win32api.MAKELONG(x, y)
        win32gui.PostMessage(self.ScreenBoardhwnd, wcon.WM_MOUSEMOVE,wcon.MK_LBUTTON, lParam)
        win32gui.SendMessage(self.ScreenBoardhwnd,  wcon.WM_SETCURSOR, self.ScreenBoardhwnd, win32api.MAKELONG(wcon.HTCLIENT, wcon.WM_LBUTTONDOWN))
        # win32gui.PostMessage(self.ScreenBoardhwnd, wcon.WM_SETCURSOR, 0, 0)
        while (win32api.GetKeyState(wcon.VK_CONTROL) < 0 or
                win32api.GetKeyState(wcon.VK_SHIFT) < 0 or
                win32api.GetKeyState(wcon.VK_MENU) < 0):
                time.sleep(0.005)
        win32gui.PostMessage(self.ScreenBoardhwnd, wcon.WM_LBUTTONDOWN,
                                wcon.MK_LBUTTON, lParam)
        win32gui.PostMessage(self.ScreenBoardhwnd, wcon.WM_LBUTTONUP, 0, lParam)
        
    
    def move_click(self,x:int=None,y:int=None,x1:int=None,y1:int=None,Stride_x:int=1,Stride_y:int=1):
        x = int(x/self.zoom_count)#1.5是缩放比例
        y = int(y/self.zoom_count)
        x1 = int(x1/self.zoom_count)
        y1 = int(y1/self.zoom_count)
        x_down = False
        y_down = False
        lenth_x = None
        lenth_y = None
        lParam1 = win32api.MAKELONG(x, y)
        lParam2 = win32api.MAKELONG(x1, y1)
        win32gui.PostMessage(self.ScreenBoardhwnd, wcon.WM_MOUSEMOVE,wcon.MK_LBUTTON, lParam1)
        # win32gui.SendMessage(self.ScreenBoardhwnd,  wcon.WM_SETCURSOR, self.ScreenBoardhwnd, win32api.MAKELONG(wcon.HTCLIENT, wcon.WM_LBUTTONDOWN))
        while (win32api.GetKeyState(wcon.VK_CONTROL) < 0 or
                win32api.GetKeyState(wcon.VK_SHIFT) < 0 or
                win32api.GetKeyState(wcon.VK_MENU) < 0):
                time.sleep(0.005)
        win32gui.PostMessage(self.ScreenBoardhwnd, wcon.WM_LBUTTONDOWN,
                              wcon.MK_LBUTTON, lParam1)
        time.sleep(0.1)
        #如果小于，降序
        if x >= x1:
            x_down = True
        lenth_x = abs(x-x1)+1
        if y >= y1:
            y_down = True   
        lenth_y = abs(y-y1)+1            
        for lx in range(0,lenth_x,Stride_x):
            for ly in range(0,lenth_y,Stride_y):
                if x_down:
                    x2 =x - lx
                else:
                    x2 =x + lx
                if y_down:
                    y2 = y - ly
                else:
                    y2 = y + ly
                    
                print("x2:{0}y2:{1}".format(x2,y2))
                win32gui.PostMessage(self.ScreenBoardhwnd, wcon.WM_MOUSEMOVE,wcon.MK_LBUTTON, win32api.MAKELONG(x2,y2))
        time.sleep(0.1)
        win32gui.PostMessage(self.ScreenBoardhwnd, wcon.WM_LBUTTONUP,
                            wcon.MK_LBUTTON, lParam2) 
        
        
    def check_fire(self):
        tpl = self.Print_screen()
        target = cv2.imread("./images/check_fire.jpg")
        x,y = self.matchTemplate(tpl,target,0.09)
        if x == -1:
            return False
        else:
            return True

    #检测宝宝是否健康            
    def check_thePetHealth(self):
        while True:
            status,ag= self.findMultiColorInRegionFuzzyByTable(da.check_pet_HP)
            if status == State.NOTMATCH:
                self.click(1575,14)
                time.sleep(1)
                self.click(1224,156) 
            else:
                break

    def fire(self):
        while True:
            time.sleep(1)
            tpl = self.Print_screen()
            target = cv2.imread("./images/auto.jpg")
            target1 = cv2.imread("./images/autoing.png")
            x,y = self.matchTemplate(tpl,target,0.1)
            if x == -1:
                break
            else:
                print("点击自动战斗 posx:{0} posy:{1}".format(x,y))
                while True:
                    tpl = self.Print_screen()
                    _x,_y = self.matchTemplate(tpl,target1,0.1)
                    if _x == -1:
                        self.click(x,y)
                        time.sleep(1)
                    else:
                        self.click(1420,829)
                        time.sleep(3)
                        break
                break
                        
    def __Ocr(self,scx_rgb,x1,y1,x2,y2):
        tpl = self.Print_screen()        
        MeanRgb = list()
        if "#" in  scx_rgb:
            __scx_rgb =  scx_rgb.split("#")
            for i in __scx_rgb:
                se_rgb_tupe =  i.split(",")
                __mean_s_r = int(se_rgb_tupe[0][0:2],16)
                __mean_s_g = int(se_rgb_tupe[0][2:4],16)
                __mean_s_b = int(se_rgb_tupe[0][4:6],16)
                __mean_m_r = int(se_rgb_tupe[1][0:2],16)
                __mean_m_g = int(se_rgb_tupe[1][2:4],16)
                __mean_m_b = int(se_rgb_tupe[1][4:6],16)
                MeanRgb.append([__mean_s_r,__mean_s_g,__mean_s_b,__mean_m_r,__mean_m_g,__mean_m_b])
        else:
            se_rgb_tupe = scx_rgb.split(",")
            __mean_s_r = int(se_rgb_tupe[0][0:2],16)
            __mean_s_g = int(se_rgb_tupe[0][2:4],16)
            __mean_s_b = int(se_rgb_tupe[0][4:6],16)
            __mean_m_r = int(se_rgb_tupe[1][0:2],16)
            __mean_m_g = int(se_rgb_tupe[1][2:4],16)
            __mean_m_b = int(se_rgb_tupe[1][4:6],16)            
            MeanRgb.append([__mean_s_r,__mean_s_g,__mean_s_b,__mean_m_r,__mean_m_g,__mean_m_b])
            
        binary = np.zeros((abs(y2-y1),abs(x2-x1)), dtype=np.uint8)
        bin_2_ = self.rgb_to_hexstr_2(tpl,binary,np.array(MeanRgb),x1,y1,x2,y2)
        return bin_2_
    
    def Ocrtext(self,scx_rgb,x1,y1,x2,y2,Debug=False,ril=RIL.TEXTLINE,lang='chi_sim',psm=7, oem=1,attribute=None,THRESH_GAUSSIAN =False):
        
        if THRESH_GAUSSIAN:
            tpl = self.Print_screen()
            tpl = tpl[y1:y2,x1:x2]
            tpl = cv2.cvtColor(tpl,cv2.COLOR_RGB2GRAY)
            image_array1 = cv2.adaptiveThreshold(tpl,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
        else:
            image_array1 = self.__Ocr(scx_rgb,x1, y1, x2, y2)
        if Debug:
            self.show(image_array1)
        _data_list = list()
        with PyTessBaseAPI(lang=lang,psm=psm, oem=oem) as api:
                level = ril#以标题为主
                #img = Image.open("C:\\Users\\Wrench\\Nox_share\\ImageShare\\Screenshots\\12121.png")
                img = Image.fromarray(image_array1)
                if attribute:
                    api.SetVariable(attribute[0], attribute[1])
                #img.show()
                api.SetImage(img)
                api.Recognize()
                ri = api.GetIterator()
                for r in iterate_level(ri, level):
                    try:
                        symbol = r.GetUTF8Text(level)  # r == ri
                        r.Confidence(level) #相似度
                        if symbol:
                            pass
                            #print('symbol {0}  conf: {1}'.format(symbol, conf))
                        boxes = r.BoundingBox(level) #xy等等坐标
                        dict_= {"text":symbol,"left":boxes[0],"top":boxes[1],"boxes2":boxes[2],"boxes3":boxes[3]}
                        _data_list.append(dict_)
                    except Exception as e:
                        pass
                        print(traceback.print_exc())
                        print("没有字符")
        return _data_list
    
    def x_Ocrtext(self,tabs,scx_rgb,x1,y1,x2,y2,similarity=0.2):
        #ret = re.findall(r"@(.*?)\$",tab,re.I|re.M)
        for tab in tabs:
            if "@" in tab:
                data_tuple = tab.split("@")[1]
                hex_str_16 = tab.split("@")[0]
            else:
                data_tuple = tab
                hex_str_16 = tab.split("$")[0]
            data_tuple = data_tuple.split("$")
            if len(data_tuple):
                    p_hexstr_2 = data_tuple[0]
                    hexstr_2 = hexstr_16_to_hexstr_2(hex_str_16)
                    hexstr_2 += p_hexstr_2
                    word = data_tuple[1]
                    x =  int(data_tuple[4])
                    y = int(data_tuple[3])
                    image_array = binstr_to_nparray(hexstr_2,x,y)
                    #self.show(image_array)
                    image_array1 = self.__Ocr(scx_rgb,x1, y1, x2, y2)
                    #self.show(image_array1)
                    new_X_t = self.matchTemplate(image_array1,image_array,similarity)
                    #print(new_X_t)
                    if new_X_t !=(-1,-1):
                        print("当前识字为:{0}".format(word))
                        return word
        return ""

                    
                    
    def z_Ocrtext(self,tabs,scx_rgb,x1,y1,x2,y2,jiange=1,M=0.1):
        #ret = re.findall(r"@(.*?)\$",tab,re.I|re.M)
        textline = list()
        m_textline = list()
        z_textline = list()
        strs = ""
        image_array1 = self.__Ocr(scx_rgb,x1, y1, x2, y2)
        # 4、分割字符
        white = []  # 记录每一列的白色像素总和
        black = []  # ..........黑色.......
        height = image_array1.shape[0]
        width = image_array1.shape[1]
        white_max = 0
        black_max = 0
        # 计算每一列的黑白色像素总和
        for i in range(width):
            s = 0  # 这一列白色总数
            t = 0  # 这一列黑色总数
            for j in range(height):
                if image_array1[j][i] == 255:
                    s += 1
                if image_array1[j][i] == 0:
                    t += 1
            white_max = max(white_max, s)
            black_max = max(black_max, t)
            white.append(s)
            black.append(t)
            # print(s)
            # print(t)
        arg = False  # False表示白底黑字；True表示黑底白字
        if black_max > white_max:
            arg = True

        # 分割图像
        def find_end(start_):
            end_ = start_ + 1
            for m in range(start_ + 1, width - 1):
                if (black[m] if arg else white[m]) > (0.95 * black_max if arg else 0.95 * white_max):  # 0.95这个参数请多调整，对应下面的0.05
                    end_ = m
                    break
            return end_
        
        n = 1
        start = 1
        end = 2
        while n < width - 2:
            n += 1
            if (white[n] if arg else black[n]) > (0.05 * white_max if arg else 0.05 * black_max):
                # 上面这些判断用来辨别是白底黑字还是黑底白字
                # 0.05这个参数请多调整，对应上面的0.95
                start = n
                end = find_end(start)
                n = end
                if end - start > 1:
                    cj = image_array1[1:height+2, start:end+1]
                    #
                    #self.show(cj)
                    bno_found = True
                    for tab in tabs:
                        if "@" in tab:
                            data_tuple = tab.split("@")[1]
                            hex_str_16 = tab.split("@")[0]
                        else:
                            data_tuple = tab
                            hex_str_16 = tab.split("$")[0]
                        data_tuple = data_tuple.split("$")
                        if len(data_tuple):
                                p_hexstr_2 = data_tuple[0]
                                hexstr_2 = hexstr_16_to_hexstr_2(hex_str_16)
                                hexstr_2 += p_hexstr_2
                                word = data_tuple[1]
                                x = int(data_tuple[4])
                                y = int(data_tuple[3])
                                image_array = binstr_to_nparray(hexstr_2,x,y)
                                #if word == "6":
                                #     for w in image_array[0]
                                #      print("正在匹配字符: 7")
                                    # self.show(cj)
                                    # self.show(image_array)
                                new_X_t = self.matchTemplate(cj,image_array,M,getone=True)
                                #print(new_X_t)
                                if new_X_t !=(-1,-1):
                                    #print("当前识字为:{0}".format(word))
                                    strs += word 
                                    bno_found = False
                                    break
                    if bno_found:
                       strs += "?"                                            
        return strs
