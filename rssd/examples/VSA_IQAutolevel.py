###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2020.04.20
###
###############################################################################
### User Entry
###############################################################################
VSA_IP  = '192.168.1.109'
VSG_IP  = '192.168.1.114'
MeasTim = 100e-6
Freq    = 6e9
Avg     = 0

### Loops
Repeat  = 1
PwrArry = range(-50,0,2)

###############################################################################
### Code Overhead
###############################################################################
import timeit
from rssd.VSA.WLAN_K91      import VSA              #pylint: disable=E0611,E0401
from rssd.VSG.WLAN_K54      import VSG              #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401

OFile = FileIO().makeFile(__file__)
VSA = VSA().jav_Open(VSA_IP,OFile)                  #Create VSA Object
VSG = VSG().jav_Open(VSG_IP,OFile)                  #Create VSG Object

###############################################################################
### Instrument Init
###############################################################################
#VSA.Set_DisplayUpdate("OFF")
VSA.Set_Param_Couple_All()
VSA.Set_In_YIG('OFF')
VSA.Set_Freq(Freq)

VSA.Init_IQ()                                       #FSW IQ Channel
VSA.Set_IQ_Time(MeasTim)

VSA.Init_WLAN()
VSA.Set_WLAN_Standard('AC')
VSA.Set_WLAN_ChBW(0)
VSA.Set_WLAN_CaptureTime(2e-3)

VSG.Set_Freq(Freq)

###############################################################################
### Measure Time
###############################################################################
LoopParam   = 'Iter,Pwr'
TimeParam   = 'AlTime,MeasTime,TotalTIme'
AmpParam    = VSA.Get_Params_Amp(1)
SysParam    = VSA.Get_Params_System(1)
MeasData    = VSA.Get_Params_WLAN_EVM(1)
OFile.write(f'{LoopParam},{TimeParam},{AmpParam},{SysParam},{MeasData}')

tick0 = timeit.default_timer()
for i in range(Repeat):
    for SMWPwr in PwrArry:
        ### <thing we are timing>
        VSG.Set_RFPwr(SMWPwr)
        tick = timeit.default_timer()

        ### <AUTOLEVEL> ###
        VSA.Get_ChannelName()
        Fs = VSA.Get_IQ_SamplingRate()
        VSA.Init_IQ()                                           #FSW IQ Channel
        VSA.Set_IQ_SamplingRate(Fs)
        VSA.Set_IQ_Time(MeasTim)
        VSA.Set_Autolevel()
        VSA.Set_ChannelSelect(VSA.CurrCh)
        tockA = timeit.default_timer()
        ### </AUTOLEVEL> ###

        VSA.write(':INIT:CONT OFF')                             # Single Sweep
        VSA.query(':INIT:IMM;*OPC?')                            # Take Sweep
        EVM         = VSA.Get_Params_WLAN_EVM()
        tockB       = timeit.default_timer()
        ### <\thing we are timing>

        ALTime      = tockA - tick
        TotTime     = tockB - tick
        TestTime    = TotTime - ALTime

        LoopParam   = f'{i},{SMWPwr:5.2f}'
        TotTime     = f'{ALTime:2,.6f},{TestTime:2,.6f},{TotTime:2,.6f}'
        AmpParam    = VSA.Get_Params_Amp()
        SysParam    = VSA.Get_Params_System()
        MeasData    = EVM
        OutStr      = f'{LoopParam},{TotTime},{AmpParam},{SysParam},{MeasData}'
        OFile.write (OutStr)

SuiteTime = timeit.default_timer() - tick0
print(f'Total Test time : {SuiteTime:2,.6f}')
print(f'Time/Measurement: {SuiteTime/(Repeat*len(PwrArry)):2,.6f}')

###############################################################################
### Cleanup Automation
###############################################################################
OFile.write("\n")
VSA.jav_Close()
