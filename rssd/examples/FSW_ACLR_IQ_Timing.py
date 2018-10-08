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

FSW_IP   = '192.168.1.109'
MeasTim  = [0.1e-3, 0.2e-3, 0.3e-3, 0.5e-3, 1e-3, 2e-3, 3e-3]
RFBW     = 95e6
RFSp     = 100e6
Freq     = 28e9
NumIter  = 20
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
FSW.Init_IQ()                       #FSW ACLR Channel
if 1:
   FSW.Set_Freq(Freq)
   FSW.Set_IQ_BW(3.1*RFSp)
   FSW.Set_IQ_SpectrumWindow()
   FSW.Set_Trace_Detector('RMS',2)
   FSW.Set_Mkr_Freq(Freq,1,2)
   FSW.Set_Mkr_Band(RFBW,1,2)
   FSW.Set_Mkr_Freq(Freq-RFSp,2,2)
   FSW.Set_Mkr_Band(RFBW,2,2)
   FSW.Set_Mkr_Freq(Freq+RFSp,3,2)
   FSW.Set_Mkr_Band(RFBW,3,2)

FSW.Set_DisplayUpdate("OFF")
FSW.Set_SweepCont(0)
FSW.Set_InitImm()
if 1:
   FSW.Set_Trig1_Source('Ext')

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('ACLR,CapTime,Iter,CmdTime')
sumTime = 0
for mTime in MeasTim:
   FSW.Set_IQ_Time(mTime)
   FSW.Set_InitImm()
   for i in range(NumIter):
      tick = datetime.now()
      FSW.Set_InitImm()
      aclr = []
      for i in range(1,3+1):
         aclr = aclr + FSW.Get_Mkr_Band(i,2)
      d = datetime.now() - tick
      sumTime = sumTime + d.microseconds/1e6
      OutStr = '%s,%.6f,%d,%3d.%06d'%(aclr,mTime,i,d.seconds,d.microseconds)
      OFile.write (OutStr)
   print('%f'%(sumTime/NumIter))   
##########################################################
### Cleanup Automation
##########################################################
FSW.jav_Close()
