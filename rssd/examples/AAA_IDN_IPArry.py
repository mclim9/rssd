##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2019.03.19
###
##########################################################
### User Entry
##########################################################
IParry   = ['192.168.1.109','192.168.1.114','192.168.1.160']

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.yaVISA    import jaVisa

##########################################################
### Code Start
##########################################################
for IPAddr in IParry:
    instr = jaVisa().jav_Open(IPAddr)
    instr.jav_IDN()
    instr.jav_Close()
