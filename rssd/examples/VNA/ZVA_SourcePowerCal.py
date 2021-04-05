###############################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2019.03.15
###
###############################################################################
### User Entry
###############################################################################
ZVA_IP      = '192.168.1.30'
FreqStart   = 1e9
FreqStop    = 6e9
SwpPt       = 601
TolerancedB = 0.1
NumSweep    = 10
CalPort     = 2

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.VNA.Common    import VNA
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)
ZVA = VNA().jav_openvisa(f'TCPIP0::{ZVA_IP}::inst0',OFile)

###############################################################################
### Code Start
###############################################################################
ZVA.Set_FreqStart(FreqStart)
ZVA.Set_FreqStop(FreqStop)
ZVA.Set_SweepPoints(SwpPt)

ZVA.Set_Pwrcal_Init()
ZVA.Set_Pwrcal_Tolerance(TolerancedB)
ZVA.Set_Pwrcal_NumReading(NumSweep)
ZVA.Set_Pwrcal_Measure(CalPort)             #Initiate Power cal
print(ZVA.Get_Pwrcal_State())               #Return Power Cal state

###############################################################################
### Close Nicely
###############################################################################
ZVA.jav_ClrErr()
ZVA.jav_Close()
