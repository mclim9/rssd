###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2018.10.26
###
###############################################################################
### User Entry
###############################################################################
ZVA_IP      = '192.168.1.30'
FreqStart   = 1e9
FreqStop    = 6e9
SwpPt       = 601

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
ZVA.Set_Trace_MeasAdd_SParam(1,1)               #S11 Measurement
ZVA.Set_Trace_MeasAdd_AWave(3,1)                #A-Wave3 w/ Gen1
ZVA.Set_FreqStart(FreqStart)
ZVA.Set_FreqStop(FreqStop)
ZVA.Set_SweepPoints(SwpPt)
print(ZVA.Get_Trace_Names())

###############################################################################
### Close Nicely
###############################################################################
ZVA.jav_ClrErr()
ZVA.jav_Close()
