##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date    : 2018.05.24
##########################################################
### User Entry
##########################################################
SMW_IP  = '192.168.1.114'
FSW_IP  = '192.168.1.109'
VSE_IP  = '127.0.0.1'               #Get local machine name
Fs        = 1200e6                  #Sampling Rate
MeasTim = 500e-6

##########################################################
### Code Overhead: Import and create objects
##########################################################
from datetime           import datetime
from rssd.VSA.Common    import VSA
from rssd.SMW.Common    import VSG
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)
SMW = VSG().jav_Open(SMW_IP,OFile)  #Create SMW Object
FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

##########################################################
### Code Start
##########################################################
FSW.jav_Reset()
FSW.Init_IQ()                              #FSW IQ Channel
FSW.Set_DisplayUpdate("OFF")
FSW.Set_SweepTime(MeasTim)
FSW.Set_IQ_SamplingRate(Fs)

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Fs,CapTime,Iter,CmdTime')

for i in range(50):
    FSW.Set_InitImm()
    tick = datetime.now()
    ### <\thing we are timing>
    FSW.Get_IQ_Data('IQData%d'%i)
    ### <\thing we are timing>
    tock = datetime.now()
    OutStr = '%f,%f,%d,%s'%(Fs/1e6,MeasTim,i,tock-tick)
    OFile.write (OutStr)

##########################################################
### Cleanup Automation
##########################################################
SMW.jav_Close()
FSW.jav_Close()
OFile.close()
