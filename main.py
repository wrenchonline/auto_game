# -*- coding: utf-8 -*-
import Robot as rb
import time
import pytesseract
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
def main():
    config = ('--psm 6 digits')
    blRobot = rb.Robot(class_name="subWin",title_name="sub",zoom_count=1.5)
    blRobot.Get_GameHwnd()
    start = time.time()
    img_cv = cv2.imread('C:\\Users\\Wrench\\Nox_share\\ImageShare\\Screenshots\\asd.png',0)#灰度处理
    th2 = cv2.adaptiveThreshold(img_cv,255,cv2.ADAPTIVE_THRESH_MEAN_C,cv2.THRESH_BINARY,11,2)
    # cv2.namedWindow("Image")
    # cv2.imshow("Image", th2)
    # cv2.waitKey (0)
    strx = int(pytesseract.image_to_string(th2,lang='eng',config=config))
    print("识别的数字为:{0}".format(strx))
    end = time.time()
    print("Elapsed (with compilation) = %s" % (end - start))
    
if __name__ == "__main__":
    main()
    
    
    