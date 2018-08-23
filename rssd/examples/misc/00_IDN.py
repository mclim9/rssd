##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Quick visa utility
### Requird: python -m pip install pyvisa
### Author:  Martin C Lim
### Date:    2017.08.01
### Description: Simple utility to:
###         1) Create socket connection
###         2) Create VISA connection
###         3) Query instrument for *IDN?
##########################################################
### User Entry
##########################################################
savefile = '00_IDN.txt'
IPArry = ['192.168.1.109',   #FSW
          '192.168.1.114',   #SMW
          '192.168.1.115',   #SMB
          '192.168.1.130',   #SMA
          '192.168.1.30',    #ZVA
          '192.168.1.40',    #ZVA
          '192.168.1.150',   #OSP
          '192.168.1.140']   #RTO

##########################################################
### Code Begin
##########################################################
import visa
import time
import socket

##########################################################
### Function Definition
##########################################################
def FileWrite(sOutput):
    sHostname = socket.gethostname()
    sDate = time.strftime("%y%m%d,%H%M%S")
    f = open(savefile,'a+')
    f.write("%s,%s,%s\n"%(sDate,sHostname,sOutput))
    f.close()
   
def Socket_IDN(IPAddr):
    s = socket.socket()
    s.settimeout(1.0)
    s.connect((IPAddr, 5025))
    s.sendall('*IDN?\n')
    data = s.recv(1024).strip()
    IDN = IPAddr + "," + data
    s.close
    print(IDN)
    FileWrite(IDN)
    
def VISA_IDN(IPAddr):
    rm = visa.ResourceManager()
    rmlist = rm.list_resources()
    try:
        VISA1 = rm.open_resource('TCPIP0::'+ IPAddr +'::inst0::INSTR')
        data = VISA1.query('*IDN?').strip()
        IDN = IPAddr + "," + data
        VISA1.close()
    except:
        IDN = IPAddr + ",###Instrument not found###"
    print(IDN)
    FileWrite(IDN)

##########################################################
### Main Code
##########################################################
for IP in IPArry:
   Socket_IDN(IP)
   VISA_IDN(IP)




