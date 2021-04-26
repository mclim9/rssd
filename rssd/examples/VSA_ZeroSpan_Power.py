"""Zero Span Measurement"""
FSW_IP  = '192.168.58.109'
Freq    = 8.6e9
Span    = 0
Avg     = 5

### Loops
Repeat  = 1
swpTimeArry = [2e-3, 3e-3, 5e-3, 1e-2, 2e-2, 3e-2, 5e-2, 1e-1, 2e-1, 3e-1, 5e-1]
rbwArry = [200e3]

################################################################################
### Code Overhead
################################################################################
from rssd.VSA.Common        import VSA
from rssd.FileIO            import FileIO
from rssd.RSI.time          import timer

OFile = FileIO().makeFile(__file__)
FSW = VSA().jav_Open(FSW_IP,OFile)                  #Create FSW Object
TMR = timer()

################################################################################
### Code Start
################################################################################
FSW.Set_Freq(Freq)
FSW.Set_Trace_Mode('WRIT')
FSW.Set_Trace_Detector('RMS')
FSW.Set_Span(Span)
FSW.Set_Mkr_Freq(Freq)
FSW.Set_In_YIG('OFF')
FSW.Set_SweepCont(0)
FSW.Set_Autolevel()

################################################################################
### Measure Time
################################################################################
#sDate = timeit.default_timer().strftime("%y%m%d-%H:%M:%S.%f") #Date String
LoopParam   = 'Iter,RBW,SwpTime'
OFile.write(f'{LoopParam},{FSW.Get_Params(1,1,1,1,1)},{FSW.Get_Params_MkrBand(1)},{TMR.Get_Params_Time(1)}')

for i in range(Repeat):
    for SwpTime in swpTimeArry:
        for rbw in rbwArry:
            TMR.start()                                 # <thing we are timing>
            FSW.Set_Channel('Spectrum')
            FSW.Set_ResBW(rbw)
            FSW.Set_SweepTime(SwpTime)
            FSW.Set_InitImm()                           # Take Sweep
            MeasData    = FSW.Get_Params_Mkr()
            TMR.tick()                                  # <\thing we are timing>
            LoopParam   = f'{i},{rbw:8.0f},{SwpTime:5.3f}'
            TotTime     = TMR.Get_Params_Time()
            OutStr      = f'{LoopParam},{FSW.Get_Params(1,1,1,1,0)},{MeasData},{TotTime}'
            OFile.write(OutStr)

################################################################################
### Cleanup Automation
################################################################################
OFile.write("\n")
FSW.jav_Close()
