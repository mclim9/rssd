# -*- coding: future_fstrings -*-
#pylint: disable=R0201,W0613
'''RSSD test bus class'''

from rssd.bus import bus

class jaVISA_mock(bus):                          #pylint: disable=R0205
    """Instrument Common functions"""
    def __init__(self):
        self.EOL        = '\n'

    def Open(self, IPAddr, fily=''):
        self.debug = 0
        self.VISA  = '@py'
        self.open(host)
        self.connected      = 1
        if self.bus == 'Nobus':
            mock = jaVISA_mock()
            self.open               = mock.open
            self.write              = mock.write
            self.query              = mock.query
            self.instr_Clear        = mock.instr_Clear
            self.instr_Error        = mock.instr_Error
            self.instr_read_raw     = mock.instr_read_raw
            self.instr_write_raw    = mock.instr_write_raw
            self.connected          = 0
        self.instr_ClrErr()
        self.dLastErr = ""
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
    RS = jaVISA_mock()
    RS.jav_openvisa(f'TCPIP::192.168.1.100::200::SOCKET')    #Socket
    print(RS.query("*IDN?"))
    RS.jav_Close()
