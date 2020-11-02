# -*- coding: future_fstrings -*-
'''RSSD VISA Bus class'''
# pylint: disable=signature-differs

import pyvisa
from rssd.RSI.time      import timer
from rssd.bus.bus       import bus

class jaVisa(bus):
    """Rohde & Schwarz VISA Class"""
    def __init__(self):
        self.VISA       = ''        # '@py' for pyvisa-py
        self.debug      = 1

    def close(self):
        """Close VISA Session"""
        try:
            errList = self.jav_ClrErr()
            self.K2.close()
            return errList
        except:
            pass

    def open(self, resourceID, param=0):            #pylint: disable=unused-argument
        """
        Open VISA object w/ VISA String.

        Examples:
            TCPIP0::<IP_Address>::inst0::INSTR
            TCPIP0::<IP_Address>::hislip0::INSTR
            TCPIP0::<IP_Address>::5025::SOCKET
            GPIB::<Addr>::INSTR
            ASRL1::INSTR
        """
        TMR = timer()
        TMR.start()
        rm = pyvisa.ResourceManager(self.VISA)                          #Create Resource Manager
        TMR.tick()
        #rmList = rm.list_resources()                                   #List VISA Resources
        try:
            # self.K2 = rm.open_resource(sVISAStr, open_timeout=100)    #Create Visa Obj
            self.K2 = rm.open_resource(resourceID)                      #Create Visa Obj
            self.K2.timeout = 5000                                      #Timeout, millisec
            # self.K2.write_termination = self.EOL
            # self.K2.read_termination  = self.EOL
            self.jav_IDN()
            self.jav_fileout(self.dataIDN)
            self.jav_ClrErr()
        except:
            if self.debug: print ('jav_OpnErr: ' + resourceID)
            self.K2 = 'NoVISA'
        TMR.tick()
        asdf = TMR.Get_Params_Time()
        return self

    def query(self, SCPIstr):
        rdStr = self.K2.query(SCPIstr)
        return rdStr

    def read_raw(self):
        return self.K2.read_raw()

    def reslist(self):
        try:
            rm = pyvisa.ResourceManager()                           #Create Resource Manager
            rmList = rm.list_resources()                            #List VISA Resources
        except:
            rmList =["No VISA"]
        return rmList

    def write(self, SCPIstr):
        self.K2.write(SCPIstr)

    def write_raw(self, SCPIstr):
        self.K2.write_raw(SCPIstr)

if __name__ == "__main__":
    RS = jaVisa()
    ipaddress   = '10.0.0.10'
    RS.open(f'TCPIP::{ipaddress}::hislip0::INSTR')        #hislip
    # RS.open(f'TCPIP::{ipaddress}::instr0::INSTR')         #VXI11
    # RS.open(f'TCPIP::{ipaddress}::5025::SOCKET')          #Socket
    print(RS.query('*IDN?'))
    RS.jav_Close()
