# -*- coding: utf-8 -*-
#模板匹配
import cv2 as cv
import numpy as np
import numpy 
import win32gui 
import win32api
import win32ui
import win32con
import pynput
import time
import ctypes
from ctypes import *

numbers_images = {'0':"num_0",'1':"num_1",'2':"num_2",'3':"num_3",'4':"num_4",'5':"num_5",'6':"num_6",
           '7':"num_7",'8':"num_8",'9':"num_9"}


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
        self.game_width = 0
        self.game_height = 0
        self.zoom_count = zoom_count

        
    def Get_GameHwnd(self):
        self.hwnd= win32gui.FindWindow('Qt5QWindowIcon','夜神模拟器')
        self.hwnd = win32gui.FindWindowEx(self.hwnd, 0, 'Qt5QWindowIcon', 'ScreenBoardClassWindow')
        self.hwnd = win32gui.FindWindowEx(self.hwnd, 0, self.class_name, self.title_name)
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
            
        else:
            print("Not found game hwnd")
            
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
        
        im_opencv = np.fromstring(signedIntsArray, dtype = 'uint8')
        
        im_opencv.shape = (self.game_height,self.game_width,4)
        
        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, hWndDC)
        
        # cv.imwrite("im_opencv.jpg",im_opencv,[int(cv.IMWRITE_JPEG_QUALITY), 100]) #保存
        # cv.namedWindow('im_opencv') #命名窗口
        # cv.imshow("im_opencv",im_opencv) #显示
        
        return  cv.cvtColor(im_opencv, cv.IMWRITE_JPEG_QUALITY)
        
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


    def animateMoveAndClick(self,curPos, targetPos, durTime=1, fps=60, waitTime=1):
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

    def matchTemplate(self,tpl,target):
        methods = [cv.TM_SQDIFF_NORMED]   #3种模板匹配方法 cv.TM_CCORR_NORMED, cv.TM_CCOEFF_NORMED
        th, tw = target.shape[:2]
        
        for md in methods:
            result = cv.matchTemplate(tpl,target, md)
            min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)
            if md == cv.TM_SQDIFF_NORMED:
                tl = min_loc
            else:
                tl = max_loc
            br = (tl[0]+tw, tl[1]+th)   #br是矩形右下角的点的坐标
            a=int((self.left + tl[0]+int(tw/2))/self.zoom_count)
            b=int((self.top + tl[1]+int(th/2))/self.zoom_count)
            new_target = (a,b)
            # cv.rectangle(tpl,tl,br,(0, 0, 255),1)  
            # cv.imshow('t',tpl)  
            # cv.waitKey(0)  
            return new_target     
        
    def clike_map(self):
        tpl = self.Print_screen() 
        target = cv.imread("./images/map.jpg")  
        new_target = self.matchTemplate(tpl,target)    
        self.animateMoveAndClick(self.getCurPos(),new_target) 
        
    
    def clike_x_map(self,number:str):
        global numbers_images
        tpl = self.Print_screen() 
        target = cv.imread("./images/map_x.jpg") 
        new_target = self.matchTemplate(tpl,target)
        self.animateMoveAndClick(self.getCurPos(),new_target) 
        time.sleep(3)
        
        number_list = [n for n in number]
        for n in number_list:
            tpl = self.Print_screen() 
            number_images = "./images/"+ numbers_images[n] + ".jpg"
            X_t = cv.imread(number_images) 
            new_X_t = self.matchTemplate(tpl,X_t)
            self.animateMoveAndClick(self.getCurPos(),new_X_t)
            
            
        tpl = self.Print_screen() 
        target = cv.imread("./images/ok.jpg")
        new_target = self.matchTemplate(tpl,target)
        self.animateMoveAndClick(self.getCurPos(),new_target) 
        time.sleep(1) 
        
            
    def clike_y_map(self,number:str):
        global numbers_images
        tpl = self.Print_screen() 
        target = cv.imread("./images/map_y.jpg") 
        new_target = self.matchTemplate(tpl,target)
        self.animateMoveAndClick(self.getCurPos(),new_target) 
        time.sleep(3)
        
        number_list = [n for n in number]
        for n in number_list:
            tpl = self.Print_screen() 
            number_images = "./images/"+ numbers_images[n] + ".jpg"
            X_t = cv.imread(number_images) 
            new_X_t = self.matchTemplate(tpl,X_t)
            self.animateMoveAndClick(self.getCurPos(),new_X_t)
            
            
        tpl = self.Print_screen() 
        target = cv.imread("./images/ok.jpg")
        new_target = self.matchTemplate(tpl,target)
        self.animateMoveAndClick(self.getCurPos(),new_target) 
        time.sleep(1)             
            

        
        
def main():
    
    blRobot = Robot(class_name="subWin",title_name="sub",zoom_count=1.5)
    blRobot.Get_GameHwnd()
    blRobot.clike_map()
    time.sleep(3)
    blRobot.clike_x_map("56")
    blRobot.clike_x_map("57")
    
    
    
    
    
    cv.waitKey(0)
    cv.destroyAllWindows()
    

          
    
if __name__ == "__main__":
    main()
    
    