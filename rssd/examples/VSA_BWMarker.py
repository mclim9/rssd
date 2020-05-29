################################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Bandwidth Marker Test
### Author : mclim
### Date   : 2020.02.03
################################################################################
### User Entry
################################################################################
VSA_IP  = '192.168.1.109'
Freq    = 9e9
Span    = 110e6
Avg     = 5

### Loops
Repeat  = 1
swpTimeArry = [2e-3, 3e-3, 5e-3, 1e-2, 2e-2, 3e-2, 5e-2, 1e-1, 2e-1, 3e-1, 5e-1]
rbwArry = [1e3, 3e3, 5e3, 1e4, 3e4, 5e4, 1e5, 3e5, 5e5, 1e6]

################################################################################
### Code Overhead
################################################################################
import timeit
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401

OFile = FileIO().makeFile(__file__)
VSA = VSA().jav_Open(VSA_IP,OFile)                  #Create VSA Object

################################################################################
### Code Start
################################################################################
# VSA.jav_Reset()
VSA.Set_Freq(Freq)
# VSA.Set_Trace_Avg('POW')
# VSA.Set_Trace_AvgCount(Avg)
VSA.Set_Trace_Mode('WRIT')
VSA.Set_Trace_Detector('RMS')
VSA.Set_Span(Span)
VSA.Set_Mkr_Freq(Freq)
VSA.Set_Mkr_Band(100e6)
VSA.Set_YIG('OFF')
VSA.Set_SweepCont(0)
# VSA.Set_Trig1_Source('Ext')

################################################################################
### Measure Time
################################################################################
#sDate = timeit.default_timer().strftime("%y%m%d-%H:%M:%S.%f") #Date String
LoopParam   = 'Iter,RBW,SwpTime'
SwpParam    = VSA.Get_SweepParams(1)
AmpParam    = VSA.Get_AmpParams(1)
TrcParam    = VSA.Get_TraceParams(1)
SysParam    = VSA.Get_System_Params(1)
MeasData    = 'MkrFreq,MkrBndPwr'
OFile.write(f'{LoopParam},TotalTime,{AmpParam},{SwpParam},{TrcParam},{SysParam},{MeasData}')

for i in range(Repeat):
    for SwpTime in swpTimeArry:
        for rbw in rbwArry:
            tick = timeit.default_timer()
            ### <\thing we are timing>
            VSA.Set_Channel('Spectrum')
            VSA.Set_ResBW(rbw)
            VSA.Set_SweepTime(0)
            VSA.query(':INIT:IMM;*OPC?')                            # Take Sweep
            BndMkr = VSA.Get_Mkr_Band()
            ### <\thing we are timing>
            tock        = timeit.default_timer()
            LoopParam   = f'{i},{rbw:8.0f},{SwpTime:5.3f}'
            SwpParam    = VSA.Get_SweepParams()
            AmpParam    = VSA.Get_AmpParams()
            TrcParam    = VSA.Get_TraceParams()
            SysParam    = VSA.Get_System_Params()
            TotTime     = f'{(tock-tick):2,.6f}'
            MeasData    = f'{BndMkr[0]:.0f},{BndMkr[1]:.3f}'
            OutStr      = f'{LoopParam},{TotTime},{AmpParam},{SwpParam},{TrcParam},{SysParam},{MeasData}'
            OFile.write (OutStr)

################################################################################
### Cleanup Automation
################################################################################
OFile.write("\n")
VSA.jav_Close()
