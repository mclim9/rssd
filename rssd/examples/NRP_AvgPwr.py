##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Average Power Sensor Readings
### Author : mclim
### Date   : 2018.10.01
###
### VISAFmt: USB0::0x0AAD::0x0138::100961::INSTR
###          <VS>::<Manu>::<Modl>::<SerN>::INSTR
###          TCPIP0::NRPM3-900105::inst0
###
###   Product  |USB ID        Product  |USB ID
###   ---------|------        ---------|------
###   NRP8S     0x00E2        NRP33SN-V 0x0168
###   NRP8SN    0x0137        NRP40S    0x015F
###   NRP18S    0x0138        NRP40SN   0x0160
###   NRP18SN   0x0139        NRP50S    0x0161
###   NRP33S    0x0145        NRP50SN   0x0162
###   NRP33SN   0x0146        NRPM      0x0195
##########################################################
### User Entry
##########################################################
NRPStr   = 'USB0::0x0AAD::0x015F::100935::INSTR'     # USB0::<Make>::<Model>::<Serial Num>::INSTR
Avg      = 100
Freq     = 28e9

##########################################################
### Code Start
##########################################################
from rssd.NRP.Common import PMr 

NRP = PMr()
NRP.jav_openvisa(NRPStr)
NRP.Set_Freq(Freq)                           # Set Frequency
NRP.Set_AverageMode(1)                       # Auto Averaging OFF
NRP.Set_Average(Avg)                         # Avg Count = 4
print(NRP.Get_Average())
print(NRP.Get_Power())
NRP.jav_ClrErr()