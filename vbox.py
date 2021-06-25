from ast import While
import remotevbox
from PIL import Image
from io import BytesIO
import queue
import time

from remotevbox.exceptions import (
    MachineCloneError,
    MachineCoredumpError,
    MachineCreateError,
    MachineDisableNetTraceError,
    MachineDiscardError,
    MachineEnableNetTraceError,
    MachineExtraDataError,
    MachineInfoError,
    MachineLaunchError,
    MachineLockError,
    MachinePauseError,
    MachinePowerdownError,
    MachineSaveError,
    MachineSetTraceFileError,
    MachineSnaphotError,
    MachineSnapshotError,
    MachineSnapshotNX,
    MachineUnlockError,
    MachineVrdeInfoError,
    ProgressTimeout,
    WrongLockState,
    WrongMachineState,
)

class Vbox:
    
    def __init__(self,name="wrench",password="ljl767689") -> None:
        self.vbox = None
        self.machine = None
        self.queue = queue.Queue()
        self.vs = None
        self.fps = None
        self.name = name
        self.password = password


    def __del__(self) -> None:
        print("Quit Vbox")
        self.vbox.disconnect()
        
    def init(self)-> None:
        self.vbox = remotevbox.connect("http://127.0.0.1:18083", self.name, self.password)
        machines = self.vbox.list_machines()
        self.machine = self.vbox.get_machine(machines[0])
        self.machine.launch()
        self.machine.lock()

        
    def lock(self):
        self.machine.lock()
        
        
    def screenshots(self):
        BF = True
        while BF:
            try: 
                self.screenshot_data = self.machine.take_screenshot_to_bytes(image_format="PNG")
                BF = False
                break
            except BaseException as e:
                continue
        return self.screenshot_data

    def screenshots_loop(self):
        while True:
            if not self.queue.empty():
                items = self.queue.get(timeout=0.2)
                self.screenshot_data = self.machine.take_screenshot_to_bytes()
                self.queue.task_done()
                
    def put_mouse_event_absolute(self,
        x,
        y,
        dz=0,
        dw=0,
        left_pressed=True,
        right_pressed=False,
        middle_pressed=False,
        times = 0.1)->None:
        x=int(x)
        y=int(y)
        self.machine.put_mouse_event_absolute(x,
                    y,
                    dz,
                    dw,
                    left_pressed=left_pressed,
                    right_pressed=right_pressed,
                    middle_pressed=middle_pressed)
        time.sleep(times)
        self.machine.put_mouse_event_absolute(x,
                    y,
                    dz,
                    dw,
                    left_pressed=False,
                    right_pressed=right_pressed,
                    middle_pressed=middle_pressed)
        time.sleep(times)
