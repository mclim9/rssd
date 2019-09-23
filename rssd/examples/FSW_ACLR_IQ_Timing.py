##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
###
##########################################################
### User Entry
##########################################################
VSA_IP  = '192.168.1.108'
VSG_IP  = '192.168.1.114' 
MeasTim = 100e-6
Freq    = 3e9
RBW     = 20e3
ChBW    = 95e6
ChSpace = 100e6
Avg     = 0
SweMode = 'NA'
SweType = 'NA'

### Loops
Repeat  = 10
PwrSweep = 59

meth = {
        0:'VSA.Set_AutoOpt_FSx_Level()',
        # 1:'VSA.Set_Autolevel()',
        1:'VSA.Set_Mkr_BandSetRef()'
        }

##########################################################
### Code Overhead
##########################################################
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401
from rssd.yaVISA_socket     import jaVisa           #pylint: disable=E0611,E0401
from datetime               import datetime         
from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401

OFile = FileIO().makeFile(__file__)
VSA = VSA().jav_Open(VSA_IP,OFile)                  #Create VSA Object
VSG = jaVisa().jav_Open(VSG_IP,OFile)               #Create Object
##########################################################
### Code Start
##########################################################
#VSA.jav_Reset()
VSA.Init_IQ()                                       #FSW ACLR Channel
if 1:
   VSA.Set_Freq(Freq)
   VSA.Set_IQ_ACLR(ChBW, ChSpace)

#VSA.Set_DisplayUpdate("OFF")
VSA.Set_Param_Couple_All()
VSA.Set_SweepTime(MeasTim)
VSA.Set_Trace_Avg('LIN')
VSA.Set_Trace_AvgCount(Avg)
VSA.Set_YIG('OFF')
if 0:
    VSA.Set_Trig1_Source('Ext')

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Model    ,Iter,Freq,RBW,SwpTime,SMWPwr,ALType,ALTime,TotTime,Attn,PreAmp,RefLvl,SwpTime,SwpPts,SwpType,SwpOpt,TxPwr,Adj-,Adj+,Alt-,Alt+,ChSpace')
for i in range(Repeat):
    for autoMeth in range(len(meth)):
        for pwr in range(PwrSweep):
            ### <\thing we are timing>
            VSG.write(f':POW:AMPL {-50 + pwr}dbm')                  ### VSG Power
            tick = datetime.now()

            ### <AUTOLEVEL> ###
            eval(meth[autoMeth])                                    # Dynamically call
            tockA =  datetime.now()
            ### <AUTOLEVEL> ###

            VSA.write(':INIT:CONT OFF')                             # Single Sweep
            VSA.query(':INIT:IMM;*OPC?')                            # Take Sweep
            ACLR = VSA.Get_Mkr_BandACLR()
            ### <\thing we are timing>

            tockB = datetime.now()
            SwpParam = VSA.Get_SweepParams()
            AmpSet  = VSA.Get_AmpSettings()
            ALTime = tockA - tick
            TotTime = tockB - tick
            OutStr = f'{VSA.Model},{i},{Freq},{RBW},{MeasTim},{-50+pwr},{meth[autoMeth]},{ALTime.seconds:3d}.{ALTime.microseconds:06d},{TotTime.seconds:3d}.{TotTime.microseconds:06d},{AmpSet},{SwpParam},{ACLR},{ChSpace}'
            OFile.write (OutStr)

##########################################################
### Cleanup Automation
##########################################################
OFile.write("\n")
VSA.jav_Close()