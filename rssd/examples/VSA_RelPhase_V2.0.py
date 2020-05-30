##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Relative Phase Example
### Author : mclim
### Date   : 2018.10.22
### HW Conf: FSW 10MHz Ref --> SMW 10MHz Ref In
###             SMW RF --> FSW RF
##########################################################
### User Entry
##########################################################
SwpTim      = 150       #Time, msec
MkrOffset   = 80        #mSec 6.4kHz:90  3.2:80 1.6:70
Delay       = 50        #mSec Delay between
DemodBW     = 6.4       #Demodulation BW, kHz
NumMkrs     = 5         #Number of phase averages
traceAvg    = 2         #Number of trace averages
SwpTim      = (NumMkrs+2)*Delay    #mSec FSW Sweep time
##########################################################
# Bench Settings
##########################################################
FSW_IP = '192.168.1.109'
SMW_IP = '192.168.1.114'

##########################################################
### Code Overhead: Import and create objects
##########################################################
import time
from rssd.VSA.ADemod_K7 import VSA
from rssd.VSG.Common    import VSG
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)
SMW = VSG().jav_Open(SMW_IP,OFile)  #Create SMW Object
FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

##########################################################
### Function Definition
##########################################################
def MeasRelPhase(FSW, SMW, x):
    count = 0
    leaveLoop = 0
    while True:
        SMW.Set_PhaseDelta((x-1)*10)        #Initial Phase Shift
        time.sleep(Delay/1000)              #Wait for phase settling
        FSW.write('INIT:IMM')               #Initiate Sweep
        time.sleep(Delay/1000)              #Wait
        for i in range(NumMkrs + 2):
            time.sleep(Delay/1000)          #Wait
            SMW.Set_PhaseDelta((x)*10)      #Initial Phase Shift
            time.sleep(Delay/1000)          #Wait
            SMW.Set_PhaseDelta((x-1)*10)    #Initial Phase Shift

        mkrArry = []
        for mkr in range(NumMkrs):          #Read Markers
            mkrArry.append(FSW.Get_Mkr_Y(mkr+1))
        #print(mkrArry) #debug

        deltaArry = []                      #Calculate Deltas
        for i in range(len(mkrArry)-1):
            deltaArry.append(abs(mkrArry[i]-mkrArry[i+1]))
            #print("%6.3f - %6.3f = %6.3f"%(mkrArry[i],mkrArry[i+1],deltaArry[i]))  #debug

        #*********************************
        #*** Measurement Error Checking
        #*********************************
        for i,val in enumerate(deltaArry):
            if (val < 0.5):      #Delta too small, not sync'd
                print("Low Delta")
            else:
                AvgAvg = sum(deltaArry) / float(len(deltaArry))
                leaveLoop = 1

        count = count + 1
        if (count > 10):    #Quit if too many retests.
            break

        if leaveLoop:
            break
    return AvgAvg

##########################################################
### Code Start
##########################################################
sDate = time.strftime("%y%m%d-%H%M%S")
OFile.write('DemodBW,Phase,Mkr1,Mkr2,Mkr3,Mkr4,Meas,MeasAvg\n')
FSW.write('SYST:DISP:UPD ON')

#*********************************
#*** SMW-Setup
#*********************************
SMW.Set_Freq(28e9)
SMW.Set_BBState(0)          #Arb Off
SMW.Set_IQMod(0)                #IQ Mod Off
SMW.write(':SOUR1:ROSC:SOUR EXT')          #ExtReference
SMW.write(':SOUR1:ROSC:EXT:FREQ 10MHZ')
SMW.write(':SOUR1:ROSC:EXT:SBAN WIDE')    #SMW WIDE(Vary less)|NARR(varys more) bandwidth
SMW.Set_RFState('ON')

#*********************************
#*** FSW-Analog Demodulation
#*********************************
FSW.Set_Channel('ADEM')
FSW.write('LAY:REPL:WIND "1","XTIM:PM"') #PM Demod window
FSW.Set_SweepCont('OFF')                        #Single sweep
FSW.write('ROSC:SOUR INT')                    #Reference
FSW.Set_Freq(28e9)                                #RF Freq
FSW.Set_SweepTime(SwpTim/1000)                #Sweep Time
FSW.write('SENS:BWID:DEM %fKHZ'%DemodBW) #Demod BW MMM
FSW.write('SENS:ADEM:AF:COUP DC')          #Coupling MMM
FSW.write('UNIT:ANGL DEG')                    #Units
FSW.write('DISP:TRAC1:Y:PDIV 4')            #Y Scaling
FSW.Set_Trace_AvgCount(1)                      #Average
FSW.write('DISP:TRAC:Y:SCAL:RPOS 10PCT') #Phase Reference Position
FSW.write('DISP:TRAC:Y:SCAL:RVAL 1')      #Phase Reference Value
FSW.Set_In_YIG('ON')                 #YIG ON
FSW.write('CALC:FEED "XTIM:PM:TDOM"')

#*********************************
#*** Loop
#*********************************
FSW.Set_Mkr_AllOff()                             #All markers off
for mkr in range(NumMkrs):                     #Create markers
    FSW.Set_Mkr_On(mkr+1)
    FSW.Set_Mkr_Time((MkrOffset+mkr*Delay)/1000,mkr+1)

for phaseAngle in range(1,7):
    phaseMeas = []
    for numAvg in range(traceAvg):
        phaseMeas.append(MeasRelPhase(FSW, SMW, phaseAngle))
    finalPhase = sum(phaseMeas) / float(len(phaseMeas))
    OutStr = ("%6.1f,%2d,%6.3f"%(DemodBW,phaseAngle*10,finalPhase))
    OFile.write(OutStr)
    #raw_input("Meas%d Done"%phaseAngle)

#*********************************
#*** Close Nicely
#*********************************
FSW.jav_Close()
SMW.jav_Close()
