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
IParry   = ['demo.rs-us.net:5902',
            'demo.rs-us.net:5902']

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
