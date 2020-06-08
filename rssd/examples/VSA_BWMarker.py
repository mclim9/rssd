################################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Bandwidth Marker Test
################################################################################
### User Entry
################################################################################
FSW_IP  = '192.168.1.109'
Freq    = 9e9
Span    = 110e6
Avg     = 5

### Loops
Repeat  = 1
swpTimeArry = [2e-3, 3e-3, 5e-3, 1e-2, 2e-2, 3e-2, 5e-2, 1e-1, 2e-1, 3e-1, 5e-1]
rbwArry = [1e3, 3e3, 5e3, 1e4, 3e4, 5e4, 1e5, 3e5, 5e5, 1e6]
# rbwArry = [0]

################################################################################
### Code Overhead
################################################################################
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401
from rssd.RSI.time          import timer

OFile = FileIO().makeFile(__file__)
FSW = VSA().jav_Open(FSW_IP,OFile)                  #Create FSW Object
TMR = timer()

################################################################################
### Code Start
################################################################################
# FSW.jav_Reset()
FSW.Set_Freq(Freq)
# FSW.Set_Trace_Avg('POW')
# FSW.Set_Trace_AvgCount(Avg)
FSW.Set_Trace_Mode('WRIT')
FSW.Set_Trace_Detector('RMS')
FSW.Set_Span(Span)
FSW.Set_Mkr_Freq(Freq)
FSW.Set_Mkr_Band(100e6)
FSW.Set_YIG('OFF')
FSW.Set_SweepCont(0)
# FSW.Set_Trig1_Source('Ext')

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
            FSW.Set_SweepTime(0)
            FSW.Set_InitImm()                           # Take Sweep
            MeasData    = FSW.Get_Params_MkrBand()
            TMR.tick()                                  # <\thing we are timing>
            LoopParam   = f'{i},{rbw:8.0f},{SwpTime:5.3f}'
            TotTime     = TMR.Get_Params_Time()
            OutStr      = f'{LoopParam},{FSW.Get_Params(1,1,1,1,0)},{MeasData},{TotTime}'
            OFile.write (OutStr)

################################################################################
### Cleanup Automation
################################################################################
OFile.write("\n")
FSW.jav_Close()
