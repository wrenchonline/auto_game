 
# -*- coding: utf-8 -*-
import threading
import time
import Robot as rb
import queue
import data as da
import cv2
from utils import * 
exitFlag = 0

# Custom Exception Class 
class MyException(Exception): 
    pass

class MyThread (threading.Thread,rb.Robot):
    def __init__(self,q):
        threading.Thread.__init__(self)
        rb.Robot.__init__(self)
        self.Get_GameHwnd()
        if isinstance(q,queue.Queue):
            self.queue = q
        else:
            raise("参数2不是队列")
        
  # Function that raises the custom exception 
    def someFunction(self,): 
        name = threading.current_thread().name 
        raise MyException(self.exc) 


    #检测是否属于战斗状态
    def check_fire(self):
        status,ag= self.findMultiColorInRegionFuzzyByTable(da.Fire)
        if status != status.OK:
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
    #开始战斗
    def fire(self):
        #bfired = False
        while True:
            status = self.Found_do(da.utils["自动战斗"]["基点"],da.utils["自动战斗"]["偏移"], 90, 1202,653,1254,710,ischlik=0,name="自动战斗",timeout=1)
            if status != status.OK:
                    break
            else:
                print("发现自动战斗")
                #bfired = True
                self.click(1230,662)
                print("点击自动战斗")
                time.sleep(5)
                continue
            
    def testfire(self):
        while True:
            bfire = self.check_fire()
            if bfire:
                time.sleep(1)
                self.fire()
                fire_end = True
                print("正在战斗")
            else:
                while fire_end:
                    print("战斗结束")
                    status = self.Found_do(da.utils["战斗取消"]["基点"],da.utils["战斗取消"]["偏移"], 
                                        80,0, 0,1279,719,
                                        ischlik=2,timeout=10,
                                        name="战斗取消")
                    if status == State.NOTMATCH:
                        raise 
                    break
                if fire_end:
                    fire_end = False
                    break
            time.sleep(2)

    def run(self): 
        # Variable that stores the exception, if raised by someFunction 
        self.exc = None
        fire_end = False
        try: 
            while True:
                if not self.queue.empty():  # 如果还有队列数据
                    data = self.queue.get(False)
                    if data in "check":
                        while True:
                            bfire = self.check_fire()
                            if bfire:
                                time.sleep(1)
                                self.fire()
                                fire_end = True
                                print("正在战斗")
                            else:
                                while fire_end:
                                    print("战斗结束")
                                    status = self.Found_do(da.utils["战斗取消"]["基点"],da.utils["战斗取消"]["偏移"], 
                                                        80,0, 0,1279,719,
                                                        ischlik=1,timeout=10,
                                                        name="战斗取消")
                                    if status == State.NOTMATCH:
                                        raise 
                                    break
                                if fire_end:
                                    fire_end = False
                                    break
                            time.sleep(2)
                        self.queue.task_done()
                    if data in "exit":
                        print("退出监控员")
                        self.queue.task_done()
                        break
                else:
                    time.sleep(5)
                #检查安全令牌
                # status,x,y=self.findMultiColorInRegionFuzzy(da.prompt_box["弹出令牌界面"]["基点"],da.prompt_box["弹出令牌界面"]["偏移"],80,1213,502, 1264,561)
                # if status==status.NOTMATCH:
                #     pass
                # else:
                #     print("检测到安全提示框弹出，正在关闭....")
                #     cancel_safe_x = 1213 + x
                #     cancel_safe_y = 502 + y
                #     self.click(cancel_safe_x,cancel_safe_y)
                #     time.sleep(0.5)
                # time.sleep(2)
        except BaseException as e:
            self.exc = e
            self.someFunction()
            
    def join(self): 
        threading.Thread.join(self)
        if self.exc: 
            raise self.exc