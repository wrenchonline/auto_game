import remotevbox
from PIL import Image
from io import BytesIO


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
    
    def __init__(self) -> None:
        self.vbox = None
        self.machine = None
        
    def __del__(self) -> None:
        print("Quit Vbox")
        self.vbox.disconnect()
        
    def init(self)-> None:
        self.vbox = remotevbox.connect("http://127.0.0.1:18083", "wrench", "ljl767689")
        machines = self.vbox.list_machines()
        # for m in self.machines:
        #     print(m)
        self.machine = self.vbox.get_machine(machines[0])
        self.machine.launch()
        
    def lock(self):
        self.machine.lock()
        
        
    def screenshots(self):
        try:
            self.screenshot_data = self.machine.take_screenshot_to_bytes()
        except WrongLockState as e:
            self.machine.lock()
            self.screenshot_data = self.machine.take_screenshot_to_bytes()
        #bytes_stream = BytesIO(self.screenshot_data)
        #roiimg = Image.open(bytes_stream)
        return self.screenshot_data
        #roiimg.show()
    def put_mouse_event_absolute(self,
        x,
        y,
        dz=0,
        dw=0,
        left_pressed=True,
        right_pressed=False,
        middle_pressed=False,)->None:
        self.machine.put_mouse_event_absolute(x,
                    y,
                    dz,
                    dw,
                    left_pressed=left_pressed,
                    right_pressed=right_pressed,
                    middle_pressed=middle_pressed)
        self.machine.put_mouse_event_absolute(x,
                    y,
                    dz,
                    dw,
                    left_pressed=left_pressed,
                    right_pressed=right_pressed,
                    middle_pressed=middle_pressed)        
        self.machine.put_mouse_event_absolute(x,
                    y,
                    dz,
                    dw,
                    left_pressed=False,
                    right_pressed=right_pressed,
                    middle_pressed=middle_pressed)
        