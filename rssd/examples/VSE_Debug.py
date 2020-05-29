##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Author: mclim
### Date:   2017.09.01
##########################################################
### User Entry
##########################################################
host = '127.0.0.1'                      #Get local machine name
port = 5025                             #Reserve a port for your service.

##########################################################
### Code Begin
##########################################################
import socket                           #Import socket module
import datetime.datetime as dt
s = socket.socket()                     #Create a socket object

def sInit():
    s.connect((host, port))
    s.settimeout(20)                    #Timeout in seconds

def sQuery(SCPI):
    s.sendall(SCPI + "\n")              #Write 'cmd'
    sOut = s.recv(1024).strip()         #Query socket
    return sOut

def sWrite(SCPI):
    s.sendall(SCPI + "\n")              #Write 'cmd'

def FileWrite(sOutput):
    sHostname = socket.gethostname()
    sDate = dt.now().strftime("%y%m%d,%H%M%S")
    f = open("00_Socket_Example.txt",'a+')
    f.write("%s,%s,%s\n"%(sDate,sHostname,sOutput))
    f.close()

##########################################################
### Main Code
##########################################################
sInit()
sWrite(":INST:SEL 'OFDM_CC1'")
print(sQuery(":FETC:SUMM:EVM?"))
sWrite(":INST:SEL 'OFDM_CC2'")
print(sQuery(":FETC:SUMM:EVM?"))
print(sQuery(":SYST:ERR?"))
s.close()
