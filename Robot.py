# -*- coding: utf-8 -*-
#模板匹配
import cv2
import numpy as np
import io
import time
from ctypes import *
from PIL import ImageGrab,Image
import vbox
from utils import * 
from numba import jit
import data as da
from func_timeout import FunctionTimedOut ,func_timeout


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


class Robot:
    def __init__(self):
        self.vbox = None
        #窗口坐标
        self.left = 0
        self.top = 0 
        self.right = 0
        self.bottom = 0
        self.hwnd = None
        self.ScreenBoardhwnd = None
        self.game_width = 0
        self.game_height = 0
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


    def Get_GameHwnd(self,Simulator_Name="vbox",game_width=1280,game_height=720):
        if Simulator_Name != "vbox":
            pass
        else:
            self.vbox = vbox.Vbox()
            self.vbox.init()
            self.game_width = game_width
            self.game_height = game_height
            
    """
    x,y = findMultiColorInRegionFuzzy( "0xed1d60", "14|-7|0xb1cdf0,21|4|0xe2df73", 90, 0, 0, 1279, 719)
    """
    def findMultiColorInRegionFuzzy(self,color,posandcolor,degree,x1=None,y1=None,x2=None,y2=None,tab=None,islist=False):
        x = None
        y = None
        tolerance = 100 - degree
        r,g,b  = Hex_to_RGB(color)

        tpl = self.Print_screen()

        #self.show(tpl)
        posandcolor_list = list()
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
                    newY = p["px"] + y
                    newX = p["py"] + x
                    __rgb_hex = p["rgb_hex"]
                    if newY < y1 or newY > y2:
                        state = State.NOTMATCH
                        break
                    if newX < x1 or newX > x2:
                        state = State.NOTMATCH
                        break
                    b,g,r = tpl[newY,newX]
                    exR = int(__rgb_hex[2:4],16) 
                    exG = int(__rgb_hex[4:6],16) 
                    exB = int(__rgb_hex[6:8],16) 
                    if (pixelMatchesColor((r, g, b),(exR,exG,exB),tolerance)):
                        state = State.OK
                    else:
                        state = State.NOTMATCH
                        break
                if state == State.OK:
                    return State.OK,x-x1,y-y1
        return State.NOTMATCH,-1,-1
    
    def findMultiColorInRegionFuzzyByTable(self,t_Set,degree=60,x1=None,y1=None,x2=None,y2=None):
        tolerance = 100 - degree
        tpl = None
        tpl = self.Print_screen()
        state = State.NOTMATCH
        for x,y,rgb_16_hex in t_Set:
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
        #start = time.time()
        signedIntsArray = self.vbox.screenshots()
        image = Image.open(io.BytesIO(signedIntsArray))
        img = cv2.cvtColor(np.asarray(image),cv2.COLOR_RGB2BGR)
        #end = time.time()
        #print("Print_screen (with compilation) = %s" % (end - start))
        return img
    
    
    def show(self,tpl):
        cv2.namedWindow("Image")
        cv2.startWindowThread()
        cv2.imshow("Image",tpl)
        cv2.waitKey(0) 
        cv2.destroyAllWindows()        


    def matchTemplate(self,tpl,target,tolerance=0.2,getone=True):
        methods = [cv2.TM_SQDIFF_NORMED]   #3种模板匹配方法 cv2.TM_CCORR_NORMED, cv2.TM_CCOEFF_NORMED
        th, tw = target.shape[:2]
        
        for md in methods:
            if getone:  
                try:
                    res =cv2.matchTemplate(tpl,target, md)
                    ok = True
                except cv2.error as e: 
                    ok = False
                    return (-1,-1)
                
                min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
                if min_val > tolerance:
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
        return (-1,-1)
        
    def clike_map(self):
        tpl = self.Print_screen() 
        target = cv2.imread("./images/map.jpg")  
        new_target = self.matchTemplate(tpl,target)    
        self.click(new_target)  
        
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
    def mouse_Wheel(self,):
        pass
        
    
    def click(self,x:int=None,y:int=None,times=0.1):
        """Click at pixel xy."""
        self.vbox.put_mouse_event_absolute(x,y,times=float(times))

                        
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

    
    def x_Ocrtext(self,tabs,scx_rgb,x1,y1,x2,y2,similarity=0.2):
        #ret = re.findall(r"@(.*?)\$",tab,re.I|re.M)
        image_array1 = self.__Ocr(scx_rgb,x1, y1, x2, y2)
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
                    new_X_t = self.matchTemplate(image_array1,image_array,similarity)
                    #print(new_X_t)
                    if new_X_t !=(-1,-1):
                        print("当前识字为:{0}".format(word))
                        return word
        return ""

                    
                    
    def Ocrtext(self,tabs,scx_rgb,x1,y1,x2,y2,jiange=1,M=0.1):
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
                                new_X_t = self.matchTemplate(cj,image_array,M,getone=True)
                                if new_X_t !=(-1,-1):
                                    strs += word 
                                    bno_found = False
                                    break
                    if bno_found:
                       strs += "?"                                            
        return strs
    
    
    def WhileDo(self,color,
                posandcolor,degree,
                x1=None,y1=None,x2=None,y2=None,
                tab=None,blist=False,ischlik=1,name="None"):
        status = State.NOTMATCH
        while True:
            status,x,y= self.findMultiColorInRegionFuzzy(color,posandcolor,degree,x1,y1,x2,y2,tab,blist)
            if status==status.NOTMATCH:
                pass
            else:
                try:
                    for _ in range(0,ischlik):
                        print("click")
                        self.click(x1+x,y1+y)
                except:
                    pass
                print("found {0} ==> x:{1} y:{2}".format(name,x,y))
                break
        return status
    
    
    
    def Found_do(self,color,
                posandcolor,degree,
                x1=None,y1=None,x2=None,y2=None,
                tab=None,blist=False,timeout=10,ischlik=1,name="None"):
        doitReturnValue = State.ERROR
        try:
            doitReturnValue = func_timeout(timeout, self.WhileDo, args=(color,
                posandcolor,degree,
                x1,y1,x2,y2,
                tab,blist,ischlik,name))
        except FunctionTimedOut:
            pass
            #print ("获取时间超时\n")
        except Exception as e:
            pass
        return doitReturnValue