################################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
################################################################################
### User Entry
################################################################################
FSW_IP  = '192.168.1.109'
FsArry  = [400e6, 500e6, 600e6, 625e6, 650e6, 675e6, 700e6, 800e6, 900e6] #Sampling Rate
MeasTim = 123e-6
numRepeat   = 10

################################################################################
### Code Overhead: Import and create objects
################################################################################
from rssd.VSA.Common    import VSA
from rssd.FileIO        import FileIO
from datetime           import datetime

OFile = FileIO().makeFile(__file__)
FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

################################################################################
### Code Start
################################################################################
FSW.jav_Reset()
FSW.Init_IQ()                       #FSW IQ Channel
FSW.Set_DisplayUpdate("OFF")
FSW.Set_SweepTime(MeasTim)
FSW.Set_SweepCont(0)

################################################################################
### Measure Time
################################################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Fs,CapTime,Iter,CmdTime')
for Fs in FsArry:
    print("Starting Fs: %f"%Fs)
    FSW.Set_IQ_SamplingRate(Fs)
    for i in range(numRepeat):
        tick = datetime.now()
        FSW.Set_InitImm()
        FSW.Get_IQ_Data()
        data = FSW.Get_IQ_Data_Ascii2().split(',')[0:2]
        d = datetime.now() - tick
        OutStr = f'{Fs/1e6},{MeasTim},{i:2d},{d.seconds:03d}.{d.microseconds:06d}, {data}'
        OFile.write (OutStr)

################################################################################
### Cleanup Automation
################################################################################
FSW.jav_Close()