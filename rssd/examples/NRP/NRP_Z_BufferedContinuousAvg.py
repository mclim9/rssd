##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Continuous Power Sensor Readings
### Author : Jim Lukes
### Date   : 2020.18.12
### Details: Example from NRP_ZN manual Ch 7.3
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
bUseBUSTrigger = False                  #true:'BUS Trigger' fales:'EXT Trigger'
numMeas = 3
Freq = 1e9
APR = 1e-3
##########################################################
### Code Start
##########################################################
from rssd.NRP.Common import PMr

NRP_Z = PMr()
NRP_Z.jav_openvisa('RSNRP::0x023::101911::INSTR')

NRP_Z.jav_Reset()                       #Start with a clean state
NRP_Z.Set_InitCont('OFF')
NRP_Z.Set_Freq(Freq)
NRP_Z.Set_Function("POW:AVG")
NRP_Z.Set_AverageMode('OFF')            #Auto Averaging OFF
NRP_Z.Set_BufferSize(numMeas)           #Buffer size is randomly selected to 17
NRP_Z.Get_BufferedMeas('ON')            #Configure a buffered measurement
NRP_Z.Set_Aperture(APR)
NRP_Z.Set_TriggerCount(numMeas)         #Avg Count = 4
NRP_Z.Set_TriggerSource('IMM')          #We get trigger pulses on the external input (SMB-type connector)
szBuff = NRP_Z.Get_Power()
print(szBuff)
