"""5G NR FSW/SMW Carrier Aggregation Setup Example"""
###############################################################################
### User Entry
###############################################################################
#pylint: disable=E0401
#pylint: disable=E0611
# SMW_IP  = '172.24.225.230'
SMW_IP  = '192.168.58.114'
FSW_IP  = '192.168.58.109'
VSG_ON  = 1
Freq    = 24e9
Pwr     = -5
NumCC   = 8
NR_Dir  = 'UL'
CCSpace = 99.96e6
modu    = 'QPSK'
CCStart = (1 - NumCC) * (CCSpace/2)

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
import timeit
from rssd.VSG.NR5G_K144     import VSG
from rssd.VSA.NR5G_K144     import VSA
# from rssd.FileIO          import FileIO

if VSG_ON: SMW = VSG().jav_Open(SMW_IP)                 #Create SMW Object
FSW = VSA().jav_Open(FSW_IP)                            #Create FSW Object

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
FSW.Set_Freq(Freq + CCStart)                            # FSW Freq --> 1st CC

for i in range(NumCC):
    Freq_CC = Freq + CCStart + (i * CCSpace)
    if VSG_ON:
        SMW.cc = i
        SMW.Set_5GNR_FreqRange(2)
        SMW.Set_5GNR_CC_Offset(CCStart + (i * CCSpace))
        SMW.Set_5GNR_TransPrecoding('ON')
        # SMW.Set_5GNR_PhaseCompensate_Freq(Freq_CC)
        SMW.Set_5GNR_BWP_Ch_Modulation(modu)
    FSW.cc = i+1
    FSW.Set_5GNR_CC_Offset(i+1,i*CCSpace)
    FSW.Set_5GNR_TransPrecoding('ON')
    FSW.Set_5GNR_PhaseCompensate('OFF')
    FSW.Set_5GNR_PhaseCompensate_Freq(Freq_CC)
    FSW.Set_5GNR_CellID(i)
    FSW.Set_5GNR_BWP_SubSpace(120)
    FSW.Set_5GNR_BWP_Ch_Modulation(modu)

tick    = timeit.default_timer()
if VSG_ON: SMW.Set_5GNR_BBState('ON')
tockA   = timeit.default_timer()
print(f'Total Time: {(tockA-tick):2,.6f} sec')
FSW.Set_Autolevel()

###############################################################################
### Close Nicely
###############################################################################
if VSG_ON: SMW.jav_Close()
