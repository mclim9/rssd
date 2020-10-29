"""Rohde & Schwarz Automation for demonstration use. """
#pylint: disable=invalid-name

import socket                                           #Import socket module
import xml.etree.ElementTree as ET
host = '192.168.1.109'                                  #Instrument IP address

###############################################################################
### Code Begin
###############################################################################

def sQuery(SCPI):
    '''socket query'''
    out = SCPI + "\n"
    s.sendall(out.encode())                             #Write 'cmd'
    sOut = s.recv(2048).strip()                         #read socket
    return sOut.decode()

def sWrite(SCPI):
    '''socket write'''
    out = SCPI + "\n"
    s.sendall(out.encode())                             #Write 'cmd'

def getSysInfo():
    '''get system options'''
    xmlIn = sQuery("SYST:DFPR?")
    strStart = xmlIn.find('deviceId="') + len('deviceID="')
    strStop  = xmlIn.find('type="') - 2
    xmlIn = xmlIn[strStart:strStop]                     #Remove header
    print(xmlIn)
    return xmlIn

###############################################################################
### Main Code
###############################################################################
s = socket.socket()                                     # Create a socket object
s.connect((host, 5025))
s.settimeout(1)                                         # Timeout in seconds

print("Info:" + sQuery("*IDN?"))
print("Opts:" + sQuery("*OPT?"))
getSysInfo()
