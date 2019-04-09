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
VSA_IP  = '192.168.1.109'
VSG_IP  = '192.168.1.114' 
MeasTim = 1e-3
Freq    = 2.3e9
RBW     = 20e3
ChBW    = 18e6
ChSpace = 20e6
Avg     = 0
SweMode = 'NA'
SweType = 'NA'

### Loops
Repeat  = 10
PwrSweep = 59

##########################################################
### Code Overhead
##########################################################
from rssd.FSW_Common        import VSA              #pylint: disable=E0611,E0401
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
   VSA.Set_IQ_BW(5.1*ChSpace)
   VSA.Set_IQ_SpectrumWindow()                      # Add Spectrum Trace
   VSA.Set_Trace_Detector('RMS',2)                  # RMS detector
   VSA.Set_Mkr_Freq(Freq,1,2)                       # Tx Freq
   VSA.Set_Mkr_Band(ChBW,1,2)                       # Tx RFBW
   VSA.Set_Mkr_Freq(Freq-ChSpace,2,2)               # Adj- Freq
   VSA.Set_Mkr_Band(ChBW,2,2)                       # Adj- RFBW
   VSA.Set_Mkr_Freq(Freq+ChSpace,3,2)               # Adj+ Freq
   VSA.Set_Mkr_Band(ChBW,3,2)                       # Adj+ RFB

#VSA.Set_DisplayUpdate("OFF")
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
OFile.write('Iter,RBW,SwpTime,SMWPwr,AL Time,TotalTime,Attn,PreAmp,RefLvl,SwpTime,SwpPts,SwpType,SwpOpt,TxPwr,Adj-,Adj+,Alt-,Alt+')
for i in range(Repeat):
    for pwr in range(PwrSweep):
        tick = datetime.now()
        ### <\thing we are timing>
        VSG.write(f':POW:AMPL {-50 + pwr}dbm')                  ### VSG Power

        #################
        ### AUTOLEVEL ###
        #################
        if 1:
            VSA.write(':INIT:CONT ON')                              # Sweep Continuous
            VSA.query(':SENS:ADJ:LEV;*OPC?')                        # Auto-Tune
        else:
            VSA.query(':INIT:IMM;*OPC?')                            # Take Sweep
            ChPwr = VSA.queryFloatArry(':CALC:MARK:FUNC:POW:RES? MCAC')[0]
            VSA.Set_RefLevel(ChPwr + 5)
            if ChPwr > -20:
                VSA.write('INP:GAIN:STAT OFF')
            else:
                VSA.write('INP:GAIN:STAT ON')
                VSA.write('INP:GAIN:VAL 15')

        tockA =  datetime.now()
        VSA.write(':INIT:CONT OFF')                             # Single Sweep
        VSA.query(':INIT:IMM;*OPC?')                            # Take Sweep
        
        ACLR = []
        for i in range(1,3+1):
            ACLR = ACLR + VSA.Get_Mkr_Band(i,2)
        ### <\thing we are timing>
        tockB = datetime.now()
        SwpParam = VSA.Get_SweepParams()
        AmpSet  = VSA.Get_AmpSettings()
        ALTime = tockA - tick
        TotTime = tockB - tick
        OutStr = f'{i},{RBW},{MeasTim},{-50+pwr},{ALTime.seconds:3d}.{ALTime.microseconds:06d},{TotTime.seconds:3d}.{TotTime.microseconds:06d},{AmpSet},{SwpParam},{ACLR}'
        OFile.write (OutStr)

##########################################################
### Cleanup Automation
##########################################################
OFile.write("\n")
VSA.jav_Close()