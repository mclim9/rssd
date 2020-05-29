##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: FSW/SMW 5G NR Demo
### Author:  mclim
### Date:    2018.09.10
### Descrip: FSW 3.20-18.7.1.0 Beta
###          SMW 4.30 SP2
##########################################################
### User Entry
##########################################################
SMW_IP   = '192.168.1.114'                    #IP Address
FSW_IP   = '192.168.1.109'                    #IP Address

##########################################################
### Code Start
##########################################################
from rssd.VST.NR5G_K144 import VST           #pylint: disable=E0611,E0401

if __name__ == "__main__":
    NR5G = VST().jav_Open(SMW_IP,FSW_IP)
    NR5G.Get_5GNR_All_print()
    NR5G.jav_Clear()
    NR5G.jav_Close()
