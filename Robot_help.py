# -*- coding: utf-8 -*-
import threading
import time
import Robot as rb
import queue
import data as da
exitFlag = 0

# Custom Exception Class 
class MyException(Exception): 
    pass

class MyThread (threading.Thread,):
    def __init__(self,q,Robot=None):
        threading.Thread.__init__(self)
        self.Robot = Robot
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
                    data = self.queue.get()
                    if data in "check":
                        while True:
                            bfire = self.Robot.check_fire()
                            if bfire:
                                self.Robot.fire()
                                fire_end = True
                                time.sleep(5)
                                print("正在战斗")
                            else:
                                while fire_end:
                                    print("战斗结束")
                                    # status,x,y=self.Robot.findMultiColorInRegionFuzzy(da.prompt_box["取消自动战斗"]["基点"],da.prompt_box["取消自动战斗"]["偏移"],50,671,310,1188,638)
                                    # #status,ag= self.findMultiColorInRegionFuzzyByTable(da.zhujiemian)
                                    # if status==status.NOTMATCH:
                                    #     time.sleep(0.5)        
                                    # else:
                                    #     #361|164   计算取消自动战斗栏 公式是范围x + 基点x +偏移361 ，范围y + 基点y +偏移164 
                                    #     cancel_fire_x = 671+x+361
                                    #     cancel_fire_y = 310+y+164
                                    #     self.Robot.click(cancel_fire_x,cancel_fire_y)
                                    #     time.sleep(0.5)
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
                else:
                    time.sleep(5)
        except BaseException as e:
            self.exc = e
            self.someFunction()
            
    def join(self): 
        threading.Thread.join(self)
        if self.exc: 
            raise self.exc