##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
### Steps  : 
###
##########################################################
### User Entry
##########################################################
instru_ip  = '192.168.1.114'

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.yaVISA_socket import jaVisa
from rssd.FileIO        import FileIO
from datetime           import datetime

OFile = FileIO().makeFile(__file__)
#instr = jaVisa().jav_openvisa(f'TCPIP0::{instru_ip}::inst0',OFile)  #Create VISA Object
instr = jaVisa().jav_Open(instru_ip,OFile)            #Create Object

##########################################################
### Code Start
##########################################################   
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Iter,CmdTime,Response')

for i in range(10):
   tick = datetime.now()
   ### <\thing we are timing>
   rdStr = instr.query('*IDN?')
   ### <\thing we are timing>
   tock = datetime.now()
   ALTime = tock - tick
   OutStr = f'{i},{ALTime.seconds:3d}.{ALTime.microseconds:06d},{rdStr}'
   OFile.write (OutStr)
   
##########################################################
### Cleanup Automation
##########################################################
instr.jav_Close()
