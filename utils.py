# -*- coding: utf-8 -*-
import string
from enum import Enum, unique
import binascii
import numpy as np
from numba import jit


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
    r = int(hex[1:3],16)
    g = int(hex[3:5],16)
    b = int(hex[5:7], 16)
    # rgb = str(r)+','+str(g)+','+str(b)
    # print(rgb)
    return r , g ,b


class State(Enum):
    OK = 1
    ERROR = 2
    ROLLBACK = 3
    NOTMATCH = 4
    
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
