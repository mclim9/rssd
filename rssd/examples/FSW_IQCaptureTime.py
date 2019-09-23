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
FSW_IP  = '192.168.1.109'
FsArry  = [100e6, 115.2e6, 200e6, 400e6, 800e6, 1200e6, 1600e6, 2000e6] #Sampling Rate
MeasTim = 500e-6


##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.VSA.Common    import VSA
from rssd.FileIO        import FileIO
from datetime          import datetime

OFile = FileIO().makeFile(__file__)
FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

##########################################################
### Code Start
##########################################################
FSW.jav_Reset()
FSW.Init_IQ()                       #FSW IQ Channel
FSW.Set_DisplayUpdate("OFF")
FSW.Set_SweepTime(MeasTim)
FSW.Set_SweepCont(0)

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
      OutStr = '%f,%f,%d,%3d.%06d'%(Fs/1e6,MeasTim,i,d.seconds,d.microseconds)
      OFile.write (OutStr)
   
##########################################################
### Cleanup Automation
##########################################################
FSW.jav_Close()
OFile.close()
