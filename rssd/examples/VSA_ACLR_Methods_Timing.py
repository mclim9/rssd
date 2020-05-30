##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
##########################################################
### User Entry
##########################################################
VSA_IP  = '192.168.1.108'
VSG_IP  = '192.168.1.114'
MeasTim = 10e-3
Freq    = 28e9
RBW     = 200e3
ChBW    = 95e6
ChSpace = 100e6
Avg     = 0
SweMode = 'AUTO'            #AUTO | SPEed | DYN
SweType = 'AUTO'           #AUTO | SWE | FFT

### Loops
Repeat  = 10
PwrSweep = 59

##########################################################
### Code Overhead
##########################################################
from datetime               import datetime
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401
from rssd.yaVISA_socket     import jaVisa           #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401

OFile = FileIO().makeFile(__file__)
VSA = VSA().jav_Open(VSA_IP,OFile)                  #Create VSA Object
VSG = jaVisa().jav_Open(VSG_IP,OFile)               #Create Object

meth = {0:'Autolvl()',
        1:'TxChOnly()',
        2:'AvgOff()',
        3:'AutoRBW()',
        4:'SwpTime()',
        5:'SetReflvl()',
        6:'K18()'
        }
meth = {
        1:'SetReflvl()',
        0:'K18()',
        }
asdf=len(meth)

def Autolvl():
    VSA.query(':SENS:ADJ:LEV;*OPC?')                        # Auto-Tune

def TxChOnly():
    VSA.Set_ACLR_NumAdj(0)
    VSA.query(':SENS:ADJ:LEV;*OPC?')                        # Auto-Tune
    VSA.Set_ACLR_NumAdj(2)

def AvgOff():
    VSA.Set_Trace_AvgCount(1)
    VSA.query(':SENS:ADJ:LEV;*OPC?')                        # Auto-Tune
    VSA.Set_Trace_AvgCount(Avg)

def AutoRBW():
    VSA.Set_ResBW(0)
    VSA.query(':SENS:ADJ:LEV;*OPC?')                        # Auto-Tune
    VSA.Set_ResBW(RBW)

def SwpTime():
    VSA.Set_SweepTime(2e-3)
    VSA.query(':SENS:ADJ:LEV;*OPC?')                        # Auto-Tune
    VSA.Set_SweepTime(MeasTim)

def NoAutoLvl():
    pass

def SetReflvl():
    VSA.Set_AttnAuto()
    VSA.write(':INIT:CONT OFF')                             # Single Sweep
    VSA.Set_InitImm()
    ChPwr = VSA.queryFloatArry(':CALC:MARK:FUNC:POW:RES? MCAC')[0]
    VSA.Set_RefLevel(ChPwr + 3)
    VSA.Set_InitImm()
    ChPwr = VSA.queryFloatArry(':CALC:MARK:FUNC:POW:RES? MCAC')[0]
    VSA.Set_RefLevel(ChPwr + 3)
    if ChPwr < -24:     #FSVA:-17  FSW:-22
        VSA.Set_Preamp('ON')
    else:
        VSA.Set_Preamp('OFF')

def K18():
    VSA.Set_Channel('AMPL')
    VSA.Set_Autolevel()                             # Auto-Tune

##########################################################
### Code Start
##########################################################
# VSA.jav_Reset()
VSA.Set_Freq(Freq)
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
# VSA.Set_Trig1_Source('Ext')

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Instr,Iter,RBW,SwpTime,SMWPwr,ALType,AL Time,TotalTime,Attn,PreAmp,RefLvl,SwpTime,SwpPts,SwpType,SwpOpt,TxPwr,Adj-,Adj+,Alt-,Alt+,Freq,ChBw')
for i in range(Repeat):
    for autoMeth in meth:
        for pwr in range(PwrSweep):
            ### <\thing we are timing>
            VSG.query(f':POW:AMPL {-50 + pwr}dbm;*OPC?')            # VSG Power
            tick = datetime.now()

            ### <AUTOLEVEL> ###
            eval(autoMeth)                                          # Dynamically call
            ### <AUTOLEVEL> ###

            tockA =  datetime.now()
            VSA.write(':INIT:CONT OFF')                             # Single Sweep
            VSA.query(':INIT:IMM;*OPC?')                            # Take Sweep
            ACLR = VSA.query(':CALC:MARK:FUNC:POW:RES? MCAC')
            ### <\thing we are timing>
            tockB = datetime.now()
            SwpParam = VSA.Get_SweepParams()
            AmpSet  = VSA.Get_AmpSettings()
            ALTime = tockA - tick
            TotTime = tockB - tick
            OutStr = f'{VSA.Model},{i},{RBW},{MeasTim},{-50+pwr},{meth[autoMeth]},{ALTime.seconds:3d}.{ALTime.microseconds:06d},{TotTime.seconds:3d}.{TotTime.microseconds:06d},{AmpSet},{SwpParam},{ACLR},{Freq},{ChBW}'
            OFile.write (OutStr)

##########################################################
### Cleanup Automation
##########################################################
OFile.write("\n")
VSA.jav_Close()
