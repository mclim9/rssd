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
OutFile = BaseDir + __file__

SMW_IP  = '192.168.1.114'
FSW_IP  = '192.168.1.109'
VSE_IP  = '127.0.0.1'               #Get local machine name
FsArry  = [100e6, 115.2e6, 200e6, 400e6, 800e6, 1200e6, 1600e6, 2000e6] #Sampling Rate
MeasTim = 500e-6

##########################################################
### Code Overhead
##########################################################
from rssd.SMW_Common import VSG
from rssd.FSW_Common import VSA
from rssd.VSE_K96    import VSE
import rssd.FileIO
from datetime  import datetime

f = rssd.FileIO.FileIO()
OFile = f.Init(OutFile)
SMW = VSG()                         #Create SMW Object
FSW = VSA()                         #Create FSW Object
VSE = VSE()                         #Create VSE Object
SMW.jav_Open(SMW_IP,f.sFName)       #Connect to SMW
FSW.jav_Open(FSW_IP,f.sFName)       #Connect to FSW
VSE.jav_Open(VSE_IP,f.sFName)       #Connect to VSE
if 0:
   SMW.jav_logSCPI()
   FSW.jav_logSCPI()
   VSE.jav_logSCPI()
   
FSW.jav_Reset()
FSW.Init_IQ()                       #FSW IQ Channel
FSW.Set_DisplayUpdate("OFF")
FSW.Set_SweepTime(MeasTim)

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Fs,CapTime,Iter,CmdTime')
for Fs in FsArry:
   print("Starting Fs: %f"%Fs)
   FSW.Set_IQ_SamplingRate(Fs)
   for i in range(50):
      tick = datetime.now()
      FSW.Set_InitImm()
      FSW.Get_IQ_Data()
      d = datetime.now() - tick
      OutStr = '%f,%f,%d,%3d.%06d%3d.%06d'%(Fs/1e6,MeasTim,i,d.seconds,d.microseconds)
      OFile.write (OutStr)
   
##########################################################
### Cleanup Automation
##########################################################
SMW.jav_Close()
FSW.jav_Close()
VSE.jav_Close()
OFile.close()
