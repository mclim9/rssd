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
import os
BaseDir = os.path.dirname(os.path.realpath(__file__))
OutFile = BaseDir + '\\' +  __file__
print(OutFile)

FSW_IP  = '192.168.1.109'
MeasTim = 1e-3
Freq    = 28e9
##########################################################
### Code Overhead
##########################################################
from rssd.FSW_Common import VSA
from datetime        import datetime
import rssd.FileIO

f = rssd.FileIO.FileIO()
OFile = f.Init(OutFile)
FSW = VSA()                         #Create FSW Object
FSW.jav_Open(FSW_IP,f.sFName)       #Connect to FSW
if 0:
   SMW.jav_logSCPI()
   FSW.jav_logSCPI()
   
FSW.jav_Reset()
FSW.Set_Freq(Freq)
FSW.Init_ACLR()                       #FSW ACLR Channel
FSW.Set_Trace_Detector('RMS')
FSW.Set_ACLR_CHBW(95e6)
FSW.Set_ACLR_AdjBW(95e6)
FSW.Set_ACLR_AdjSpace(100e6)
#FSW.Set_ResBW(500e3)

#FSW.Set_DisplayUpdate("OFF")
FSW.Set_SweepCont(0)
FSW.Set_SweepTime(MeasTim)
FSW.Set_YIG('ON')
FSW.Set_InitImm()
if 1:
   FSW.Set_Trig1_Source('Ext')

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('ACLR,CapTime,Iter,CmdTime')
sumTime = 0
for i in range(20):
   tick = datetime.now()
   FSW.Set_InitImm()
   aclr = FSW.Get_ACLR()
   d = datetime.now() - tick
   sumTime += d.microseconds
   OutStr = '%s,%.6f,%d,%3d.%06d'%(aclr,MeasTim,i,d.seconds,d.microseconds)
   OFile.write (OutStr)

print('%f'%(sumTime/20))   
##########################################################
### Cleanup Automation
##########################################################
FSW.jav_Close()
