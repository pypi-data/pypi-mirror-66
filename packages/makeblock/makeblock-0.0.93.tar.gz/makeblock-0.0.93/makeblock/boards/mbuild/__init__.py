# -*- coding: utf-8 -*
import makeblock.modules.mbuild
import makeblock.protocols as Protocols
from ...boards.base import _BaseEngine
from ...protocols.PackData import NeuronPackData
from ...comm.SerialPort import SerialPort
from ...comm import mlink
from time import sleep
MODE_REQUEST = 0
MODE_CHANGE = 1
MODE_PERIOD = 2
GESTURE_NONE = 0
GESTURE_WAVING = 1
GESTURE_MOVING_UP = 2
GESTURE_MOVING_DOWN = 3
C3 = 131
D3 = 147
E3 = 165
F3 = 174
G3 = 196
A3 = 220
B3 = 247
C4 = 261
D4 = 293
E4 = 329
F4 = 349
G4 = 392
A4 = 440
B4 = 493
C5 = 523
D5 = 587
E5 = 659
F5 = 698
G5 = 784
A5 = 880
B5 = 987
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
    '''
        :description: mBuild
        :example:
        .. code-block:: python
            :linenos:

            from time import sleep
            from makeblock import SerialPort
            from makeblock import mBuild

            uart = SerialPort.connect("COM3")
            board = mBuild.connect(uart)

    '''
    return Modules(device)

create = connect

def Piano(idx=1):
    '''
        :description: Fingertip Piano
        :example:
        .. code-block:: python
            :linenos:

            from time import sleep
            from makeblock import mBuild

            piano = mBuild.Piano()
            print(piano.is_pressed('A'),piano.is_pressed('B'),piano.is_touched(1),piano.is_touched(2),piano.is_touched(3),piano.is_touched(4),piano.joystick_x,piano.joystick_y,piano.distance)
    '''
    global board
    if board is None:
        ports = [port[0] for port in SerialPort.list() if port[2] != 'n/a' and port[2].find('1A86:7523')>0 ]
        if len(ports)>0:
            uart = SerialPort(ports[0])
            board = create(uart)
            return makeblock.modules.mbuild.FingertipPiano(board,idx)
        return None
    else:
        return makeblock.modules.mbuild.FingertipPiano(board,idx)

def Speaker(idx=1):
    '''
        :description: Speaker
        :example:
        .. code-block:: python
            :linenos:

            speaker = mBuild.Speaker(2)
            while True:
                speaker.play_tone(mBuild.C4)
                sleep(0.25)
                speaker.play_tone(mBuild.D4)
                sleep(0.25)
                speaker.play_tone(mBuild.E4)
                sleep(0.25)
                speaker.play_tone(mBuild.F4)
                sleep(0.25)
                speaker.play_tone(0)
                sleep(0.25)
    '''
    global board
    if not board is None:
        return makeblock.modules.mbuild.Speaker(board,idx)

class Modules(_BaseEngine):
    '''
    '''
    def __init__(self,device):
        super().__init__(_BaseEngine.mBuild,device)
        self.broadcast()

    def broadcast(self):
        self.call(NeuronPackData.broadcast())

    def Speaker(self,idx=1):
        return makeblock.modules.mbuild.Speaker(self,idx)

    def LedMatrix(self,idx=1):
        return makeblock.modules.mbuild.LedMatrix(self,idx)

    def RGBLed(self,idx=1):
        return makeblock.modules.mbuild.RGBLed(self,idx)

    def LedStrip(self,idx=1):
        return makeblock.modules.mbuild.LedStrip(self,idx)

    def FingertipPiano(self,idx=1):
        return makeblock.modules.mbuild.FingertipPiano(self,idx)

    def Ultrasonic(self,idx=1):
        return makeblock.modules.mbuild.Ultrasonic(self,idx)

    def Button(self,idx=1):
        return makeblock.modules.mbuild.Button(self,idx)

    def Slider(self,idx=1):
        return makeblock.modules.mbuild.Slider(self,idx)

    def Joystick(self,idx=1):
        return makeblock.modules.mbuild.Joystick(self,idx)

    def SoilMoisture(self,idx=1):
        return makeblock.modules.mbuild.SoilMoisture(self,idx)

    def LaserRanging(self,idx=1):
        return makeblock.modules.mbuild.LaserRanging(self,idx)

    def Flame(self,idx=1):
        return makeblock.modules.mbuild.Flame(self,idx)

    def Touch(self,idx=1):
        return makeblock.modules.mbuild.Touch(self,idx)

    def Sound(self,idx=1):
        return makeblock.modules.mbuild.Touch(self,idx)

    def Light(self,idx=1):
        return makeblock.modules.mbuild.Touch(self,idx)
    
    def PIRMotion(self,idx=1):
        return makeblock.modules.mbuild.PIRMotion(self,idx)

    def Magnetic(self,idx=1):
        return makeblock.modules.mbuild.Magnetic(self,idx)

    def Angle(self,idx=1):
        return makeblock.modules.mbuild.Angle(self,idx)

    def Motion(self,idx=1):
        return makeblock.modules.mbuild.Motion(self,idx)

    def Servo(self,idx=1):
        return makeblock.modules.mbuild.Servo(self,idx)

    def DCMotor(self,idx=1):
        return makeblock.modules.mbuild.DCMotor(self,idx)

    def EncoderMotor(self,idx=1):
        return makeblock.modules.mbuild.EncoderMotor(self,idx)

    def Color(self,idx=1):
        return makeblock.modules.mbuild.Color(self,idx)

    def GPIO(self,idx=1):
        return makeblock.modules.mbuild.GPIO(self,idx)

    def PowerManager(self,idx=1):
        return makeblock.modules.mbuild.PowerManager(self,idx)

    def Infrarer(self,idx=1):
        return makeblock.modules.mbuild.Infrarer(self,idx)

    def ExtDCMotor(self,idx=1):
        return makeblock.modules.mbuild.ExtDCMotor(self,idx)

    def SmartServo(self,idx=1):
        return makeblock.modules.mbuild.SmartServo(self,idx)
    
    