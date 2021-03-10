# -*- coding: utf-8 -*-
import threading
import time
import sys
import Robot as rb
import queue
import data as da
exitFlag = 0

# Custom Exception Class 
class MyException(Exception): 
    pass

class MyThread (threading.Thread,rb.Robot):
    def __init__(self,q,class_name="subWin",title_name="sub",zoom_count=1.5):
        threading.Thread.__init__(self)
        rb.Robot.__init__(self,class_name=class_name,title_name=title_name,zoom_count=zoom_count)
        self.Get_GameHwnd()
        if isinstance(q,queue.Queue):
            self.queue = q
        else:
            raise("参数2不是队列")
            
  # Function that raises the custom exception 
    def someFunction(self,): 
        name = threading.current_thread().name 
        raise MyException(self.exc) 


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
                                self.fire()
                                fire_end = True
                                #self.check_thePetHealth()
                            else:
                                while fire_end:
                                    status,x,y=self.findMultiColorInRegionFuzzy(da.prompt_box["取消自动战斗"]["基点"],da.prompt_box["取消自动战斗"]["偏移"],80,671,310,1188,638)
                                    #status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                                    if status==status.NOTMATCH:
                                        time.sleep(0.5)        
                                    else:
                                        #361|164   计算取消自动战斗栏 公式是范围x + 基点x +偏移361 ，范围y + 基点y +偏移164 
                                        cancel_fire_x = 671+x+361
                                        cancel_fire_y = 310+y+164
                                        self.click(cancel_fire_x,cancel_fire_y)
                                        time.sleep(0.5)
                                        break
                                if fire_end:
                                    break
                                break
                                #self.queue.task_done()
                        self.queue.task_done()
                    if data in "exit":
                        print("退出监控员")
                        self.queue.task_done()
                        break
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