'''RSSD instrument object'''
#pylint: disable=too-many-function-args
#pylint: disable=method-hidden,E0202

import time
import rssd.FileIO
# from rssd.test.yaVISA       import jaVISA_mock
# from rssd.RSI.time          import timer
from rssd.bus.socket        import jaSocket
from rssd.bus.VISA          import jaVisa
from rssd.bus.test          import jaTest

class instrument(object):
    '''Rohde & Schwarz Instrument Class'''
    def __init__(self):
        self.dataIDN   = ""         # Raw IDN String
        self.Make      = ""         # IDN Make
        self.Model     = ""         # IDN Model
        self.Device    = ""         # IDN Device
        self.Version   = ""         # IDN Version
        self.debug     = 1          # Print or not
        self.EOL       = '\r\n'
        self.f         = ''         # Log File Object
        self.dLastErr  = ''         # Last error
        self.bus       = 'Nobus'    # bus object
        self.connected = 0

    def delay(self,sec):
        '''delay in Sec'''
        time.sleep(sec)

    def SCPI_clear(self):
        '''Clear Errors'''
        self.bus.clear()

    def SCPI_close(self):
        '''Close bus Session'''
        try:
            errList = self.SCPI_ClrErr()
            self.bus.close()
            return errList
        except:
            pass

    def SCPI_clrErr(self):
        '''Read all SYST:ERR messages'''
        ErrList = []
        try:                                                        #Instr supports SYST:ERR?
            while True:
                RdStr = self.query("SYST:ERR?").strip()
                ErrList.append(RdStr)
                RdStrSplit = RdStr.split(',')
                if RdStr == "<notRead>" : break                     #No readstring
                if RdStrSplit[0] == "0" : break                     #Read 0 error:R&S
                if RdStrSplit[0] == "+0": break                     #Read 0 error:Other
                self.dLastErr = RdStr
                if self.debug: print("SCPI_ClrErr: %s-->%s"%(self.Model,RdStr))
        except:  #Instrument does not support SYST:ERR?
            if self.debug: print("SCPI_ClrErr: %s-->SYST:ERR not Supported"%(self.Model))
        return ErrList

    def SCPI_error(self):
        '''Read SYST:ERR?'''
        RdStr = self.query("SYST:ERR?").strip().split(',')
        return RdStr

    def SCPI_file_write(self, outstr):
        '''Write SCPI to file if f object exists'''
        if self.f != '':
            self.f.write(outstr.strip())

    def SCPI_IDN(self):
        '''query *IDN?  Assign data to properties'''
        self.dataIDN = "Temp"                                       #Temp for self.query
        self.dataIDN = self.query("*IDN?").strip()
        if self.dataIDN != "<notRead>":                             #Data Returned?
            IDNStr = self.dataIDN.split(',')
            try:
                self.Make       = IDNStr[0]
                self.Model      = IDNStr[1]
                self.Device     = IDNStr[2]
                self.Version    = IDNStr[3]
            except:
                pass
        else:
            self.dataIDN = ""                                       #Reset if not read
        return self.dataIDN

    def SCPI_logscpi(self):
        self.f = rssd.FileIO()                                      #pylint:disable=E1101
        DataFile = self.f.init("yaVISA")                            #pylint:disable=W0612

    def SCPI_read_OPC(self, InCMD):
        ''' Wait based on *OPC '''
        start_time = time.time()
        self.write("*ESE 1")                                        #Event Status Enable
        self.write("*SRE 32")                                       #ServiceReqEnable-Bit5:Std Event
        self.write(InCMD + ";*OPC")                                 #Initiate Read.  *OPC will trigger ESR
        #print ('    OPC Wait: ' +InCMD)
        read = 0
        while (read & 1) != 1:                                      #Loop until done
            try:
                read = self.queryInt("*ESR?")                       #Poll EventStatReg-Bit0:Op Complete  (STB?)
            except:
                if self.debug: print("SCPI_OPCWai:*ESR? Error")
            time.sleep(0.5)
            delta = (time.time() - start_time)
            if delta > 300:
                if self.debug: print("SCPI_OPCWai: timeout")
                break
        if self.debug: print('SCPI_OPCWai: %0.2fsec'%(delta))
        self.SCPI_ClrErr()
        return delta

    def open(self, address, type = 'socket', param = 5025):         #pylint: disable=redefined-builtin
        '''Open bus Sesion.  Return bus object'''
        if type == 'socket':
            self.bus = jaSocket.open(address)
        elif type == 'visa-socket':
            self.bus = jaVisa.open(f'TCPIP0::{address}::{param}::SOCKET')
        elif type == 'vxi11':
            self.bus = jaVisa.open(f'TCPIP0::{address}::instr0::INSTR')
        elif type == 'hislip':
            self.bus = jaVisa.open(f'TCPIP0::{address}::hislip0::INSTR')
        elif type == 'test':
            self.debug = 0
            self.connected      = 1
            if self.bus == 'Nobus':
                self.bus = jaTest.open('test')
            self.SCPI_ClrErr()
            self.dLastErr = ""
        self.SCPI_IDN()
        self.SCPI_file_write(self.dataIDN)
        self.SCPI_ClrErr()
        return self

    def SCPI_read_raw(self):
        '''read raw data from bus'''
        return self.bus.read_raw()

    def SCPI_reset(self):
        '''reset instrument'''
        self.write("*RST;*CLS;*WAI")

    def SCPI_read_wait(self, InCMD):
        '''Brute Force Wait and check *OPC? '''
        start_time = time.time()
        self.write(InCMD)                                           #Initiate busand
        read = "0"
        while (int(read) & 1) != 1:                                 #Loop until done
            try:
                read = self.queryInt("*OPC?")                       #See if we can get *OPC?
            except:
                pass
            time.sleep(2)
            delta = (time.time() - start_time)
            if delta > 300:
                if self.debug: print("SCPI_Wai   : timeout")
                break
        if self.debug: print('SCPI_Wai   : %0.2fsec'%(delta))
        return delta


    def query(self,cmd):
        read ="<notRead>"
        try:
            if self.dataIDN != "":
                read = self.bus.query(cmd).strip()                   #Write if connected
        except:
            if self.debug: print("SCPI_RdErr : %s-->%s"%(self.Model,cmd))
        self.SCPI_file_write(self.f, "%s,%s,%s"%(self.Model,cmd,read))
        return read

    def queryFloat(self,cmd):
        try:
            strArry = self.query(cmd).split(',')
            return [float(i) for i in strArry][0]
        except:
            return -9999.9999

    def queryFloatArry(self,cmd):
        try:
            strArry = self.query(cmd).split(',')
            return [float(i) for i in strArry]
        except:
            return [-9999.9999, -888.888, -777.777, -666.666, -555.555, -444.444]

    def queryInt(self,cmd):
        try:
            strArry = self.query(cmd).split(',')
            return int([float(i) for i in strArry][0])
            # Float for scientific 'e' notation
        except:
            return -9999

    def queryIntArry(self,cmd):
        try:
            strArry = self.query(cmd).split(',')
            return [int(i) for i in strArry]
        except:
            return [-9999,-8888,-7777]

    def write(self,cmd):
        try:
            if self.dataIDN != "": self.bus.write(cmd)               #Write if connected
        except:
            if self.debug: print("SCPI_WrtErr: %s-->%s"%(self.Model,cmd))
        self.SCPI_file_write(self.f, "%s,%s"%(self.Model,cmd))      

    def write_raw(self,SCPI):
        self.bus.write_raw(SCPI)

    def write_scpilist(self,SCPIList):
        '''Send SCPI list & Query if "?" '''
        ### Collect read results into a list for return.
        OutList = []
        for cmd in SCPIList:
            if cmd.find('?') == -1:
                self.write(cmd)
            else:
                ReadStr = self.query(cmd)
                OutList.append(ReadStr)
        return OutList

if __name__ == "__main__":
    RS = instrument().open('10.0.0.10')                 #Default HiSlip
    RS.debug    = 1
    rdStr = RS.query('*IDN?')
    print(rdStr)
    RS.SCPI_Close()
