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
import time

class jaVISA_mock(object):
    ### Instrument Common functions. 
    def __init__(self):
        self.dataIDN    = ""    # Raw IDN String
        self.Make       = ""    # IDN Make
        self.Model      = ""    # IDN Model
        self.Device     = ""    # IDN Device
        self.Version    = ""    # IDN Version 
        self.debug      = 1     # Print or not.
        self.EOL        = '\n'
        self.f          = ''    # file log object

    def delay(self,sec):
        pass

    def jav_Clear(self):
        pass

    def jav_Close(self):
        pass

    def jav_ClrErr(self):
        return "no Error"

    def jav_Error(self):
        return '0,No Error'

    def jav_IDN(self,prnt=1):
        self.dataIDN    = "test"                               #Temp for self.query
        self.Make       = 'MakeTest'
        self.Model      = 'ModelTest'
        self.Device     = 'DevTest'
        self.Version    = '1.0.0'
        if self.debug: print('jav_IDN    : %s'%(self.dataIDN))
        return self.dataIDN
                
    def jav_OPC_Wait(self, InCMD):
        return 0.0

    def jav_Open(self, IPAddr, fily='',prnt=1):
        return self

    def jav_openvisa(self, sVISAStr, fily='',prnt=1):
        return self

    def jav_fileout(self, fily, outstr):
        try:
            if fily != '':
                fily.write(outstr.strip())
        except:
            pass

    def jav_Reset(self):
        pass

    def jav_logscpi(self):
        pass

    def jav_read_raw(self):
        pass

    def jav_write_raw(self,SCPI):
        pass

    def jav_reslist(self):
        rmList =["jaVISA Test"]
        return rmList

    def jav_scpilist(self,SCPIList):
        ### Send SCPI list & Query if "?" 
        ### Collect read results into a list for return.
        OutList = []
        for cmd in SCPIList:
            if cmd.find('?') == -1:
                self.write(cmd)
            else:
                ReadStr = self.query(cmd)
                OutList.append(ReadStr)
        return OutList

    def query(self,cmd):
        return "<notRead>"

    def queryFloat(self,cmd):
        return -9999.9999

    def queryFloatArry(self,cmd):
        return [-9999.9999]

    def queryInt(self,cmd):
        return -9999

    def queryIntArry(self,cmd):
        return [-9999]

    def write(self,cmd):
        pass

if __name__ == "__main__":
    RS = jaVISA_mock()
    RS.jav_openvisa(f'TCPIP::192.168.1.100::200::SOCKET')    #Socket
    print(RS.query("*IDN?"))
    RS.jav_Close()