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
SMW_IP      = '192.168.1.114'
FSWP_IP     = '192.168.1.108'
FreqArry    = range(int(39.8e9),int(43e9),int(100e6))
pwrArry     = range(-20,-13,1)        #Power Array
numMeas     = 1

##########################################################
### Code Overhead: Import and create objects
##########################################################
from datetime               import datetime     #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO       #pylint: disable=E0611,E0401
from rssd.VSG.Common        import VSG          #pylint: disable=E0611,E0401
from rssd.PNA.Common        import PNA          #pylint: disable=E0611,E0401
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
Header = 'Iter,SetFreq,SMFPwr,FSWPFreq,FSWPPwr,LockStatus,PN1,PN2,PN3,PN4'
OFile.write(Header)

FSWP.Set_SweepCont(0)
SMW.Set_RFPwr(-50)
SMW.Set_RFState(1)

for i in range(numMeas):                                        #Loop: Measurements
    for freq  in FreqArry:                                      #Loop: Frequency
        SMW.Set_Freq(freq)
        # FSWP.Set_Freq(freq)
        lockHist = []
        lockPerf = [2,0,0,0]
        for pwr in pwrArry:                                     #Loop: Power
            SMW.Set_RFPwr(pwr)
            FSWP.Set_InitImm()
            FSWP.Set_InitImm()
            # SMW.delay(2)
            lock = FSWP.Get_FreqLock()
            mkr = []
            for m in range(1,5):
                mkr.append(FSWP.Get_Mkr_Y(m))
                # mkr[m-1] = FSWP.Get_Mkr_Y(m)
            ffrq = FSWP.Get_Freq()
            fpwr = FSWP.Get_Power()
            OutStr = f'{i},{freq},{pwr:.2f},{ffrq},{fpwr},{lock},{mkr}'
            OFile.write (OutStr)
            lockHist.append(int(lock))
            if (lockHist[-4:] == [2,0,0,0]):
                break

##########################################################
### Cleanup Automation
##########################################################
SMW.jav_Close()
FSWP.jav_Close()