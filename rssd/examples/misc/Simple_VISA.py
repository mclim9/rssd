##########################################################
### Rohde & Schwarz Automation for demonstration use.
##########################################################
host = '192.168.1.114'           #Instrument IP address

##########################################################
### Code Begin
##########################################################
import visa                      #Import VISA module
import xml.etree.ElementTree as ET  

def vQuery(SCPI):
   vOut = VISA1.query(SCPI)      #Query cmd
   return vOut.strip()

def vWrite(SCPI):
   VISA1.write(SCPI)             #Write cmd

def getSysInfo2():
   xmlIn = vQuery("SYST:DFPR?")

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

print("Info:" + vQuery("*IDN?"))
print("Opts:" + vQuery("*OPT?"))

VISA1.close()
