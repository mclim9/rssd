'''RSSD Socket Bus Class'''
# pylint: disable=E0611,E0401,E0202
# pylint: disable=signature-differs
import os
import socket
import logging
from rssd.bus.bus import bus

class jaSocket(bus):
    """Rohde & Schwarz VISA Class"""
    def __init__(self):
        self.EOL        = '\n'              # \n or \r\n
        self.K2         = 'NoVISA'
        logging.basicConfig(level=logging.INFO, \
                            filename=os.path.splitext(__file__)[0] + '.log', filemode='w', \
                            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    def close(self):
        """Close K2 Session"""
        try:
            self.K2.close()
        except:
            pass

    def open(self, resourceID, param):
        '''
        Open raw socket Connection
        resourceID  = IPaddress(string)
        param       = port number
        '''
        self.K2 = socket.socket()
        self.ResID = resourceID
        try:
            self.K2.settimeout(1)
            self.K2.connect((resourceID,param))
        except:
            logging.error(f'jaS_OpnErr: {self.ResID}')
            self.K2 = 'NoSOCKET'
        return self

    def query(self, SCPIstr):
        read ="<notRead>"
        try:
            cmd = SCPIstr + self.EOL
            self.K2.sendall(cmd.encode())               # Write if connected
            sOut = self.K2.recv(10000).strip()          # read socket
            read = sOut.decode()
        except:
            logging.error(f'jaS_RdErr : {self.ResID}-->{SCPIstr}')
        return read

    def timeout(self, seconds):
        self.K2.settimeout(seconds)

    def read_raw(self):
        """Read binary values from instrument"""
        sOut = self.K2.recv(10000).strip()              # read socket
        return sOut

    def write(self, SCPIstr):
        try:
            out = SCPIstr + self.EOL
            self.K2.sendall(out.encode())               #Write if connected
        except:
            logging.error(f'jaS_WrtErr: {self.ResID}-->{SCPIstr}')

    def write_raw(self, SCPIstr):
        self.write(SCPIstr)

if __name__ == "__main__":
    RS = jaSocket().open("192.168.58.115",5025)
    print(RS.query("*IDN?"))
    RS.close()
