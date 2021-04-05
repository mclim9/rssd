##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Modified from NRP_AvgPwr.py to use correct VISA 
### to include NRP Passport for USB control
### Purpose: Average Power Sensor Readings
### Author : Jim Lukes
### Date   : 2020.18.12
###
### VISAFmt: RSNRP::0x0023::101911::INSTR
###          <VS>::<Modl>::<SerN>::INSTR
###          
###
###   Product  |USB ID        Product  |USB ID      Product  |USB ID
###   ---------|------        ---------|------      ---------|------
###   NRP-Z11    0x00C        NRP-Z31    0x02C      NRP-Z81    0x023
###   NRP-21     0x003        NRP-Z37    0x02D      NRP-Z85    0x083
###   NRP-Z22    0x013        NRP-Z51    0x016      NRP-Z86    0x095
###   NRP-Z23    0x014        NRP-Z52    0x017      NRP-Z91    0x021
###   NRP-Z24    0x015        NRP-Z55    0x018      NRP-Z92    0x062
###   NRP-Z27    0x02F        NRP-Z56    0x019      NRP-Z98    0x052
###   NRP-Z28    0x051        NRP-Z57    0x070
##########################################################
### User Entry
##########################################################
NRPStr   = 'RSNRP::0x023::101911::INSTR'        # USB0::<Make>::<Model>::<Serial Num>::INSTR
Avg      = 100
Freq     = 2e9

##########################################################
### Code Start
##########################################################
from rssd.NRP.Common import PMr

NRP = PMr()
NRP.jav_openvisa(NRPStr)
NRP.Set_Freq(Freq)                              # Set Frequency
NRP.Set_AverageMode(1)                          # Auto Averaging OFF
NRP.Set_Average(Avg)                            # Avg Count = 4
print(NRP.Get_Average())
print(NRP.Get_Power())
NRP.jav_ClrErr()
