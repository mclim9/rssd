###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
###
###############################################################################
### User Entry
###############################################################################
VSA_IP  = '192.168.1.109'
VSG_IP  = '192.168.1.114'
MeasTim = 100e-6
Freq    = 9e9
ChBW    = 95e6
ChSpace = 100e6
Avg     = 0

### Loops
Repeat  = 1
PwrSweep = 59

meth = {
        # 0:'VSA.Set_AutoOpt_FSx_Level()',
        0:'VSA.Set_Autolevel()',
        1:'VSA.Set_Mkr_BandSetRef()'
        }

###############################################################################
### Code Overhead
###############################################################################
import timeit
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401
from rssd.yaVISA_socket     import jaVisa           #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401

OFile = FileIO().makeFile(__file__)
VSA = VSA().jav_Open(VSA_IP,OFile)                  #Create VSA Object
VSG = jaVisa().jav_Open(VSG_IP,OFile)               #Create Object
###############################################################################
### Code Start
###############################################################################
#VSA.jav_Reset()
VSA.Init_IQ()                                       #FSW ACLR Channel
VSA.Set_Freq(Freq)
VSA.Set_IQ_ACLR(ChBW, ChSpace)

#VSA.Set_DisplayUpdate("OFF")
VSA.Set_Param_Couple_All()
VSA.Set_SweepTime(MeasTim)
VSA.Set_Trace_Avg('LIN')
VSA.Set_Trace_AvgCount(Avg)
VSA.Set_Trace_Detector('RMS')
VSA.Set_In_YIG('OFF')
# VSA.Set_Trig1_Source('Ext')

###############################################################################
### Measure Time
###############################################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
LoopParam   = 'Iter,ALMeth,Pwr'
TimeParam   = 'AlTime,MeasTime,TotalTIme'
SwpParam    = VSA.Get_Params_Sweep(1)
AmpParam    = VSA.Get_Params_Amp(1)
TrcParam    = VSA.Get_Params_Trace(1)
SysParam    = VSA.Get_Params_System(1)
MeasData    = 'TxPwr,Adj-,Adj+,Alt-,Alt+'
OFile.write(f'{LoopParam},{TimeParam},{AmpParam},{SwpParam},{TrcParam},{SysParam},{MeasData}')

# OFile.write('Model    ,Iter,Freq,RBW,SwpTime,SMWPwr,ALType,ALTime,TotTime,Attn,PreAmp,RefLvl,SwpTime,SwpPts,SwpType,SwpOpt,TxPwr,Adj-,Adj+,Alt-,Alt+,ChSpace')
tick0 = timeit.default_timer()
for i in range(Repeat):
    for autoMeth in meth:
        for VSApwr in range(PwrSweep):
            ### <\thing we are timing>
            VSG.write(f':POW:AMPL {-50 + VSApwr}dbm')               # VSG Power
            tick = timeit.default_timer()

            ### <AUTOLEVEL> ###
            eval(autoMeth)                                          #pylint: disable=W0123
            tockA = timeit.default_timer()
            ### <AUTOLEVEL> ###

            VSA.write(':INIT:CONT OFF')                             # Single Sweep
            VSA.query(':INIT:IMM;*OPC?')                            # Take Sweep
            ACLR = VSA.Get_Mkr_BandACLR()
            ### <\thing we are timing>

            tockB = timeit.default_timer()
            ALTime = tockA - tick
            TotTime = tockB - tick
            TestTime = TotTime - ALTime

            LoopParam   = f'{i},{autoMeth},{VSApwr:5.2f}'
            SwpParam    = VSA.Get_Params_Sweep()
            AmpParam    = VSA.Get_Params_Amp()
            TrcParam    = VSA.Get_Params_Trace()
            SysParam    = VSA.Get_Params_System()
            TotTime     = f'{ALTime:2,.6f},{TestTime:2,.6f},{TotTime:2,.6f}'
            MeasData    = ACLR
            OutStr      = f'{LoopParam},{TotTime},{AmpParam},{SwpParam},{TrcParam},{SysParam},{MeasData}'

            # OutStr = f'{VSA.Model},{i},{Freq},{RBW},{MeasTim},{-50+pwr},{meth[autoMeth]},{ALTime.seconds:3d}.{ALTime.microseconds:06d},{TotTime.seconds:3d}.{TotTime.microseconds:06d},{AmpSet},{SwpParam},{ACLR},{ChSpace}'
            OFile.write (OutStr)
SuiteTime = timeit.default_timer() - tick0
print(f'Total Test time : {SuiteTime:2,.6f}')
print(f'Time/Measurement: {SuiteTime/(Repeat*PwrSweep):2,.6f}')

###############################################################################
### Cleanup Automation
###############################################################################
OFile.write("\n")
VSA.jav_Close()
