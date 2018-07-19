##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Demonstrate NRPM Radiated power sensor
### Author:  mclim
### Date:    2018.05.31 
##########################################################
### User Entry
##########################################################
visa = '127.0.0.1'               #Get local machine name

##########################################################
### Code Start
##########################################################
from rssd.NPR_Common import PMr

NRP = PMr()
NRP.jav_openvisa("USB0::0x0AAD::0x0196::900105::INSTR")
#   NRP.jav_logscpi()
NRP.jav_Reset()
NRP.Set_Freq(24e9)

print(NRP.Get_PowerAll())        #Power Before SG on
for i in range(1,4):
   NRP.Set_Gen_MasterPwr(1,i)
   NRP.Set_Gen_RFPwr(1,i)
   NRP.Set_Gen_Freq(24e9)
   NRP.Get_Gen_Freq()
   print(NRP.Get_PowerAll())        #Power SG on 
   NRP.Set_Gen_RFPwr(0,i)
   NRP.Set_Gen_MasterPwr(0,i)
NRP.jav_Close()
   
