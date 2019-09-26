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
SMW_IP   = '192.168.1.114'

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.VSG.NR5G_K144     import VSG
from rssd.FileIO            import FileIO


SMW = VSG().jav_Open(SMW_IP)  #Create SMW Object

##########################################################
### Code Start
##########################################################
SMW.write(f'SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:STAT 0')
cat = SMW.query('SOUR1:BB:NR5G:SETT:TMOD:DL:CAT?').split(',')
print(len(cat))

SMW.Set_5GNR_BBState('OFF')
for file in cat:
    SMW.write(f'SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:TYPE {file}')
    SMW.write(f'SOUR1:BB:NR5G:SETT:STOR "/var/user/FRC/{file}"')

##########################################################
### Close Nicely
##########################################################
SMW.jav_Close()