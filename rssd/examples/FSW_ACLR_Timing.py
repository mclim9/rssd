##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date    : 2018.05.24
### Steps  : 
###
##########################################################
### User Entry
##########################################################
VSA_IP  = '192.168.1.108'
VSG_IP  = '192.168.1.114' 
MeasTim = 10e-3
Freq    = 2.3e9
RBW     = 20e3
ChBW    = 18e6
ChSpace = 20e6
Avg     = 0
SweMode = 'AUTO'            #AUTO | SPEed | DYN
SweType = 'AUTO'           #AUTO | SWE | FFT

### Loops
Repeat  = 1
PwrSweep = 59

##########################################################
### Code Overhead
##########################################################
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401
from rssd.yaVISA_socket     import jaVisa           #pylint: disable=E0611,E0401
from datetime               import datetime
from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401
import rssd.VSA_Leveling    as VSAL                 # pylint: disable=E0611,E0401
import timeit

OFile = FileIO().makeFile(__file__)
VSA = VSA().jav_Open(VSA_IP,OFile)                  #Create VSA Object
VSG = jaVisa().jav_Open(VSG_IP,OFile)               #Create Object
##########################################################
### Code Start
##########################################################
# VSA.jav_Reset()
VSA.Set_Freq(Freq)
VSA.Set_Param_Couple_All()
VSA.Init_ACLR()                                     #VSA ACLR Channel
VSA.Set_ACLR_CHBW(ChBW)
VSA.Set_ACLR_AdjBW(ChBW)
VSA.Set_ACLR_AdjSpace(ChSpace)
VSA.Set_ACLR_NumAdj(2)

VSA.Set_ResBW(RBW)
#VSA.Set_DisplayUpdate("OFF")
VSA.Set_SweepTime(MeasTim)
VSA.Set_Trace_Avg('LIN')
VSA.Set_Trace_AvgCount(Avg)
VSA.Set_Trace_Detector('RMS')
VSA.Set_SweepOpt(SweMode)
VSA.Set_SweepType(SweType)
VSA.Set_YIG('OFF')
if 0:
    VSA.Set_Trig1_Source('Ext')

##########################################################
### Measure Time
##########################################################
#sDate = timeit.default_timer().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Iter,RBW,SwpTime,SMWPwr,AL Time,TotalTime,Attn,PreAmp,RefLvl,SwpTime,SwpPts,SwpType,SwpOpt,TxPwr,Adj-,Adj+,Alt-,Alt+')
table = VSAL.ReadLevellingTables(Freq)

for i in range(Repeat):
    for pwr in range(PwrSweep):
        tick = timeit.default_timer()

        ### <\thing we are timing>
        VSG.write(f':POW:AMPL {-50 + pwr}dbm')                  ### VSG Power
        #################
        ### AUTOLEVEL ###
        #################
        if 0:
            VSA.write(':INIT:CONT ON')                          # Sweep Continuous
            VSA.query(':SENS:ADJ:LEV;*OPC?')                    # Auto-Tune
        else:
            lvlTable = VSA.Set_Autolevel_IQIF(table)
        tockA =  timeit.default_timer()
        VSA.Set_Channel('Spectrum')
        VSA.write(':INIT:CONT OFF')                             # Single Sweep
        VSA.query(':INIT:IMM;*OPC?')                            # Take Sweep
        ACLR = VSA.query(':CALC:MARK:FUNC:POW:RES? MCAC')
        ### <\thing we are timing>
        tockB    = timeit.default_timer()
        SwpParam = VSA.Get_SweepParams()
        AmpSet   = VSA.Get_AmpSettings()
        ALTime   = f'{(tockA-tick):2,.6f}'
        TotTime  = f'{(tockB-tick):2,.6f}'
        OutStr   = f'{i},{RBW},{MeasTim},{-50+pwr},{ALTime},{TotTime},{AmpSet},{SwpParam},{ACLR}'
        OFile.write (OutStr)
VSAL.WriteLevellingTables(Freq, table)

##########################################################
### Cleanup Automation
##########################################################
OFile.write("\n")
VSA.jav_Close()