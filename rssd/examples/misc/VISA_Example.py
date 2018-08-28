##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Simple Instrument Socket Example
### Author:  mclim
### Date:    2017.09.01
##########################################################
### User Entry
##########################################################
host = '192.168.1.109'           #Instrument IP address

##########################################################
### Code Begin
##########################################################
import visa                      #Import VISA module

def sQuery(SCPI):
   sOut = VISA1.query(SCPI)      #Write cmd
   return sOut.strip()

def sWrite(SCPI):
   VISA1.write(SCPI)             #Write cmd

def getSysInfo():
   xmlIn = sQuery("SYST:DFPR?")
   strStart = xmlIn.find('deviceId="') + len('deviceID="')
   strStop  = xmlIn.find('type="') - 2
   xmlIn = xmlIn[strStart:strStop]#Remove header
   print(xmlIn)
   return xmlIn

##########################################################
### Main Code
##########################################################
rm = visa.ResourceManager()
rmlist = rm.list_resources()
VISA1 = rm.open_resource('TCPIP0::'+ host +'::inst0::INSTR')

print("Info:" + sQuery("*IDN?"))
print("Opts:" + sQuery("*OPT?"))
getSysInfo()

VISA1.close()
