"""Rohde & Schwarz Automation for demonstration use. """
#pylint: disable=invalid-name, unused-import
import os
import socket                                       #Import socket module
import logging
import xml.etree.ElementTree as ET
host = '10.0.0.16'                                  #Instrument IP address

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

def readSCPI():
    '''read SCPI array from file'''
    SCPIFile = os.path.splitext(__file__)[0] + '.txt'
    SCPIOut = []
    with open(SCPIFile, 'r') as csv_file:
        fileData = csv_file.readlines()
        for line in fileData:
            if line[0] != "#":                          # Remove Comments
                SCPIOut.append(line)
    return SCPIOut

def sendSCPI(SCPIarry):
    '''send SCPI array.  Check error after each cmd'''
    for cmd in SCPIarry:
        try:
            if '?' in cmd:

                sQuery(cmd)
            else:
                sWrite(cmd)
            error = sQuery('SYST:ERR?')
            outStr = f'{error.strip()} {cmd.strip()}'
            logging.info(outStr)
        except socket.timeout:
            error = 'SCPI TIMEOUT' + sQuery('SYST:ERR?')
            outStr = f'{error.strip()} {cmd.strip()}'
            logging.error(outStr)

###############################################################################
### Main Code
###############################################################################
s = socket.socket()                                     # Create a socket object
s.connect((host, 5025))
s.settimeout(5)                                         # Timeout in seconds
logging.basicConfig(level=logging.DEBUG, \
    filename=os.path.splitext(__file__)[0] + '.log', filemode='w', \
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
arry = readSCPI()
sendSCPI(arry)
