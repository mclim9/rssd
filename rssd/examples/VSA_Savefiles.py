##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Timing SCPI Commands Example
### Author : mclim
### Date   : 2019.12.06
### Steps  : 
###
##########################################################
### User Entry
##########################################################
FSW_IP   = '192.168.1.109'
SaveName = 'test'

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.VSA.NR5G_K144    import VSA
FSW = VSA().jav_Open(FSW_IP)  #Create FSW Object

##########################################################
### Code Start
##########################################################
FSW.Set_5GNR_AllocFileSave(SaveName)
FSW.Set_Savestate(SaveName)

##########################################################
### Cleanup Automation
##########################################################
FSW.jav_Close()
