##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
### Steps  : 
###
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

##########################################################
### Code Overhead: Import and create objects
##########################################################
from datetime               import datetime     #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO       #pylint: disable=E0611,E0401
from rssd.VST_WLAN          import VST          #pylint: disable=E0611,E0401
import time
OFile = FileIO().makeFile(__file__)

##########################################################
### Code Start
##########################################################
WLAN = VST().jav_Open(SMW_IP,FSW_IP,OFile)

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
OFile.write('Freq,Pwr,ALTime,Std,ChBW,MCS,Pwr,Attn,Preamp,RefLvl,EVM,CmdTime')

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

            for freq  in FreqArry:                              #Loop: Frequency
                WLAN.FSW.Set_Freq(freq)
                WLAN.SMW.Set_Freq(freq)
                for pwr in pwrArry:                             #Loop: Power
                    WLAN.SMW.Set_RFPwr(pwr)
                    #Autolevel Timing
                    tick = datetime.now()
                    WLAN.FSW.Set_WLAN_Autolvl()
                    ALTime = datetime.now() - tick
                    input('Cont?')

                    # Measure EVM
                    tick = datetime.now()
                    WLAN.FSW.Init_WLAN()
                    WLAN.FSW.Set_SweepCont(0)
                    WLAN.FSW.Set_InitImm()
                    EVM = WLAN.FSW.Get_WLAN_EVMParams()
                    Attn = WLAN.FSW.Get_AmpSettings()
                    d = datetime.now() - tick
                    OutStr = f'{freq},{pwr:3d},{ALTime.seconds:3d}.{ALTime.microseconds:06d},{WLAN.WLAN_Std},{WLAN.WLAN_ChBW},{WLAN.WLAN_MCS},{Attn},{EVM},{d.seconds:3d}.{d.microseconds:06d}'
                    OFile.write (OutStr)

##########################################################
### Cleanup Automation
##########################################################
WLAN.jav_Close()
