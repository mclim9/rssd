"""VSA Single Sweep Example"""
FSW_IP  = '192.168.58.109'
Freq    = 28e9
##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.VSA.Common    import VSA
FSW = VSA().jav_Open(FSW_IP)        # Create FSW Object

##########################################################
### Code Start
##########################################################

FSW.Set_Freq(Freq)
FSW.write('INIT:CONT OFF')          # Single Sweep Mode
FSW.query('INIT:IMM; *OPC?')        # Take 1st sweep
FSW.query('INIT:IMM; *OPC?')        # Take 2nd sweep

##########################################################
### Cleanup Automation
##########################################################
FSW.jav_Close()
