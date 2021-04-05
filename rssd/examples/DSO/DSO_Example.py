################################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Digital Storage Oscilloscope Example
### Author : mclim
### Date   : 2020.03.24
###
################################################################################
### User Entry
################################################################################
RTO_IP      = '192.168.1.33'

################################################################################
### Code Overhead
################################################################################
from rssd.FileIO            import FileIO       #pylint: disable=E0611,E0401
from rssd.DSO.Common        import DSO

OFile   = FileIO().makeFile(__file__)           # Open Log file
RTO     = DSO().jav_Open(RTO_IP, OFile)         # Create RTO object & log IDN

################################################################################
### Code Start
################################################################################
rdStr = RTO.query('*IDN?')
RTO.Set_TimeScale(1e-8)
rdStr = RTO.Get_TimeScale()
RTO.Set_TimeScale(2e-8)
rdStr = RTO.Get_TimeScale()
OFile.write(rdStr)
