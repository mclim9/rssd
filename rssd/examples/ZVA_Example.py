##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2018.10.26
###
##########################################################
### User Entry
##########################################################
ZVA_IP   = 'localhost'
Freq     = 28e9
ChBW     = 100

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.VNA_Common    import VNA
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)
ZVA = VNA().jav_openvisa('TCPIP0::'+ZVA_IP+'::5025::SOCKET',OFile)  #Create SMW Object

##########################################################
### Code Start
##########################################################
ZVA.Set_FreqStart(2e6)
ZVA.Set_FreqStop(3e9)
print(ZVA.query('SYST:ERR?\n\r'))

##########################################################
### Close Nicely
##########################################################
ZVA.jav_Close()
