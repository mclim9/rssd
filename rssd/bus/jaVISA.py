'''RSSD VISA Bus class'''
# pylint: disable=signature-differs
import os
import pyvisa
import logging
from rssd.RSI.time      import timer
from rssd.bus.bus       import bus

class jaVisa(bus):
    """Rohde & Schwarz VISA Class"""
    def __init__(self):
        self.EOL        = '\n'              # \n or \r\n
        self.VISA       = ''                # '@py' for pyvisa-py
        self.debug      = 1
        logging.basicConfig(level=logging.INFO, \
                            filename=os.path.splitext(__file__)[0] + '.log', filemode='w', \
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def close(self):
        """Close VISA Session"""
        try:
            self.K2.close()
            self.rm.close()
        except:
            logging.info(f'jaV-Close : Could not close')

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
        self.rm = pyvisa.ResourceManager(self.VISA)                     # Create Resource Manager
        self.ResID = resourceID
        TMR.tick()
        try:
            # self.K2 = rm.open_resource(resourceID, open_timeout=100)  # Create Visa Obj
            self.K2 = self.rm.open_resource(self.ResID)                 # Create Visa Obj
            self.K2.timeout = 5000                                      # Timeout, millisec
            self.K2.write_termination = self.EOL
            self.K2.read_termination  = self.EOL
        except:
            logging.info(f'jaV_OpnErr: {self.ResID}')
            self.K2 = 'NoVISA'
        TMR.tick()
        asdf = TMR.Get_Params_Time()
        return self

    def query(self, SCPIstr):
        rdStr = '<notRead>'
        try:
            rdStr = self.K2.query(SCPIstr)
        except AttributeError:                                          # K2 = string
            logging.info(f'jaV_RdErr : {self.ResID}-->{SCPIstr}')
        return rdStr

    def read_raw(self):
        return self.K2.read_raw()

    def reslist(self):
        try:
            rmList = self.rm.list_resources()                           #List VISA Resources
        except:
            rmList =["No VISA"]
        return rmList

    def write(self, SCPIstr):
        try:
            self.K2.write(SCPIstr)
        except AttributeError:                                          # K2 = string
            logging.info(f'jaV_WrtErr: {self.ResID}-->{SCPIstr}')

    def write_raw(self, SCPIstr):
        self.K2.write_raw(SCPIstr)

if __name__ == "__main__":
    ipaddress   = '192.168.58.15'
    RS = jaVisa().open(f'TCPIP::{ipaddress}::hislip0::INSTR')           # hislip
    RS = jaVisa().open(f'TCPIP::{ipaddress}::instr0::INSTR')            # VXI11
    RS = jaVisa().open(f'TCPIP::{ipaddress}::5025::SOCKET')             # Socket
    print(RS.query('*IDN?'))

    RS.close()
