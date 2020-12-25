# -*- coding: utf-8 -*-
import threading
import time
import Robot as rb
import queue
exitFlag = 0

class myThread (threading.Thread,rb.Robot):
    def __init__(self,queue,class_name="subWin",title_name="sub",zoom_count=1.5):
        threading.Thread.__init__(self)
        rb.Robot.__init__(class_name=class_name,title_name=title_name,zoom_count=zoom_count)
        self.queue = queue
        
    def run(self):
        while True:
            if not self.queue.empty():  # 如果还有包子
                data = self.queue.get()
                if data in "check":
                    bfire = self.check_fire()
                    #print("check_fire:{0}".format(bfire))
                    if bfire:
                        self.fire()
                    time.sleep(5)
            
    

