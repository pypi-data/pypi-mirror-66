# -*- coding: utf-8 -*
import struct
from time import ctime, sleep
import threading
import makeblock
import makeblock.utils as utils
from makeblock.protocols.PackData import NeuronPackData

class _BaseModule:
    def __init__(self,board,idx=1,mode=1,period=0):
        self._pack = None
        self.setup(board,idx,mode,period)
        
    def _callback(self,data):
        pass

    def quit(self):
        makeblock.quit()

    def setup(self,board,idx,mode=1,period=0):
        self._board = board
        self._mode = mode
        self._pack = NeuronPackData()
        self._pack.idx = idx
        self._init_module()
    
    def _init_module(self):
        pass

    def force_update(self):
        self._pack.data = [0x1]
        self.request(self._pack)

    def request(self,pack):
        self._board.remove_response(pack)
        self._board.request(pack)

    def call(self,pack):
        self._board.call(pack)

    def subscribe(self,pack):
        self._board.request(pack)

class Temperature(_BaseModule):
    def _init_module(self):
        self._temperature = 0
        self._pack.type = NeuronPackData.TYPE_SENSOR
        self._pack.service = 0x63
        self._pack.subservice = 0x1
        self._pack.on_response = self.__on_parse
        self.__subscribe()
        
    def __on_parse(self, pack):
        self._temperature = utils.bits2float(pack.data[1:6])
        self._callback(self._temperature)

    def __on_subscribe_response(self, pack):
        if len(pack.data)>6:
            self._temperature = utils.bits2float(pack.data[1:6])

    def on_change(self,callback):
        self._callback = callback

    @property
    def temperature(self):
        return self._temperature

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class Humiture(_BaseModule):
    def _init_module(self):
        self._pack.type = NeuronPackData.TYPE_SENSOR
        self._pack.service = 0x63
        self._pack.subservice = 0x19
        self._pack.on_response = self.__on_parse
        self._status = {"temp":0,"hum":0}
        self.__subscribe()
        
    def __on_parse(self, pack):
        self._status["temp"] = utils.bits2short(pack.data[1:3])
        self._status["hum"] = pack.data[3]
        self._callback(self._status)

    def __on_subscribe_response(self, pack):
        if len(pack.data)>3:
            self._status["temp"] = utils.bits2short(pack.data[1:3])
            self._status["hum"] = pack.data[3]

    def on_change(self,callback):
        self._callback = callback

    @property
    def temperature(self):
        return self._status["temp"]
    
    @property
    def humiture(self):
        return self._status["hum"]

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)

class Ultrasonic(_BaseModule):
    def _init_module(self):
        self._distance = 0
        self._pack.service = 0x63
        self._pack.subservice = 0x16
        # self._pack.on_response = self.__on_parse
        self.__subscribe();
        
    def __on_parse(self, pack):
        self._distance = int(utils.bits2float(pack.data[1:6])*10)/10
        # self._callback(self._distance)

    def __on_subscribe_response(self,pack):
        self._distance = int(utils.bits2float(pack.data[1:6])*10)/10

    def on_change(self,callback):
        self._callback = callback

    def get_distance(self,callback):
        self._pack.on_response = callback
        self.force_update()
    
    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)

    @property
    def distance(self):
        return self._distance

class Slider(_BaseModule):
    def _init_module(self):
        self._value = 0
        self._pack.service = 0x64
        self._pack.subservice = 0xd
        self._pack.on_response = self.__on_parse
        self.__subscribe()
    
    def __on_parse(self, pack):
        if len(pack.data)>1:
            self._value = pack.data[1]
            self._callback(self._value)

    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            self._value = pack.data[1]

    def on_change(self,callback):
        self._callback = callback

    def get_value(self,callback):
        self._callback = callback
        self.force_update()

    @property
    def value(self):
        return self._value

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)

class MQ2(_BaseModule):
    def _init_module(self):
        self._value = 0
        self._pack.service = 0x63
        self._pack.subservice = 0x1c
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            self._value = pack.data[1]
    
    @property
    def value(self):
        return self._value

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class Light(_BaseModule):
    def _init_module(self):
        self._value = 0
        self._pack.service = 0x63
        self._pack.subservice = 0x14
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            self._value = pack.data[1]
    
    @property
    def value(self):
        return self._value

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)
        
class SoilMoisture(_BaseModule):
    def _init_module(self):
        self._value = 0
        self._pack.service = 0x63
        self._pack.subservice = 0x15
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            self._value = pack.data[1]
    
    @property
    def value(self):
        return self._value

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)
     
class Sound(_BaseModule):
    def _init_module(self):
        self._value = 0
        self._pack.service = 0x63
        self._pack.subservice = 0x13
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            self._value = pack.data[1]
    
    @property
    def value(self):
        return self._value

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class Touch(_BaseModule):
    def _init_module(self):
        self._value = 0
        self._pack.service = 0x63
        self._pack.subservice = 0xa
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            self._value = pack.data[1]
    
    @property
    def value(self):
        return self._value

    def channel(self,idx=0):
        return (self._value>>idx)&0x1

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class Button(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x64
        self._pack.subservice = 0xb
        self._status = {"is_pressed":False,"count":0}
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            if pack.data[0]==1:
                self._status["is_pressed"] = pack.data[1]==1
            elif pack.data[0]==2:
                self._status["count"] = utils.bits2long(pack.data[1:6])
    
    @property
    def is_pressed(self):
        return self._status["is_pressed"]
    
    @property
    def count(self):
        return self._status["count"]

    def reset(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x3]
        self.call(pack)

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class Joystick(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x64
        self._pack.subservice = 0xc
        self._x = 0
        self._y = 0
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            self._x = utils.bits2int8(pack.data[1:3])
            self._y = utils.bits2int8(pack.data[3:5])
    
    @property
    def x(self):
        return self._x
    
    @property
    def y(self):
        return self._y

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class LaserRanging(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x63
        self._pack.subservice = 0x12
        self._distance = 0
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            self._distance = utils.bits2float(pack.data[1:6])
    
    @property
    def distance(self):
        return self._distance

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class Flame(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x63
        self._pack.subservice = 0x1b
        self._value = 0
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            self._value = utils.bits2int8(pack.data[1:3])
    
    @property
    def value(self):
        return self._value

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class PIRMotion(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x63
        self._pack.subservice = 0x17
        self._status = {"is_moving":False,"count":0}
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            if pack.data[0]==1:
                self._status["is_moving"] = pack.data[1]==1
            elif pack.data[0]==2:
                self._status["count"] = utils.bits2long(pack.data[1:6])
    
    @property
    def is_moving(self):
        return self._status["is_moving"]
    
    @property
    def count(self):
        return self._status["count"]

    def reset(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x3]
        self.call(pack)

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class Magnetic(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x63
        self._pack.subservice = 0x1e
        self._status = {"is_magnetic":False,"count":0}
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            if pack.data[0]==1:
                self._status["is_magnetic"] = pack.data[1]==1
            elif pack.data[0]==2:
                self._status["count"] = utils.bits2long(pack.data[1:6])
    
    @property
    def is_magnetic(self):
        return self._status["is_magnetic"]
    
    @property
    def count(self):
        return self._status["count"]

    def reset(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x3]
        self.call(pack)

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class Angle(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x63
        self._pack.subservice = 0xe
        self._status = {"direction":0,"speed":0,"angle":0}
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            if pack.data[0]==1:
                self._status["angle"] = utils.bits2long(pack.data[1:6])
            elif pack.data[0]==2:
                self._status["direction"] = pack.data[1]
            elif pack.data[0]==4:
                self._status["speed"] = utils.bits2long(pack.data[1:6])
    
    @property
    def angle(self):
        return self._status["angle"]
    
    @property
    def direction(self):
        return self._status["direction"]

    @property
    def speed(self):
        return self._status["speed"]

    def reset(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x3]
        self.call(pack)

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class Motion(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x63
        self._pack.subservice = 0x1a
        self._status = {"intensity":0,"speed":0,"angle":0}
        self.__subscribe()
    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            if pack.data[0]==1:
                self._status["intensity"] = pack.data[1]
            elif pack.data[0]==2:
                self._status["acceleration_x"] = utils.bits2float(pack.data[1:6])
            elif pack.data[0]==3:
                self._status["acceleration_y"] = utils.bits2float(pack.data[1:6])
            elif pack.data[0]==4:
                self._status["acceleration_z"] = utils.bits2float(pack.data[1:6])
            elif pack.data[0]==5:
                self._status["velocity_x"] = utils.bits2float(pack.data[1:6])
            elif pack.data[0]==6:
                self._status["velocity_y"] = utils.bits2float(pack.data[1:6])
            elif pack.data[0]==7:
                self._status["velocity_z"] = utils.bits2float(pack.data[1:6])
            elif pack.data[0]==8:
                self._status["pitch"] = utils.bits2short(pack.data[1:3])
            elif pack.data[0]==9:
                self._status["roll"] = utils.bits2short(pack.data[1:3])
    
    @property
    def intensity(self):
        return self._status["intensity"]
    
    @property
    def acceleration_x(self):
        return self._status["acceleration_x"]

    @property
    def acceleration_y(self):
        return self._status["acceleration_y"]

    @property
    def acceleration_z(self):
        return self._status["acceleration_z"]

    @property
    def velocity_x(self):
        return self._status["velocity_x"]

    @property
    def velocity_y(self):
        return self._status["velocity_y"]

    @property
    def velocity_z(self):
        return self._status["velocity_z"]

    @property
    def pitch(self):
        return self._status["pitch"]

    @property
    def roll(self):
        return self._status["roll"]

    def reset(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x4]
        self.call(pack)
        pack.data = [0x5]
        self.call(pack)
        pack.data = [0x6]
        self.call(pack)

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        for i in range(9):
            pack.data = [0x1,NeuronPackData.TYPE_CHANGE,i+0x1]
            pack.data.extend(utils.long2bits(0))
            self.subscribe(pack)


class Color(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x63
        self._pack.subservice = 0x11
        self._status = {"intensity":[0,0],"reflect":[0,0],"color":[{'red':0,'green':0,'blue':0},{'red':0,'green':0,'blue':0}]}
        self.__subscribe()

    
    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            if pack.data[0]==0x8:
                self._status["color"][0]["red"] = utils.bits2short(pack.data[1:3])
                self._status["color"][0]["green"] = utils.bits2short(pack.data[3:5])
                self._status["color"][0]["blue"] = utils.bits2short(pack.data[5:7])
                self._status["color"][1]["red"] = utils.bits2short(pack.data[7:9])
                self._status["color"][1]["green"] = utils.bits2short(pack.data[9:11])
                self._status["color"][1]["blue"] = utils.bits2short(pack.data[11:13])
            elif pack.data[0]==0x9:
                self._status["intensity"][0] = utils.bits2short(pack.data[1:3])
                self._status["intensity"][1] = utils.bits2short(pack.data[3:5])
            elif pack.data[0]==0xa:
                self._status["reflect"][0] = utils.bits2short(pack.data[1:3])
                self._status["reflect"][1] = utils.bits2short(pack.data[3:5])
    
    def color(self,idx=0):
        if idx>1:
            idx=1
        if idx<0:
            idx=0
        return self._status["color"][idx]

    def intensity(self,idx=0):
        if idx>1:
            idx=1
        if idx<0:
            idx=0
        return self._status["intensity"][idx]

    def reflect(self,idx=0):
        if idx>1:
            idx=1
        if idx<0:
            idx=0
        return self._status["reflect"][idx]

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x78,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)
        pack.data = [0x79,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)
        pack.data = [0x7a,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)

class GPIO(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x68
        self._pack.subservice = 0x1
        self._callback = None

    def __on_parse(self,pack):
        if not self._callback is None:
            if pack.data[0]==3:
                self._callback(utils.bits2short(pack.data[1:3]))
            elif pack.data[0]==2:
                self._callback(pack.data[1])

    def digital_write(self,pin,level):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x1,pin,level]
        self.call(pack)

    def pwm_write(self,pin,pwm,freq=1000):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x4,pin]
        pack.data.extend(utils.float2bits(freq))
        pack.data.extend(utils.float2bits(pwm))
        self.call(pack)

    def digital_read(self,pin,callback):
        self._callback = callback
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x2,pin]
        self.request(pack)

    def analog_read(self,pin,callback):
        self._callback = callback
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x3,pin]
        self.request(pack)

    def enable(self,status=0):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x5,status]
        self.call(pack)

class PowerManager(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x64
        self._pack.subservice = 0x9
        self._status = {"current":0,"voltage":0,"wireless":0,"power":0}
        self.__subscribe()

    def __on_subscribe_response(self,pack):
        if len(pack.data)>1:
            if pack.data[0]==0x1:
                self._status["wireless"] = pack.data[1]
                self._status["power"] = pack.data[2]
            elif pack.data[0]==0x2:
                self._status["voltage"] = utils.bits2float(pack.data[1:6])
                self._status["current"] = utils.bits2float(pack.data[6:11])

    @property
    def current(self):
        return self._status["current"]
    
    @property
    def voltage(self):
        return self._status["voltage"]

    @property
    def wireless(self):
        return self._status["wireless"]

    @property
    def power(self):
        return self._status["power"]

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)
        pack.data = [0x7e,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)

class Infrarer(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x68
        self._pack.subservice = 0x2
    
    def send_message(self,msg=""):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x2,len(msg)]
        pack.data.extend(utils.string2bytes(msg))
        self.call(pack)

    def record(self,idx=0,time=3000):
        if idx>1:
            idx=1
        if idx<0:
            idx=0
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x3]
        pack.data.extend(utils.long2bits(time))
        pack.data.append(idx)
        self.call(pack)

    def send_record(self,idx=0):
        if idx>1:
            idx=1
        if idx<0:
            idx=0
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x4,idx]
        self.call(pack)

class RGBLed(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x65
        self._pack.subservice = 0x2
    
    def set_color(self,red,green,blue):
        self._pack.data = [0x1]
        self._pack.data.extend(utils.ushort2bits(red))
        self._pack.data.extend(utils.ushort2bits(green))
        self._pack.data.extend(utils.ushort2bits(blue))
        self.call(self._pack)
    
class LedStrip(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x65
        self._pack.subservice = 0x3
    
    def set_color(self,index,red,green,blue):
        self._pack.data = [0x1,index]
        self._pack.data.extend(utils.ushort2bits(red))
        self._pack.data.extend(utils.ushort2bits(green))
        self._pack.data.extend(utils.ushort2bits(blue))
        self.call(self._pack)

class LedMatrix(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x65
        self._pack.subservice = 0x9
    
    def set_pixel(self,index,red,green,blue):
        self._pack.data = [0x2,index]
        self._pack.data.extend(utils.ushort2bits(red))
        self._pack.data.extend(utils.ushort2bits(green))
        self._pack.data.extend(utils.ushort2bits(blue))
        self.call(self._pack)
    
    def set_pixels(self,bits,red,green,blue):
        self._pack.data = [0x1]
        for i in range(2):
            self._pack.data.extend(utils.long2bits(bits[i]))
        self._pack.data.extend(utils.ushort2bits(red))
        self._pack.data.extend(utils.ushort2bits(green))
        self._pack.data.extend(utils.ushort2bits(blue))
        self.call(self._pack)

    def set_string(self,msg):
        l = len(msg)
        self._pack.data = [0x7]
        self._pack.data.extend(utils.ushort2bits(l))
        for i in range(l):
            self._pack.data.append(ord(msg[i]))
        self.call(self._pack)

class Servo(_BaseModule):
    BOTH_SERVOS = 1
    LEFT_SERVO = 2
    RIGHT_SERVO = 3
    def _init_module(self):
        self._pack.service = 0x62
        self._pack.subservice = 0xa
    
    def set_angle(self,angle):
        angle = int(angle)
        self._pack.data = [0x1]
        self._pack.data.extend(utils.ushort2bits(angle))
        self.call(self._pack)
    
    def release(self):
        self._pack.data = [0x6]
        self.call(self._pack)

class DCMotor(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x62
        self._pack.subservice = 0x9
    
    def set_pwm(self,pwm):
        self._pack.data = [0x1]
        self._pack.data.extend(utils.int2bits(pwm))
        self.call(self._pack)


class EncoderMotor(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x62
        self._pack.subservice = 0x6
        self._status = {"stall":False}

    def set_speed(self,speed):
        if speed>320:
            speed = 320
        if speed<-320:
            speed = -320
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x4]
        pack.data.extend(utils.ushort2bits(speed))
        self.call(pack)

    def set_pwm(self,pwm):
        if pwm>255:
            pwm = 255
        if pwm<-255:
            pwm = -255
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x11]
        pack.data.extend(utils.ushort2bits(pwm))
        self.call(pack)

    def move_to(self,position,speed):
        if speed>320:
            speed = 320
        if speed<0:
            speed = 0
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x2]
        pack.data.extend(utils.long2bits(position))
        pack.data.extend(utils.ushort2bits(speed))
        self.call(pack)

    def move(self,position,speed):
        if speed>320:
            speed = 320
        if speed<0:
            speed = 0
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x3]
        pack.data.extend(utils.long2bits(position))
        pack.data.extend(utils.ushort2bits(speed))
        self.call(pack)

    def set_lock(self,lock):
        if lock>1:
            lock = 1
        if lock<0:
            lock = 0
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x14,lock]
        self.call(pack)

    def set_zero(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x12]
        self.call(pack)

    def stop(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x5]
        self.call(pack)

    def __on_subscribe_response(self,pack):
        if pack.data[0]==0x27:
            self._status["stall"] = pack.data[1]==1
    
    @property
    def stall(self):
        return self._status["stall"]

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7d,NeuronPackData.TYPE_CHANGE]
        pack.data.extend(utils.long2bits(0))
        self.subscribe(pack)

class ExtDCMotor(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x62
        self._pack.subservice = 0x7

    def reset(self,port):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x1,port]
        self.call(pack)

    def set_pwm(self,port,pwm):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x2,port]
        pack.data.extend(utils.ushort2bits(pwm))
        self.call(pack)

    def stop(self,port):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x3,port]
        self.call(pack)

class SmartServo(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x60
        self._callback = None
        self._status = {"speed":0,"position":0,"temp":0,"current":0,"voltage":0}
        self.__subscribe()

    def __on_parse(self,pack):
        if not self._callback is None:
            if pack.subservice == 0x41:
                self._callback(pack.data[0])

    def __on_subscribe_response(self,pack):
        if pack.subservice==0x36:
            self._status["position"] = utils.bits2long(pack.data[0:5])
        elif pack.subservice==0x23:
            self._status["speed"] = int(utils.bits2float(pack.data[0:5])*10)/10
        elif pack.subservice==0x25:
            self._status["temp"] = int(utils.bits2float(pack.data[0:5])*100)/100
        elif pack.subservice==0x26:
            self._status["current"] = int(utils.bits2float(pack.data[0:5])*100)/100
        elif pack.subservice==0x27:
            self._status["voltage"] = int(utils.bits2float(pack.data[0:5])*100)/100

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.data = [NeuronPackData.TYPE_CHANGE]
        pack.subservice = 0x36
        self.subscribe(pack)
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.data = [NeuronPackData.TYPE_CHANGE]
        pack.subservice = 0x23
        pack.data = [NeuronPackData.TYPE_CHANGE]
        self.subscribe(pack)
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.data = [NeuronPackData.TYPE_CHANGE]
        pack.subservice = 0x25
        pack.data = [NeuronPackData.TYPE_CHANGE]
        self.subscribe(pack)
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.data = [NeuronPackData.TYPE_CHANGE]
        pack.subservice = 0x26
        pack.data = [NeuronPackData.TYPE_CHANGE]
        self.subscribe(pack)
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.data = [NeuronPackData.TYPE_CHANGE]
        pack.subservice = 0x27
        pack.data = [NeuronPackData.TYPE_CHANGE]
        self.subscribe(pack)

    @property
    def position(self):
        return self._status["position"]

    @property
    def speed(self):
        return self._status["speed"]

    @property
    def voltage(self):
        return self._status["voltage"]

    @property
    def current(self):
        return self._status["current"]

    @property
    def temperature(self):
        return self._status["temp"]

    def set_lock(self,lock):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x16
        pack.data = [lock]
        self.call(pack)

    def set_led(self,red,green,blue):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x17
        pack.data = []
        pack.data.extend(utils.ushort2bits(red))
        pack.data.extend(utils.ushort2bits(green))
        pack.data.extend(utils.ushort2bits(blue))
        self.call(pack)

    def set_zero(self):
        pack = NeuronPackData()
        pack.service = self._pack.service
        pack.subservice = 0x30
        self.call(pack)

    def move_to(self,position,speed):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x33
        pack.data = []
        pack.data.extend(utils.long2bits(position))
        pack.data.extend(utils.ushort2bits(speed))
        self.call(pack)

    def move(self,position,speed):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x34
        pack.data = []
        pack.data.extend(utils.long2bits(position))
        pack.data.extend(utils.ushort2bits(speed))
        self.call(pack)
    
    def set_rotation(self,rotation,during):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x2a
        pack.data = []
        pack.data.extend(utils.float2bits(rotation))
        pack.data.extend(utils.ushort2bits(during))
        self.call(pack)

    def set_pwm(self,pwm):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x35
        pack.data = []
        pack.data.extend(utils.short2bits(pwm))
        self.call(pack)

    def set_absolute_angle_with_force(self,angle,speed,force=100):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x38
        pack.data = []
        pack.data.extend(utils.long2bits(angle))
        pack.data.extend(utils.ushort2bits(speed))
        pack.data.extend(utils.ushort2bits(force))
        self.call(pack)

    def set_relative_angle_with_force(self,angle,speed,force=100):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x39
        pack.data = []
        pack.data.extend(utils.long2bits(angle))
        pack.data.extend(utils.ushort2bits(speed))
        pack.data.extend(utils.ushort2bits(force))
        self.call(pack)

    def set_speed(self,speed):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x3a
        pack.data = []
        pack.data.extend(utils.int2bits(speed))
        self.call(pack)

    def home(self,direction,speed):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x43
        pack.data = [direction]
        pack.data.extend(utils.ushort2bits(speed))
        self.call(pack)

    def request_error(self,callback):
        self._callback = callback
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x41
        pack.on_response = self.__on_parse
        self.request(pack)

    def clear_error(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = 0x42
        self.call(pack)

class Speaker(_BaseModule):
    def _init_module(self):
        self._pack.service = 0x66
        self._pack.subservice = 0x4

    def play_tone(self,hz):
        self._pack.data = [0x2]
        self._pack.data.extend(utils.ushort2bits(hz))
        self.call(self._pack)
    
class FingertipPiano(_BaseModule):
    '''
        :description: Fingertip Piano
        :example:
        .. code-block:: python
            :linenos:

            piano = FingertipPiano(1)

    '''
    def _init_module(self):
        self._isExiting = False
        self._pack.service = 0x64
        self._pack.subservice = 0xf
        self._piano = {'touch1_strength':0,'touch2_strength':0,'touch3_strength':0,'touch4_strength':0,'keyA':0,'keyB':0,'touch1':0,'touch2':0,'touch3':0,'touch4':0,'joystick_x':0,'joystick_y':0,'distance':0,'keyA_count':0,'keyB_count':0,'last_touched':0,'last_pressed':0,'gesture':0}
        self.__subscribe()
        # self._thread = threading.Thread(target=self._thread_detect,args=())
        # self._thread.start()
        # self._board.add_thread(self)

    # def _thread_detect(self):
    #     while True:
    #         if self._isExiting:
    #             break
    #         self._detecting()
    #         sleep(0.1)

    # def _detecting(self):
    #     # print("detecting")
    #     pass

    def __on_parse(self, pack):
        pass

    def __on_subscribe_response(self,pack):
        if pack.data[0]==0x2:
            self._piano['keyA'] = pack.data[1]
            self._piano['keyB'] = pack.data[2]
        elif pack.data[0]==0x3:
            self._piano['touch1'] = pack.data[1]
            self._piano['touch2'] = pack.data[2]
            self._piano['touch3'] = pack.data[3]
            self._piano['touch4'] = pack.data[4]
        elif pack.data[0]==0x6:
            self._piano['gesture'] = pack.data[1]
        elif pack.data[0]==0x5:
            self._piano['joystick_x'] = utils.bits2int8(pack.data[1:3])
            self._piano['joystick_y'] = utils.bits2int8(pack.data[3:5])
        elif pack.data[0]==0x7:
            self._piano['distance'] = pack.data[1]
        elif pack.data[0]==0x8:
            self._piano['touch1_strength'] = utils.bits2short(pack.data[1:3])
            self._piano['touch2_strength'] = utils.bits2short(pack.data[3:5])
            self._piano['touch3_strength'] = utils.bits2short(pack.data[5:7])
            self._piano['touch4_strength'] = utils.bits2short(pack.data[7:9])
        elif pack.data[0]==0x9:
            self._piano['keyA_count'] = utils.bits2long(pack.data[1:6])
            self._piano['keyB_count'] = utils.bits2long(pack.data[6:11])

    def __subscribe(self):
        pack = NeuronPackData()
        pack.on_response = self.__on_subscribe_response
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x7f,NeuronPackData.TYPE_CHANGE,0,0,0,0]
        self.subscribe(pack)
        pack.data = [0x7e,NeuronPackData.TYPE_CHANGE,0,0,0,0]
        self.subscribe(pack)
        pack.data = [0x7d,NeuronPackData.TYPE_CHANGE,0,0,0,0]
        self.subscribe(pack)
        pack.data = [0x7c,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)
        pack.data = [0x7b,NeuronPackData.TYPE_CHANGE,0,0,0,0]
        self.subscribe(pack)
        pack.data = [0x7a,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)
        pack.data = [0x78,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)
        pack.data = [0x79,NeuronPackData.TYPE_PERIOD]
        pack.data.extend(utils.long2bits(100))
        self.subscribe(pack)

    def count_pressed(self,idx):
        """
            :description: count of button pressed

            :param idx: button number, 'A' or 'B' 
            :type idx: str
            :return: count
            :rtype: int
            :example:

            .. code-block:: python
                :linenos:

                while True:
                    print(piano.count_pressed('A'),piano.count_pressed('B'))
                    sleep(1)

        """
        if idx==1 or idx.lower()=='a':
            return self._piano['keyA_count']
        if idx==2 or idx.lower()=='b':
            return self._piano['keyB_count']

    def is_pressed(self,idx):
        """
            :description: the status will changed when the button is pressed
            :param idx: the button number, 'A' or 'B' 
            :type idx: str
            :return: whether the button is pressed
            :rtype: int
            :example:

            .. code-block:: python
                :linenos:

                while True:
                    print(piano.is_pressed('A'),piano.is_pressed('B'))
                    sleep(1)

        """
        if idx==1 or (type(idx)==str and idx.lower()=='a'):
            return self._piano['keyA']
        if idx==2 or (type(idx)==str and idx.lower()=='b'):
            return self._piano['keyB']

    @property
    def is_obstacle_ahead(self):
        return self.distance<95

    @property
    def obstacle_moving(self):
        return self.gesture

    def last_pressed(self,idx=0):
        if idx==1:
            idx = 'A'
        elif idx==2:
            idx = 'B'
        if idx==0:
            if (self._piano['keyA']+self._piano['keyB'])==0 and self._piano['last_pressed']!=idx:
                self._piano['last_pressed']=idx
                return 0
        elif self._piano['key'+idx] and self._piano['last_pressed']!=idx:
            self._piano['last_pressed']=idx
            return 0
        return 1

    def touch_value(self,idx):
        if idx==1 or (type(idx)==str and idx.lower()=='a'):
            return int(self._piano['touch1_strength']*100/256)
        elif idx==2 or (type(idx)==str and idx.lower()=='b'):
            return int(self._piano['touch2_strength']*100/256)
        elif idx==3 or (type(idx)==str and idx.lower()=='c'):
            return int(self._piano['touch3_strength']*100/256)
        elif idx==4 or (type(idx)==str and idx.lower()=='d'):
            return int(self._piano['touch4_strength']*100/256)

    def is_touched(self,idx):
        """
            :description: the status will changed when the touchpad is touched
            :param idx: the touchpad number, range: 1~4 
            :type idx: int
            :return: whether the touchpad is touched
            :rtype: int
            :example:

            .. code-block:: python
                :linenos:

                while True:
                    print(piano.is_touched(1),piano.is_touched(2))
                    sleep(1)

        """
        if idx==1 or (type(idx)==str and idx.lower()=='a'):
            return self._piano['touch1']
        elif idx==2 or (type(idx)==str and idx.lower()=='b'):
            return self._piano['touch2']
        elif idx==3 or (type(idx)==str and idx.lower()=='c'):
            return self._piano['touch3']
        elif idx==4 or (type(idx)==str and idx.lower()=='d'):
            return self._piano['touch4']

    def last_touched(self,idx=0):
        if idx==0:
            if self._piano['touch4']+self._piano['touch1']+self._piano['touch2']+self._piano['touch3']==0 and self._piano['last_touched']!=idx:
                self._piano['last_touched']=idx
                return 0
        elif self._piano['touch'+str(idx)] and self._piano['last_touched']!=idx:
            self._piano['last_touched']=idx
            return 0
        return 1

    @property
    def gesture(self):
        return self._piano['gesture']

    @property
    def distance(self):
        return self._piano['distance']

    @property
    def ir_intensity(self):
        return 100 - self.distance

    @property
    def joystick_x(self):
        return self._piano['joystick_x']

    @property
    def joystick_y(self):
        return self._piano['joystick_y']

    @property
    def joystick_direction(self):
        if self.is_joystick_up:
            return self.DIRECTION_UP
        elif self.is_joystick_down:
            return self.DIRECTION_DOWN
        elif self.is_joystick_left:
            return self.DIRECTION_LEFT
        elif self.is_joystick_right:
            return self.DIRECTION_RIGHT
        return self.DIRECTION_HOME

    @property
    def is_joystick_up(self):
        return self._piano['joystick_y']>30

    @property
    def is_joystick_down(self):
        return self._piano['joystick_y']<-30

    @property
    def is_joystick_left(self):
        return self._piano['joystick_x']<-30

    @property
    def is_joystick_right(self):
        return self._piano['joystick_x']>30
        
    @property
    def DIRECTION_HOME(self):
        return 0

    @property
    def DIRECTION_UP(self):
        return 1

    @property
    def DIRECTION_DOWN(self):
        return 2

    @property
    def DIRECTION_LEFT(self):
        return 3

    @property
    def DIRECTION_RIGHT(self):
        return 4

    @property  
    def GESTURE_NONE(self):
        return 0

    @property  
    def GESTURE_WAVING(self):
        return 1
    
    @property  
    def GESTURE_MOVING_DOWN(self):
        return 2

    @property  
    def GESTURE_MOVING_UP(self):
        return 3

    @property
    def APPROACHING(self):
        return self.GESTURE_MOVING_DOWN

    @property
    def AWAY(self):
        return self.GESTURE_MOVING_UP

    def set_led(self,red=0,green=0,blue=0):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x1]
        pack.data.extend(utils.ushort2bits(red))
        pack.data.extend(utils.ushort2bits(green))
        pack.data.extend(utils.ushort2bits(blue))
        self.call(pack)

    def led_on(self,red=0,green=0,blue=0):
        self.set_led(red,green,blue)

    def led_off(self):
        self.set_led(0,0,0)

    def reset_button(self,idx=2):
        self.reset_button(idx)

    def reset_pressed(self,idx=2):
        if type(idx)==str:
            if idx.lower()=='a':
                idx = 0
            elif idx.lower()=='b':
                idx = 1
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x11,idx]
        self.call(pack)
    
    def calibrate(self):
        pack = NeuronPackData()
        pack.idx = self._pack.idx
        pack.service = self._pack.service
        pack.subservice = self._pack.subservice
        pack.data = [0x10]
        self.call(pack)