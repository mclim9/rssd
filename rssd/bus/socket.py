# -*- coding: future_fstrings -*-
# pylint: disable=E0611,E0401,E0202
'''RSSD Socket Bus Class'''

import socket
from rssd.bus.bus import bus

class jaSocket(bus):
    """Rohde & Schwarz VISA Class"""
    def __init__(self):
        self.EOL        = '\n'
        self.K2         = 'NoVISA'

    def Close(self):
        """Close K2 Session"""
        try:
            errList = self.jav_ClrErr()
            self.K2.close()
            return errList
        except:
            pass

    def open(self, sIPAddr, port):
        #*****************************************************************
        #*** Open raw socket Connection
        #*****************************************************************
        self.K2 = socket.socket()
        try:
            self.K2.settimeout(1)
            self.K2.connect((sIPAddr,port))
            self.jav_IDN()
            self.jav_fileout(self.dataIDN)
            self.jav_ClrErr()
        except:
            if self.debug: print ('jav_OpnErr: ' + sIPAddr)
            self.K2 = 'NoSOCKET'
        return self

    def jav_Open_Basic(self, sIPAddr,fily='',port=5025):
        """ Open raw socket Connection
            No IDN or Error checking"""
        self.K2 = socket.socket()
        try:
            self.K2.settimeout(1)
            self.K2.connect((sIPAddr,port))
            self.dataIDN = 'jav_Open_Basic'
            self.jav_fileout(fily, self.dataIDN)
        except:
            if self.debug: print ('jav_OpnErr: ' + sIPAddr)
            self.K2 = 'NoSOCKET'
        return self

    def query(self, SCPIstr):
        read ="<notRead>"
        try:
            if self.dataIDN != "":
                cmd = SCPIstr + '\n'
                self.K2.sendall(cmd.encode())               #Write if connected
                sOut = self.K2.recv(10000).strip()           #read socket
                read = sOut.decode()
        except:
            if self.debug: print("jav_RdErr : %s-->%s"%(self.Model,cmd))
        self.jav_fileout(self.f, "%s,%s,%s"%(self.Model,cmd,read))
        return read

    def read_raw(self):
        # return self.K2.read()
        print('jav_read_raw socket not supported')
        return 9999

    def write(self, SCPIstr):
        try:
            out = SCPIstr + self.EOL
            if self.dataIDN != "": self.K2.sendall(out.encode()) #Write if connected
        except:
            if self.debug: print("jav_WrtErr: %s-->%s"%(self.Model, SCPIstr))
        self.jav_fileout(self.f, "%s,%s"%(self.Model, SCPIstr))

    def write_raw(self, SCPIstr):
        self.K2.write(SCPIstr)

if __name__ == "__main__":
    RS = jaSocket().Open("192.168.1.160",5025)
    RS.EOL = '\r\n'
    print(RS.query("*IDN?"))
    RS.jav_Close()
