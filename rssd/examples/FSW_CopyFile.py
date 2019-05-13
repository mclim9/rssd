##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
###
##########################################################
### User Entry
##########################################################
VSA_IP  = '192.168.1.108'
##########################################################
### Code Overhead
##########################################################
from rssd.FSW_Common        import VSA              #pylint: disable=E0611,E0401
from rssd.yaVISA_socket     import jaVisa           #pylint: disable=E0611,E0401
VSA = VSA().jav_Open(VSA_IP)                  #Create VSA Object

##########################################################
### Code Start
##########################################################

print(VSA.query(':MMEM:CAT? '))
print(VSA.query(':MMEM:CAT? "autologin.reg"'))

##########################################################
### Cleanup Automation
##########################################################
VSA.jav_Close()