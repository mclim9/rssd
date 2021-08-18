"""Rohde & Schwarz Automation for demonstration use. """
#pylint: disable=invalid-name

import socket                                           # Import socket module
# import xml.etree.ElementTree as ET

def sWrite(SCPI):
    """Socket Write"""
    print(f'Write: {SCPI}')
    s.sendall(f'{SCPI}\n'.encode())                     # Write SCPI

def sQuery(SCPI):
    """Socket Query"""
    sWrite(SCPI)
    sOut = s.recv(2048).strip().decode()                # Read socket
    print(f'Query: {sOut}')
    return sOut

def getSysInfo():
    '''get system options'''
    xmlIn = sQuery("SYST:DFPR?")
    strStart = xmlIn.find('deviceId="') + len('deviceID="')
    strStop  = xmlIn.find('type="') - 2
    xmlIn = xmlIn[strStart:strStop]                     # Remove header
    print(xmlIn)
    return xmlIn

###############################################################################
### Main Code
###############################################################################
s = socket.socket()                                     # Create a socket object
s.connect(('192.168.58.30', 5025))
s.settimeout(1)                                         # Timeout in seconds

print("Info:" + sQuery("*IDN?"))
print("Opts:" + sQuery("*OPT?"))
# getSysInfo()
