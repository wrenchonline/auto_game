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
        try: 
            while True:
                if not self.queue.empty():  # 如果还有队列数据
                    data = self.queue.get(False)
                    if data in "check":
                        bfire = self.check_fire()
                        if bfire:
                            self.fire()
                            while True:
                                status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                                if status==status.NOTMATCH:
                                    time.sleep(0.5)        
                                else:
                                    self.click(1581,823)
                                    time.sleep(0.5)
                                    break
                            self.check_thePetHealth()
                            
                            self.queue.task_done()
                        else:
                            self.queue.task_done()
                    if data in "exit":
                        print("退出监控员")
                        self.queue.task_done()
                        break
                time.sleep(2)
        except BaseException as e: 
            self.exc = e 
            self.someFunction()
            
    def join(self): 
        threading.Thread.join(self)
        if self.exc: 
            raise self.exc