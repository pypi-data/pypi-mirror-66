# -*- coding: utf-8 -*
from ...modules.rj25 import *
from ...boards.base import _BaseEngine
from ...comm.SerialPort import SerialPort
from ...comm import mlink
PORT1 = 1
PORT2 = 2
PORT3 = 3
PORT4 = 4
PORT5 = 5
PORT6 = 6
PORT7 = 7
PORT8 = 8
SLOT1 = 1
SLOT2 = 2
SLOT3 = 3
SLOT4 = 4
board = None
def connect(device=None,channel=None):
    global board
    if type(device)==int:
        channel = device
    if not board is None:
        return board
    if channel is None:
        channels = mlink.list()
        if len(channels)>0:
            device = mlink.connect(channels[0])
            board = Modules(device)
            return board
    else:
        device = mlink.connect(channel)
        board = Modules(device)
        return board
    if device is None:
        ports = [port[0] for port in SerialPort.list() if port[2] != 'n/a' and port[2].find('1A86:7523')>0 ]
        if len(ports)>0:
            device = SerialPort(ports[0])
            board = Modules(device)
            return board
    return Modules(device)

create = connect

class Modules(_BaseEngine):
    """

    """
    def __init__(self,device):
        super().__init__(_BaseEngine.MegaPi,device)
        
    def Servo(self,port,slot):
        return Servo(self,port,slot)

    def DCMotor(self,*argv):
        return DCMotor(self,*argv)

    def StepperMotor(self,slot):
        return StepperMotor(self,slot)

    def EncoderMotor(self,slot):
        return EncoderMotor(self,slot)

    def RGBLed(self,port,slot=2):
        return RGBLed(self,port,slot)

    def SevenSegmentDisplay(self,port):
        return SevenSegmentDisplay(self,port)

    def LedMatrix(self,port):
        return LedMatrix(self,port)

    def DSLRShutter(self,port):
        return DSLRShutter(self,port)
    
    def InfrareReceiver(self,port):
        return InfrareReceiver(self,port)

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