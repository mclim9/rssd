###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2020.03.12
###
###############################################################################
### User Entry
###############################################################################
# SMW_IP  = '172.24.225.230'
SMW_IP  = '192.168.1.114'
FSW_IP  = '192.168.1.109'
VSG_ON  = 1
Freq    = 39e9
Pwr     = -10
NumCC   = 1
NR_Dir  = 'UP'
CCSpace = 99.96e6
CCStart = (1 - NumCC) * (CCSpace/2)

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.VSG.NR5G_K144     import VSG              #pylint: disable=E0611,E0401
from rssd.VSA.NR5G_K144     import VSA              #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401
import timeit

if VSG_ON: SMW = VSG().jav_Open(SMW_IP)             #Create SMW Object
FSW = VSA().jav_Open(FSW_IP)                        #Create FSW Object

###############################################################################
### Code Start
###############################################################################
if VSG_ON:
    SMW.Get_SysC_All()
    SMW.Set_Freq(Freq)                                  # SMW Freq --> BB Center
    SMW.Set_5GNR_BBState('OFF')
    SMW.Set_5GNR_Direction(NR_Dir)
    SMW.Set_5GNR_CC_Num(NumCC)
    SMW.Set_5GNR_PhaseCompensate('OFF')
    SMW.Set_RFPwr(Pwr)
    SMW.Set_RFState(1)

FSW.Init_5GNR()
FSW.Set_5GNR_Result_View('ALL')
FSW.Set_5GNR_EVMUnit('DB')
FSW.Set_5GNR_Direction(NR_Dir)
FSW.Set_5GNR_FreqRange(2)
FSW.Set_SweepCont(1)
FSW.Set_5GNR_CC_Num(NumCC)
FSW.Set_5GNR_CC_Capture('SING')
FSW.Set_Freq(Freq + CCStart)                        # FSW Freq --> 1st CC

for i in range(NumCC):
    Freq_CC = Freq + CCStart + (i * CCSpace)
    if VSG_ON:
        SMW.cc = i
        SMW.Set_5GNR_FreqRange(2)
        SMW.Set_5GNR_CC_Offset(CCStart + (i * CCSpace))
        SMW.Set_5GNR_TransPrecoding('ON')
        SMW.Set_5GNR_PhaseCompensate_Freq(Freq_CC)
    FSW.cc = i+1
    FSW.Set_5GNR_CC_Offset(i+1,i*CCSpace)
    FSW.Set_5GNR_TransPrecoding('ON')
    FSW.Set_5GNR_PhaseCompensate('OFF')
    FSW.Set_5GNR_PhaseCompensate_Freq(Freq_CC)
    FSW.Set_5GNR_CellID(i)
    FSW.Set_5GNR_BWP_SubSpace(120)

tick    = timeit.default_timer()
if VSG_ON: SMW.Set_5GNR_BBState('ON')
tockA   = timeit.default_timer()
print(f'Total Time: {(tockA-tick):2,.6f} sec')
FSW.Set_Autolevel()

###############################################################################
### Close Nicely
###############################################################################
if VSG_ON: SMW.jav_Close() 