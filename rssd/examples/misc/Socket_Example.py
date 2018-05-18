##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Simple Instrument Socket Example
### Author:  mclim
### Date:    2017.09.01
##########################################################
### User Entry
##########################################################
host = '192.168.1.109'           #Get local machine name
port = 5025                      #Reserve a port for your service.

##########################################################
### Code Begin
##########################################################
import socket                    #Import socket module
s = socket.socket()              #Create a socket object

def sInit():
   s.connect((host, port))
   s.settimeout(20)              #Timeout in seconds  

def sQuery(SCPI):
   s.sendall(SCPI + "\n")        #Write 'cmd'
   sOut = s.recv(1024).strip()   #Query socket
   return sOut

def sWrite(SCPI):
   s.sendall(SCPI + "\n")        #Write 'cmd'

def FileWrite(sOutput):
   sHostname = socket.gethostname()
   sDate = datetime.now().strftime("%y%m%d,%H%M%S")
   f = open("00_Socket_Example.txt",'a+')
   f.write("%s,%s,%s\n"%(sDate,sHostname,sOutput))
   f.close()

##########################################################
### Main Code
##########################################################
sInit()    
print(sQuery("*IDN?"))
sWrite("MMEM:LOAD:DEM 'C:\R_S\Instr\Debug\Allocation_V3.10_17.11.17.198\TwoBWP_AllMods.allocation'")
