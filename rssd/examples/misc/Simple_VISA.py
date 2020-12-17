'''Rohde & Schwarz Automation for demonstration use.'''
#pylint: disable=invalid-name, unused-import, using-constant-test
import xml.etree.ElementTree as ET
import pyvisa                               #Import VISA module

###############################################################################
### Code Begin
###############################################################################
def vQuery(SCPI):
    '''VISA query'''
    VISA1.read_termination = '\n'           # 0x0A for socket
    vOut = VISA1.query(SCPI)                #Query cmd
    return vOut.strip()

def vWrite(SCPI):
    '''VISA write'''
    VISA1.write(SCPI)                       #Write cmd

def getSysInfo():
    '''Get System Info'''
    xmlIn = vQuery("SYST:DFPR?")

    xmlIn = xmlIn[xmlIn.find('>')+1:]       #Remove header
    root  = ET.fromstring(xmlIn)
    if 0:
        DData = root.find('DeviceData').items()
        devID = DData[0][1]
        dType = DData[1][1]
    devID = root[0].attrib['deviceId']
    dType = root[0].attrib['type']
    # os     = root[2][1].attrib['name']
    # osVer = root[2][1].attrib['version']
    # print(os, osVer)
    print(dType, devID)

###############################################################################
### Main Code
###############################################################################
rm = pyvisa.ResourceManager()
rmlist = rm.list_resources()
# VISA1 = rm.open_resource('TCPIP0::172.20.16.253::5025::SOCKET')
VISA1 = rm.open_resource('TCPIP0::172.20.16.253::inst0::INSTR')

print("Info:" + vQuery("*IDN?"))
vWrite("CALC2:CHAN1:AVER:STAT 1")
print("Opts:" + vQuery("CALC2:CHAN1:AVER:STAT?"))
vWrite('CALC2:CHAN1:AVER:COUN 20000')
print("Opts:" + vQuery("CALC2:CHAN1:AVER:COUN?"))
# print("Opts:" + vQuery("CALC2:CHAN1:TRAC:AVER:STAT?"))
# getSysInfo()

VISA1.close()
