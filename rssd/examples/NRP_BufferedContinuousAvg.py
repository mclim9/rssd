##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Continuous Power Sensor Readings
### Author : mclim
### Date   : 2018.10.01
### Details: Example from NRPxxSN manual Ch 7.3
##########################################################
### User Entry
##########################################################
bUseBUSTrigger = True                           #true:'BUS Trigger' fales:'EXT Trigger'
numMeas = 17

##########################################################
### Code Start
##########################################################
from rssd.NRP.Common import PMr

NRPxxS = PMr()
NRPxxS.jav_openvisa('USB0::0x0AAD::0x0196::900105::INSTR')

#Use the first NRP series NRPxxS which is found
NRPxxS.jav_Reset()                          #Start with a clean state
NRPxxS.Set_AverageMode(0)                   #Auto Averaging OFF
NRPxxS.Set_Average(4)                       #Avg Count = 4
if (bUseBUSTrigger):                        #Select the trigger source
    NRPxxS.Set_TriggerSource('BUS')         #Use '*TRG' to trigger a single physical measurement
else:
    NRPxxS.Set_TriggerSource('EXT2')        #We get trigger pulses on the external input (SMB-type connector)

NRPxxS.Set_TriggerAuto(0)                   #Auto-Trigger OFF
NRPxxS.Set_BufferSize(numMeas)              #Buffer size is randomly selected to 17
NRPxxS.Get_BufferedMeas('ON')               #Configure a buffered measurement
NRPxxS.Set_TriggerCount(numMeas)
szBuff = NRPxxS.jav_ClrErr                  #Read out all errors / Clear error queue

NRPxxS.Set_InitImm()                        #Start a 'single' buffered measurement
                                            #Since 17 trigger-counts have been configured,
                                            #the 'single' buffered measurement, which becomes
                                            #initiated by INIT:IMM, is not over until
                                            #17 physical measurements have been triggered

NRPxxS.write('STAT:OPER:MEAS:NTR 2')        #The end of a physical measurement can be recognized
NRPxxS.write('STAT:OPER:MEAS:PTR 0')        #by a transistion to 'NOT MEASURING' which is a
                                            #negative transistion on bit 1
for i in range(numMeas):                    #Collect 17 physical measurements
    iDummy = NRPxxS.Get_EventStatus()       #Clear the event register by reading it

    if (bUseBUSTrigger):                    #Trigger measurement by '*TRG' or from SMB-type connector
        NRPxxS.write('*TRG')

    iMeasEvent = 0
    while (iMeasEvent != 2):                #Loop until the measurement is done
        iMeasEvent = NRPxxS.Get_EventStatus()
        iMeasEvent = iMeasEvent & 2
    print('Triggered!\n')                   #All 17 physical measurement have been executed.

#That means, buffer is full and can be read
szBuff = NRPxxS.Get_Power()
print(szBuff)
