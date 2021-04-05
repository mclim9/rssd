###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2018.10.26
###
###############################################################################
### User Entry
###############################################################################
SMW_IP   = '192.168.1.114'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.VSG.NR5G_K144     import VSG              #pylint: disable=E0611,E0401
# from rssd.FileIO            import FileIO           #pylint: disable=E0611,E0401
SMW = VSG().jav_Open(SMW_IP)                        #Create SMW Object

###############################################################################
### Code Start
###############################################################################
SMW.Set_5GNR_Direction('DOWN')
cat = SMW.Get_5GNR_TM_Cat()
print(len(cat))

SMW.Set_5GNR_BBState('OFF')
for file in cat:
    print(file)
    SMW.Set_5GNR_TM(file)
    SMW.Set_5GNR_savesetting(f'TM/{file}')

###############################################################################
### Close Nicely
###############################################################################
SMW.jav_Close()
