################################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
################################################################################
### User Entry
################################################################################
VSA_IP  = '192.168.1.109'
VSG_IP  = '192.168.1.114'
MeasTim = 0
Freq    = 9.0e9
RBW     = 200e3
ChBW    = 90e6
ChSpace = 100e6
DUTGain = 50
Avg     = 0
SweMode = 'AUTO'            #AUTO | SPEed | DYN
SweType = 'AUTO'            #AUTO | SWE | FFT

### Loops
Repeat  = 1
PwrSweep = 59

################################################################################
### Code Overhead
################################################################################
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401
from rssd.yaVISA_socket     import jaVisa           #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401
# import rssd.VSA_Leveling    as VSAL               #pylint: disable=E0611,E0401
import timeit

OFile = FileIO().makeFile(__file__)
VSA = VSA().jav_Open(VSA_IP,OFile)                  #Create VSA Object
VSG = jaVisa().jav_Open(VSG_IP,OFile)               #Create Object
################################################################################
### Code Start
################################################################################
# VSA.jav_Reset()
VSA.Set_Freq(Freq)
VSA.Set_Param_Couple_All()
VSA.Init_ACLR()                                     #VSA ACLR Channel
VSA.Set_ACLR_CHBW(ChBW)
VSA.Set_ACLR_AdjBW(ChBW)
VSA.Set_ACLR_AdjSpace(ChSpace)
VSA.Set_ACLR_NumAdj(1)

VSA.Set_ResBW(RBW)
VSA.Set_SweepTime(MeasTim)
VSA.Set_Trace_Avg('LIN')
VSA.Set_Trace_AvgCount(Avg)
VSA.Set_Trace_Detector('RMS')
VSA.Set_SweepOpt(SweMode)
VSA.Set_SweepType(SweType)
VSA.Set_YIG('OFF')
if 0:
    VSA.Set_Trig1_Source('Ext')

################################################################################
### Measure Time
################################################################################
#sDate = timeit.default_timer().strftime("%y%m%d-%H:%M:%S.%f") #Date String
LoopParam   = 'Iter,Pwr'
TimeParam   = 'AlTime,MeasTime,TotalTIme'
SwpParam    = VSA.Get_Params_Sweep(1)
AmpParam    = VSA.Get_Params_Amp(1)
TrcParam    = VSA.Get_Params_Trace(1)
SysParam    = VSA.Get_Params_System(1)
MeasData    = 'TxPwr,Adj-,Adj+,Alt-,Alt+'
OFile.write(f'{LoopParam},{TimeParam},{AmpParam},{SwpParam},{TrcParam},{SysParam},{MeasData}')
# table = VSAL.ReadLevellingTables(Freq)

tick0 = timeit.default_timer()
for i in range(Repeat):
    for VSApwr in range(PwrSweep):
        tick = timeit.default_timer()

        ### <\thing we are timing>
        VSG.write(f':POW:AMPL {VSApwr - DUTGain}dbm')           # VSG Power
        #################
        ### AUTOLEVEL ###
        #################
        if 1:
            VSA.Set_SweepCont(0)                                # Sweep Continuous
            VSA.Set_Autolevel()
        # else:
        #     lvlTable = VSA.Set_Autolevel_IQIF(table)
        tockA =  timeit.default_timer()
        VSA.Set_Channel('SAN')
        VSA.Set_SweepCont(0)                                    # Single Sweep
        VSA.Set_InitImm()                                       # Take Sweep
        ACLR = VSA.query(':CALC:MARK:FUNC:POW:RES? MCAC')
        ### <\thing we are timing>
        tockB    = timeit.default_timer()
        ALTime   = (tockA-tick)
        TotTime  = (tockB-tick)
        TestTime = TotTime - ALTime
        # OutStr   = f'{i},{RBW},{MeasTim},{-50+pwr},{ALTime},{TotTime},{AmpSet},{SwpParam},{ACLR}'

        ##############################################################
        ### LOG DATA
        ##############################################################
        LoopParam   = f'{i},{VSApwr:5.2f}'
        SwpParam    = VSA.Get_Params_Sweep()
        AmpParam    = VSA.Get_Params_Amp()
        TrcParam    = VSA.Get_Params_Trace()
        SysParam    = VSA.Get_Params_System()
        TotTime     = f'{ALTime:2,.6f},{TestTime:2,.6f},{TotTime:2,.6f}'
        MeasData    = ACLR
        OutStr      = f'{LoopParam},{TotTime},{AmpParam},{SwpParam},{TrcParam},{SysParam},{MeasData}'
        OFile.write (OutStr)

# VSAL.WriteLevellingTables(Freq, table)
SuiteTime = timeit.default_timer() - tick0
print(f'Total Test time : {SuiteTime:2,.6f}')
print(f'Time/Measurement: {SuiteTime/(Repeat*PwrSweep):2,.6f}')

################################################################################
### Cleanup Automation
################################################################################
OFile.write("\n")
VSA.jav_Close()
