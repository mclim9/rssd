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
port = 5025                      #Instrument control port

##########################################################
### Code Begin
##########################################################
import socket                    #Import socket module
import xml.etree.ElementTree as ET 

def sQuery(SCPI):
   out = SCPI + "\n"
   s.sendall(out.encode())       #Write 'cmd'
   sOut = s.recv(2048).strip()   #read socket
   return sOut.decode()

def sWrite(SCPI):
   out = SCPI + "\n"
   s.sendall(out.encode())       #Write 'cmd'

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
s = socket.socket()              #Create a socket object
s.connect((host, port))
s.settimeout(1)                  #Timeout in seconds  

print("Info:" + sQuery("*IDN?"))
print("Opts:" + sQuery("*OPT?"))
getSysInfo()
