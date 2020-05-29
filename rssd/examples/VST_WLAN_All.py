##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Sample SMW FSW WLAN EVM Sweep
### Author : mclim
### Date   : 2019.03.21
##########################################################
### User Entry
##########################################################
SMW_IP      = '192.168.1.114'
FSW_IP      = '192.168.1.109'
FreqArry    = [2.1e9,2.2e9]
pwrArry     = [-20, -10, -5]
StdArry     = ['AC','N']
CHBWArry    = [20,40]
MCSArry     = [1,3,5]
SweepTime   = 0.002

MeasEVM     = 0
MeasACLR    = 0
MeasSEM     = 1

##########################################################
### Code Overhead: Import and create objects
##########################################################
# import time
from datetime               import datetime     #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO       #pylint: disable=E0611,E0401
from rssd.VST_WLAN          import VST          #pylint: disable=E0611,E0401
OFile = FileIO().makeFile(__file__)

##########################################################
### Code Start
##########################################################
WLAN = VST().jav_Open(SMW_IP,FSW_IP,OFile)

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Freq,SMWPwr,ALTime,Std,ChBW,MCS,Attn,Preamp,RefLvl,MeasPwr,EVM,SEM,TxCh,Adj-,Adj+,Alt1-,Alt1+,Alt2-,Alt2+,CmdTime')        # All

WLAN.FSW.jav_Reset()
WLAN.FSW.Init_WLAN()
WLAN.FSW.Set_Trig1_Source('EXT')
WLAN.FSW.Set_SweepCont(0)

for std in StdArry:                                             #Loop: Standard
    for chbw in CHBWArry:                                       #Loop: Ch Bandwidth
        for MCS in MCSArry:                                     #Loop: Modulation
            WLAN.WLAN_Std   = std
            WLAN.WLAN_MCS   = MCS
            WLAN.WLAN_ChBW  = chbw
            WLAN.Set_WLAN_All()                                 ### Make Waveform ###
            print(f'802.11{std} RFBW:{WLAN.WLAN_ChBW} MCS:{MCS}')
            WLAN.FSW.Set_SweepTime(SweepTime)
            WLAN.FSW.write(':TRAC:IQ:SRAT 160e6')

            for freq  in FreqArry:                              #Loop: Frequency
                WLAN.FSW.Set_Freq(freq)
                WLAN.SMW.Set_Freq(freq)
                for pwr in pwrArry:                             #Loop: Power
                    WLAN.SMW.Set_RFPwr(pwr)

                    ### Autolevel Timing
                    tick = datetime.now()
                    WLAN.FSW.write(':CONF:BURS:IQ:IMM')                             #EVM
                    WLAN.FSW.write(':SENS:DEM:FORM:BCON:AUTO 1')                    #Auto PPDU Demod
                    WLAN.FSW.Set_WLAN_Autolvl()
                    Attn = WLAN.FSW.Get_AmpSettings()
                    WLAN.FSW.Set_SweepCont(0)
                    ALTime = datetime.now() - tick
                    tick = datetime.now()
                    WLAN.FSW.Set_InitImm()

                    ### Measure EVM
                    if MeasEVM:
                        WLAN.FSW.Set_InitImm()
                        WLAN.FSW.write(':CONF:BURS:IQ:IMM')                             #EVM
                        WLAN.FSW.write(':SENS:DEM:FORM:BCON:AUTO 1')                    #Auto PPDU Demod
                        WLAN.FSW.Set_InitImm()
                        EVM = WLAN.FSW.Get_WLAN_EVMParams()
                    else:
                        EVM = '-9999,-9999'
                    ### Measure ACLR
                    if MeasACLR:
                        WLAN.FSW.write(':CONF:BURS:SPEC:ACPR:IMM')                      #Config ACLR Ch
                        WLAN.FSW.Set_InitImm()
                        WLAN.FSW.Set_InitImm()
                        ACLR = WLAN.FSW.Get_ACLR()
                    else:
                        ACLR = [-9999,-9999,-9999,-9999,-9999,-9999,-9999]

                    ### Measure SEM
                    if MeasSEM:
                        WLAN.FSW.write(':CONF:BURS:SPEC:MASK:IMM')                      #Config SEM Ch
                        WLAN.FSW.Set_InitImm()
                        SEM = WLAN.FSW.query(':CALC1:LIM:FAIL?')
                    else:
                        SEM = 'NotTested'
                    d = datetime.now() - tick
                    OutStr = f'{freq},{pwr:3d},{ALTime.seconds:3d}.{ALTime.microseconds:06d},{WLAN.WLAN_Std},{WLAN.WLAN_ChBW},{WLAN.WLAN_MCS},{Attn},{EVM},{SEM},{ACLR},{d.seconds:3d}.{d.microseconds:06d}'
                    OFile.write (OutStr)

##########################################################
### Cleanup Automation
##########################################################
WLAN.jav_Close()
