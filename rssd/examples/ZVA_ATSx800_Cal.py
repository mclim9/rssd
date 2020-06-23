###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2018.10.26
###
###############################################################################
### User Entry
###############################################################################
ZVA_IP      = '10.0.0.13'
FreqStart   = 2.4e9
FreqStop    = 4.3e9
SwpPt       = 1001

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
ZVA.Set_Trace_DelAll()
ZVA.Set_Trace_MeasAdd_SParam(2,1)               #S21 Measurement
ZVA.Set_Trace_MeasAdd_SParam(3,1)               #S31 Measurement
ZVA.Set_FreqStart(FreqStart)
ZVA.Set_FreqStop(FreqStop)
ZVA.Set_SweepPoints(SwpPt)
ZVA.Set_Trace_Select('S21')
ZVA.Set_InitImm()
ZVA.Set_Mkr_Coupled(1)
ZVA.Set_Mkr_Frq(2.4e9,1)
ZVA.Set_Mkr_Frq(2.8e9,2)
ZVA.Set_Mkr_Frq(3.9e9,3)
ZVA.Save_Trace_CSV('test')
# ZVA.Save_Trace_SxP('TEstS2p')

###############################################################################
### Close Nicely
###############################################################################
ZVA.jav_ClrErr()
ZVA.jav_Close()
