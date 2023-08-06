# -*- coding: utf-8 -*
from makeblock.boards.base import _BaseEngine
from makeblock.modules.rj25 import *

PORT1 = 1
PORT2 = 2
PORT3 = 3
PORT4 = 4
PORT5 = 5
PORT2 = 6
PORT7 = 7
PORT8 = 8
SLOT1 = 1
SLOT2 = 2
SLOT3 = 3
SLOT4 = 4
M1 = 1
M2 = 2
def connect(device):
    return Modules(device)

create = connect

class Modules(_BaseEngine):
    
    def __init__(self,device):
        super().__init__(_BaseEngine.MegaPi,device)

    def Servo(self,port,slot):
        return Servo(self,port,slot)

    def DCMotor(self,port):
        return DCMotor(self,port)

    def RGBLed(self,port,slot=2):
        return RGBLed(self,port,slot)

    def SevenSegmentDisplay(self,port):
        return SevenSegmentDisplay(self,port)

    def LedMatrix(self,port):
        return LedMatrix(self,port)

    def DSLRShutter(self,port):
        return DSLRShutter(self,port)
    
    def InfraredReceiver(self,port):
        return InfraredReceiver(self,port)

    def Ultrasonic(self,port):
        return Ultrasonic(self,port)

    def Button(self,port):
        return Button(self,port)

    def LineFollower(self,port):
        return LineFollower(self,port)

    def LimitSwitch(self,port,slot=2):
        return LimitSwitch(self,port,slot)

    def PIRMotion(self,port):
        return PIRMotion(self,port)

    def Light(self,port):
        return Light(self,port)
    
    def Sound(self,port):
        return Sound(self,port)

    def Potentiometer(self,port):
        return Potentiometer(self,port)

    def Joystick(self,port):
        return Joystick(self,port)

    def Gyro(self):
        return Gyro(self)

    def Compass(self):
        return Compass(self)

    def Temperature(self,port,slot):
        return Temperature(self,port,slot)

    def Humiture(self,port):
        return Humiture(self,port)

    def Flame(self,port):
        return Flame(self,port)

    def Gas(self,port):
        return Gas(self,port)

    def Touch(self,port):
        return Touch(self,port)

    def Color(self,port):
        return Color(self,port)

    def Pin(self):
        return Pin(self)