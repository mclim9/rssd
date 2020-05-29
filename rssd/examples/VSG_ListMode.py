##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: VSG List Mode
### Author:  mclim
### Date:    2019.06.13
##########################################################
### User Entry
##########################################################
host = '192.168.1.114'               #Get local machine name

##########################################################
### Code Start
##########################################################
from rssd.SMW_Common import VSG

SMW = VSG().jav_Open(host)
#SMW.jav_logSCPI()                  # Log SCPI commands
SMW.Set_Freq(10e9)                  # Set 10GHz
SMW.Set_RFPwr(-30)                  # Output -30dBm
SMW.Set_ListMode_File('list1.lsw')  # Select List File
SMW.Set_ListMode_TrigSource('SING') # Single run
SMW.Set_ListMode_RMode('LIVE')
SMW.Set_ListMode_Dwell(1)           # Dwell time
SMW.Set_RFState(1)                  # RF Output on.
SMW.Set_ListMode('LIST')            # Turn on listmode
SMW.Set_ListMode_TrigExecute()      # Execute single trigger
SMW.Set_ListMode_TrigWait()         # Wait for single trigger
SMW.Set_RFState('OFF')              # RF Output off

SMW.jav_ClrErr()                    # Clear Errors
