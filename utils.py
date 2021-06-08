# -*- coding: utf-8 -*-
import string
from enum import Enum
import cv2


# RGB格式颜色转换为16进制颜色格式
def toHex(tmp) :  
	rgb = tmp.split(",")  
	strs = "#"  
	for j in range (0, len(rgb)):  
		num = string.atoi(rgb[j])  
		strs += str(hex(num))[-2:]  #每次转换之后只取0x7b的后两位，拼接到strs中  
	print("转换后的16进制值为：")  
	print(strs) 
 
def rgb_to_hex(tup):
    """Convert RGB value to hex."""
    return '%02x%02x%02x'.upper() % (tup[0], tup[1], tup[2])

 
# 16进制颜色格式颜色转换为RGB格式
def Hex_to_RGB(hex):
    r = int(hex[2:4],16)
    g = int(hex[4:6],16)
    b = int(hex[6:8], 16)
    # rgb = str(r)+','+str(g)+','+str(b)
    # print(rgb)
    return r , g ,b


class State(Enum):
    OK = 1
    ERROR = 2
    ROLLBACK = 3
    NOTMATCH = 4
    
ascii_char = list("$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. ")  

#将256灰度映射到70个字符上  
def get_char(r,g,b,alpha=256):#alpha透明度  
    if alpha==0:  
        return ' '
    length=len(ascii_char)  
    gray=int(0.2126*r+0.7152*g+0.0722*b)#计算灰度  
    unit=(256.0+1)/length  
    return ascii_char[int(gray/unit)]#不同的灰度对应着不同的字符 
    
    
#rgb误差函数，反正是从pyscreeze这上面抄的魔改的
def pixelMatchesColor(pix,expectedRGBColor,tolerance=0):
    """
    TODO
    """
    if len(pix)==3 and len(expectedRGBColor) == 3: #RGB mode
        r,g,b = pix[:3] 
        exR, exG, exB = expectedRGBColor[:3]
        return (abs(r - exR) <= tolerance) and (abs(g - exG) <= tolerance) and (abs(b - exB) <= tolerance)
    else:
        assert False, 'Color mode was expected to be length 3 (RGB) or 4 (RGBA), but pixel is length %s and expectedRGBColor is length %s' % (len(pix), len(expectedRGBColor))



def encode(s):
    return ' '.join([bin(ord(c)).replace('0b', '') for c in s])
 
def decode(s):
    return ''.join([chr(i) for i in [int(b, 2) for b in s.split(' ')]])
    
# >>>encode('hello')
# '1101000 1100101 1101100 1101100 1101111'
# >>>decode('1101000 1100101 1101100 1101100 1101111')
# 'hello'

def hexstr_16_to_hexstr_2(hex_str):
    x = bin(int('1'+hex_str, 16))[3:]#含有前导0的转换
    return x

def hexstr_16_to_hexint_2(hex_str):
    x = bytes.fromhex(hex_str)
    return x

def display(dianzhen_str,x,y,bx):
    dianzhen_str += bx 
    #初始化22*23的点阵位置，每个汉字需要16*16=256个点来表示
    rect_list = list()
    for j in range(x):
        rect_list.append([] * y) 
        for k in range(y):
           rect_list[j].append([] * y) 
    i = 0
    for j in range(x):
        for k in range(y):
            rect_list[j][k]=int(dianzhen_str[i])
            i+=1;
    i = 0
    for j in range(y):
        for k in range(x):
            if rect_list[k][j]:
                 #前景字符（即用来表示汉字笔画的输出字符）
                print('◼', end=' ')
            else:
                # 背景字符（即用来表示背景的输出字符）
                print('◻', end=' ')   
        print()
        
def pian_color(img):
    l_channel, a_channel, b_channel = cv2.split(img)
    h,w,_ = img.shape
    da = a_channel.sum()/(h*w)-128
    db = b_channel.sum()/(h*w)-128
    histA = [0]*256
    histB = [0]*256
    for i in range(h):
        for j in range(w):
            ta = a_channel[i][j]
            tb = b_channel[i][j]
            histA[ta] += 1
            histB[tb] += 1
    msqA = 0
    msqB = 0
    for y in range(256):
        msqA += float(abs(y-128-da))*histA[y]/(w*h)
        msqB += float(abs(y - 128 - db)) * histB[y] / (w * h)
    import math
    result = math.sqrt(da*da+db*db)/math.sqrt(msqA*msqA+msqB*msqB)
    print("d/m = %s"%result)
    