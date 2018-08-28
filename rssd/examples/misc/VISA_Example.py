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

def sQuery(SCPI):
   sOut = VISA1.query(SCPI)      #Write cmd
   return sOut

def sWrite(SCPI):
   VISA1.write(SCPI)             #Write cmd

##########################################################
### Main Code
##########################################################
rm = visa.ResourceManager()
rmlist = rm.list_resources()
VISA1 = rm.open_resource('TCPIP0::'+ host +'::inst0::INSTR')

print("Info:" + sQuery("*IDN?"))
print("Opts:" + sQuery("*OPT?"))
print("XML :%s"%(sQuery("SYST:DFPR?")))

VISA1.close()
