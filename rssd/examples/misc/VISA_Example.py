##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Simple Instrument Socket Example
### Author:  mclim
### Date:    2017.09.01
##########################################################
### User Entry
##########################################################
host = '192.168.1.114'           #Instrument IP address

##########################################################
### Code Begin
##########################################################
import visa                      #Import VISA module
import xml.etree.ElementTree as ET  

def sQuery(SCPI):
   sOut = VISA1.query(SCPI)      #Write cmd
   return sOut.strip()

def sWrite(SCPI):
   VISA1.write(SCPI)             #Write cmd

def getSysInfo():
   xmlIn = sQuery("SYST:DFPR?")
   strStart = xmlIn.find('deviceId="') + len('deviceID="')
   strStop  = xmlIn.find('type="') - 2
   xmlIn = xmlIn[strStart:strStop]
   print(xmlIn)
   return xmlIn 

def getSysInfo2():
   xmlIn = sQuery("SYST:DFPR?")

   xmlIn = xmlIn[xmlIn.find('>')+1:]#Remove header
   root  = ET.fromstring(xmlIn)
   if 0:
      DData = root.find('DeviceData').items()
      devID = DData[0][1]
      dType = DData[1][1]
   devID = root[0].attrib['deviceId']
   dType = root[0].attrib['type']
   os    = root[2][1].attrib['name']
   osVer = root[2][1].attrib['version']
   print(os, osVer)
   print(dType, devID)
   
##########################################################
### Main Code
##########################################################
rm = visa.ResourceManager()
rmlist = rm.list_resources()
VISA1 = rm.open_resource('TCPIP0::'+ host +'::inst0::INSTR')

print("Info:" + sQuery("*IDN?"))
print("Opts:" + sQuery("*OPT?"))
getSysInfo2()

VISA1.close()
