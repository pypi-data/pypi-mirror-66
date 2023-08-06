# -*- coding: utf-8 -*
from time import sleep
from ...modules.cyberpi import *
from ...boards.base import _BaseEngine
from ...protocols.PackData import HalocodePackData
from ...comm.SerialPort import SerialPort
from ...comm import mlink
MODE_REQUEST = 0
MODE_CHANGE = 1
MODE_PERIOD = 2
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
            return board.api
    else:
        device = mlink.connect(channel)
        board = Modules(device).api
        return board
    if device is None:
        ports = [port[0] for port in SerialPort.list() if port[2] != 'n/a' and port[2].find('1A86:7523')>0 ]
        if len(ports)>0:
            device = SerialPort(ports[0])
            board = Modules(device).api
            return board
    '''
        :description: CyberPi - |cyberpi_more_info|

        .. |cyberpi_more_info| raw:: html
        
            <a href="http://docs.makeblock.com/halocode/en/tutorials/introduction.html" target="_blank">More Info</a>
            
        :example:
        .. code-block:: python
            :linenos:

            from time import sleep
            from makeblock import CyberPi

            board = CyberPi.connect()

    '''
    return Modules(device).api

create = connect
from makeblock.modules.cyberpi import api_cyberpi_api
class Modules(_BaseEngine):
    def __init__(self,device):
        super().__init__(_BaseEngine.Halocode,device)
        if device.type!='mlink':
            while not self.protocol.ready:
                self.broadcast()
                sleep(0.1)
                
        self.setTransferMode()
        
        self.module_auto = BaseModuleAuto(self)
        api_cyberpi_api.module_auto = self.module_auto
        self.api = api_cyberpi_api

    def setTransferMode(self):
        # pack = HalocodePackData()
        # pack.type = HalocodePackData.TYPE_SCRIPT
        # pack.mode = HalocodePackData.TYPE_RUN_WITHOUT_RESPONSE
        # pack.script = "global_objects.communication_o.enable_protocol(global_objects.communication_o.REPL_PROTOCOL_GROUP_ID)"
        # self.call(pack)
        # sleep(1)
        # self.repl('import communication')
        # self.repl('communication.bind_passthrough_channels("uart0", "uart1")')
        # sleep(1)

        pass

    def broadcast(self):
        pack = HalocodePackData()
        pack.type = HalocodePackData.TYPE_SCRIPT
        pack.mode = HalocodePackData.TYPE_RUN_WITH_RESPONSE
        pack.script = "cyberpi.get_name()"
        self.call(pack)
