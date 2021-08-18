from datetime           import datetime
from rssd.VSE.Common    import VSE
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)
FSW = VSE().jav_Open('127.0.0.1',OFile)  #Create FSW Object

################################################################################
### Code Start
################################################################################
FSW.Init_IQ()                       #FSW IQ Channel
FSW.Set_DisplayUpdate("OFF")
FSW.Set_SweepCont(0)

OFile.write('Fs,CapTime,Iter,CmdTime')
for Fs in [491.52e6, 1351.68e6]:
    for measTime in [10e-3, 20e-3]:
        print(f'Fs:{Fs} Meas:{measTime}')
        FSW.Set_IQ_SamplingRate(Fs)
        FSW.Set_SweepTime(measTime)
        tick = datetime.now()
        FSW.Set_InitImm()
        FSW.Get_IQ_Data()
        d = datetime.now() - tick
        OutStr = f'{Fs/1e6},{measTime},{0:2d},{d.seconds:03d}.{d.microseconds:06d}'
        OFile.write(OutStr)

FSW.jav_Close()
