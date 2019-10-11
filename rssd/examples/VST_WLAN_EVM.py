##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Sample SMW FSW WLAN EVM Sweep
### Author : mclim
### Date   : 2019.03.21
###
##########################################################
### User Entry
##########################################################
SMW_IP      = '192.168.1.114'
FSW_IP      = '192.168.1.109'
FreqArry    = [5.25e9,5.57e9]
pwrArry     = [-20, -10, -5]
pwrArry     = range(-50,10,3)       #Power Array
ModArry     = [['AC', 80,11],       #Std,BW,MCS
                ['AC',160,11]]      #Std,BW,MCS
SweepTime   = 0.002

##########################################################
### Code Overhead: Import and create objects
##########################################################
from datetime               import datetime     #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO       #pylint: disable=E0611,E0401
from rssd.VST.WLAN          import VST          #pylint: disable=E0611,E0401
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

for mod in ModArry:                                             #Loop: Standard
    WLAN.WLAN_Std   = mod[0]
    WLAN.WLAN_ChBW  = mod[1]
    WLAN.WLAN_MCS   = mod[2]
    WLAN.Set_WLAN_All()                                 ### Make Waveform ###
    print(f'802.11{WLAN.WLAN_Std} RFBW:{WLAN.WLAN_ChBW} MCS:{WLAN.WLAN_MCS}')
    WLAN.FSW.Set_SweepTime(SweepTime)
#   WLAN.FSW.write(':TRAC:IQ:SRAT 160e6')

    for freq  in FreqArry:                              #Loop: Frequency
        WLAN.FSW.Set_Freq(freq)
        WLAN.SMW.Set_Freq(freq)
        WLAN.Freq = freq
        for pwr in pwrArry:                             #Loop: Power
            WLAN.SMW.Set_RFPwr(pwr)
            #Autolevel Timing
            tick = datetime.now()
            WLAN.FSW.Set_WLAN_Autolvl()
            WLAN.FSW.Set_SweepCont(0)
            ALTime = datetime.now() - tick

            # Measure EVM
            tick = datetime.now()
            WLAN.FSW.Set_InitImm()
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
