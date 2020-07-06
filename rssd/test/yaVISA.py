# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Yet(Just) Another VISA wrapper
### Author:  Martin C Lim
### Date:    2020.04.20
### Descrip: jaVISA mockup
###          properties for: Make; Model; Version; IDN; last error
###          logSCPI --> file for
#####################################################################
class jaVISA_mock(object):                          #pylint: disable=R0205
    ### Instrument Common functions
    def __init__(self):
        self.dataIDN    = ""    # Raw IDN String
        self.Make       = ""    # IDN Make
        self.Model      = ""    # IDN Model
        self.Device     = ""    # IDN Device
        self.Version    = ""    # IDN Version
        self.debug      = 1     # Print or not
        self.EOL        = '\n'
        self.f          = ''    # file log object

    def delay(self,sec):                            #pylint: disable=R0201,W0613
        pass

    def jav_Clear(self):                            #pylint: disable=R0201,W0613
        pass

    def jav_Close(self):                            #pylint: disable=R0201,W0613
        pass

    def jav_ClrErr(self):                           #pylint: disable=R0201,W0613
        return "no Error"

    def jav_Error(self):                            #pylint: disable=R0201,W0613
        return '0,No Error'

    def jav_IDN(self,prnt=1):                       #pylint: disable=R0201,W0613
        self.dataIDN    = "test"                    #Temp for self.query
        self.Make       = 'MakeTest'
        self.Model      = 'ModelTest'
        self.Device     = 'DevTest'
        self.Version    = '1.0.0'
        if self.debug: print('jav_IDN    : %s'%(self.dataIDN))
        return self.dataIDN

    def jav_OPC_Wait(self, InCMD):                  #pylint: disable=R0201,W0613
        return 0.0

    def jav_Open(self, IPAddr, fily=''):            #pylint: disable=R0201,W0613
        return self

    def jav_openvisa(self, sVISAStr, fily=''):      #pylint: disable=R0201,W0613
        return self

    def jav_read_raw(self):
        return b'1234567890'

    def jav_write_raw(self,SCPI):                   #pylint: disable=R0201,W0613
        pass

    def query(self,cmd):                            #pylint: disable=R0201,W0613
        return "<notRead>"

    def write(self,cmd):                            #pylint: disable=R0201,W0613
        pass

if __name__ == "__main__":
    RS = jaVISA_mock()
    RS.jav_openvisa(f'TCPIP::192.168.1.100::200::SOCKET')    #Socket
    print(RS.query("*IDN?"))
    RS.jav_Close()
