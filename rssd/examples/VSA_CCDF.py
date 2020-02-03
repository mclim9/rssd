##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
###
##########################################################
### User Entry
##########################################################
FSW_IP  = '192.168.1.109'
Freq    = 28e9
RFBW    = 100e6
NumIQ   = 2e6
NumMeas = 10

##########################################################
### Code Overhead
##########################################################
from rssd.VSA.Common       import VSA        #pylint: disable=E0611,E0401
from datetime              import datetime
from rssd.FileIO           import FileIO     #pylint: disable=E0611,E0401

OFile = FileIO().makeFile(__file__)
FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

##########################################################
### Code Start
##########################################################
FSW.jav_Reset()
FSW.Set_Freq(Freq)
FSW.Init_CCDF()                       #FSW CCDF Channel
FSW.Set_CCDF_BW(RFBW)
FSW.Set_CCDF_Samples(NumIQ)
FSW.Set_SweepCont(0)

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Iter,CrestF,P10_00,P01_00,P00_10,P00_01,CmdTime')
sumTime = 0
for i in range(NumMeas):
   tick = datetime.now()
   FSW.Set_InitImm()
   ccdf = FSW.Get_CCDF()
   d = datetime.now() - tick
   sumTime += d.microseconds
   OutStr = f'{i},{ccdf},{d.seconds}.{d.microseconds}'
   OFile.write (OutStr)

##########################################################
### Cleanup Automation
##########################################################
FSW.jav_Close()
