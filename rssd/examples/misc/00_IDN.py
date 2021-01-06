##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Quick visa utility
### Requird: python -m pip install pyvisa
### Author:  Martin C Lim
### Date:    2017.08.01
### Description: Simple utility to:
###          1) Create socket connection
###          2) Create VISA connection
###          3) Query instrument for *IDN?
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
import time
import socket
import visa

##########################################################
### Function Definition
##########################################################
def FileWrite(sOutput):
    sHostname = socket.gethostname()
    sDate = time.strftime("%y%m%d,%H%M%S")
    f = open(savefile,'a+')
    f.write("%s,%s,%s\n"%(sDate,sHostname,sOutput))
    f.close()

def Socket_Query(IPAddr):
    try:
        s = socket.socket()
        s.settimeout(1.0)
        s.connect((IPAddr, 5025))
        SCPI = '*IDN?' + '\n'
        s.sendall(SCPI.encode())
        sRead = s.recv(1024).decode().strip()
        s.close()
    except:                                   #If error
        sRead = "###Socket Instrument not found###"
    print(IPAddr + ',' + sRead)
    FileWrite(IPAddr + ',' + sRead)

def VISA_Query(IPAddr):
    try:
        rm = visa.ResourceManager()
        rmlist = rm.list_resources()
        VISA1 = rm.open_resource('TCPIP0::'+ IPAddr +'::inst0::INSTR')
        sRead = VISA1.query('*IDN?').strip()
        VISA1.close()
    except:
        sRead = "###VISA Instrument not found###"
    print(IPAddr + ',' + sRead)
    FileWrite(IPAddr + ',' + sRead)

##########################################################
### Main Code
##########################################################
for IP in IPArry:
    Socket_Query(IP)
    VISA_Query(IP)
