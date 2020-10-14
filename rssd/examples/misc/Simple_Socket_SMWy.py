""" Rohde & Schwarz Automation for demonstration use."""
#pylint: disable=invalid-name
##########################################################
### User Entry
##########################################################
import socket                       #Import socket module
host = '192.168.58.114'             #Instrument IP address
port = 5025                         #Instrument control port

##########################################################
### Code Begin
##########################################################
def sQuery(SCPI):
    """Socket Query"""
    out = SCPI + "\n"
    s.sendall(out.encode())         #Write 'cmd'
    sOut = s.recv(2048).strip()     #read socket
    return sOut.decode()

def sWrite(SCPI):
    """Socket Write"""
    out = SCPI + "\n"
    s.sendall(out.encode())         #Write 'cmd'

##########################################################
### Main Code
##########################################################
s = socket.socket()                 #Create a socket object
s.connect((host, port))
s.settimeout(1)                     #Timeout in seconds

sWrite(':SOURce1:BB:NR5G:SCHed:CELL0:SUBF0:USER0:BWPart0:ALLoc0:PUSCh:TXSCheme:CDMData 1')
print(sQuery(':SOURce1:BB:NR5G:SCHed:CELL0:SUBF0:USER0:BWPart0:ALLoc0:PUSCh:TXSCheme:CDMData?'))
sWrite(':SOURce1:BB:NR5G:SCHed:CELL0:SUBF0:USER0:BWPart0:ALLoc0:PUSCh:DMRS:POWer -10')
print(sQuery(':SOURce1:BB:NR5G:SCHed:CELL0:SUBF0:USER0:BWPart0:ALLoc0:PUSCh:DMRS:POWer?'))
