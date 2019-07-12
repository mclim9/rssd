##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date    : 2018.05.24
###
##########################################################
### User Entry
##########################################################
SMW_IP      = '192.168.1.113'
FSWP_IP     = '192.168.1.108'
FreqArry    = range(18000000000,40000000000,500000000)
pwrArry     = range(-50,10,5)        #Power Array
numMeas     = 1

##########################################################
### Code Overhead: Import and create objects
##########################################################
from datetime               import datetime     #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO       #pylint: disable=E0611,E0401
from rssd.SMW_Common        import VSG          #pylint: disable=E0611,E0401
from rssd.PNA_Common        import PNA          #pylint: disable=E0611,E0401
import time

OFile = FileIO().makeFile(__file__)

##########################################################
### Code Start
##########################################################
SMW = VSG().jav_Open(SMW_IP, OFile)
FSWP = PNA().jav_Open(FSWP_IP, OFile)

##########################################################
### Measure Time
##########################################################
Header = 'Iter,SetFreq,SMFPwr,FSWPFreq,FSWPPwr,LockStatus'
OFile.write(Header)

FSWP.Set_SweepCont(0)
SMW.Set_RFPwr(-50)
SMW.Set_RFState(1)

for i in range(numMeas):                                        #Loop: Measurements
    for freq  in FreqArry:                                      #Loop: Frequency
        SMW.Set_Freq(freq)
        # FSWP.Set_Freq(freq)
        for pwr in pwrArry:                                     #Loop: Power
            SMW.Set_RFPwr(pwr)
            FSWP.Set_InitImm()
            SMW.delay(2)
            lock = FSWP.Get_FreqLock()
            ffrq = FSWP.Get_Freq()
            fpwr = FSWP.Get_Power()
            OutStr = f'{i},{freq},{pwr},{ffrq},{fpwr},{lock}'
            OFile.write (OutStr)

##########################################################
### Cleanup Automation
##########################################################
SMW.jav_Close()
FSWP.jav_Close()