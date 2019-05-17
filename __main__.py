##########################################################
### User Entry
##########################################################
instru_ip  = '192.168.1.114'

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.yaVISA_socket import jaVisa
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)
instr = jaVisa().jav_Open(instru_ip,OFile)  #Create Object

##########################################################
### Code Start
##########################################################
instr.write('*CLS;*WAI')
rdStr = instr.query('*IDN?')
OFile.write(rdStr)

##########################################################
### Cleanup Automation
##########################################################
instr.jav_Close()