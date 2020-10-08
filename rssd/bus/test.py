# -*- coding: future_fstrings -*-
#pylint: disable=R0201,W0613
'''RSSD test bus class'''

from rssd.bus.bus import bus

class jaTest(bus):                          #pylint: disable=R0205
    """Instrument Common functions"""
    def __init__(self):
        self.EOL        = '\n'

    def Open(self, IPAddr, fily=''):
        self.connected          = 0
        return self

    def read_raw(self):
        return b'1234567890'

    def write_raw(self,SCPI):
        pass

    def query(self,cmd):
        return "<notRead>"

    def write(self,cmd):
        pass

if __name__ == "__main__":
    RS = jaTest()
    RS.jav_openvisa(f'TCPIP::192.168.1.100::200::SOCKET')    #Socket
    print(RS.query("*IDN?"))
    RS.jav_Close()
