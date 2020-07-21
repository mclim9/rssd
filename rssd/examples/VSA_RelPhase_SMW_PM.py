###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Relative Phase Example
### HW Conf: FSW 10MHz Ref --> SMW 10MHz Ref In
###             SMW RF --> FSW RF
###############################################################################
### User Entry
###############################################################################
SwpTim      = 150                   # Time, msec
MkrOffset   = 2                    # mSec 6.4kHz:90  3.2:80 1.6:70
Delay       = 1                    # mSec Delay between
DemodBW     = 100                   # Demodulation BW, kHz
NumMkrs     = 5                     # Number of phase averages
traceAvg    = 2                     # Number of trace averages
SwpTim      = (NumMkrs+2)*Delay     # mSec FSW Sweep time

###############################################################################
# Bench Settings
###############################################################################
FSW_IP = '192.168.1.109'
SMW_IP = '192.168.1.114'

###############################################################################
### Overhead: Import and create objects
###############################################################################
from rssd.VSA.ADemod_K7 import VSA
from rssd.VSG.Common    import VSG
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)
SMW = VSG().jav_Open(SMW_IP,OFile)          # Create SMW Object
FSW = VSA().jav_Open(FSW_IP,OFile)          # Create FSW Object

###############################################################################
### Function Definition
###############################################################################
def MeasRelPhase(FSW):
    leaveLoop = 0
    for i in range(10):
        FSW.write('INIT:IMM')               # Initiate Sweep

        mkrArry = []
        for mkr in range(NumMkrs):          # Read Markers
            mkrArry.append(FSW.Get_Mkr_Y(mkr+1))

        deltaArry = []                      # Calculate Deltas
        for i in range(len(mkrArry)-1):
            deltaArry.append(abs(mkrArry[i]-mkrArry[i+1]))

        #######################################################################
        ### Measurement Error Checking
        #######################################################################
        for i,val in enumerate(deltaArry):
            if (val < 0.5):                 # Delta too small, not sync'd
                print("Low Delta")
            else:
                AvgAvg = sum(deltaArry) / float(len(deltaArry))
                leaveLoop = 1
        if leaveLoop:   break
    return AvgAvg

def rad2deg(radian):
    """ PI() * Radian = 180 Degree"""
    degree = radian * 180 / 3.14159
    return degree

def deg2rad(degree):
    radian = degree * 3.14159 / 180
    return radian

###############################################################################
### Code Start
###############################################################################
OFile.write('DemodBW,Phase,Mkr1,Mkr2,Mkr3,Mkr4,Meas,MeasAvg\n')
FSW.write('SYST:DISP:UPD ON')

###############################################################################
### SMW-Setup  1 Radian = 180/Pi()
###############################################################################
SMW.Set_Freq(28e9)
SMW.Set_BBState(0)                          # Arb Off
SMW.Set_IQMod(0)                            # IQ Mod Off

SMW.Set_Ref_Source('EXT')                   # ExtReference
SMW.Set_Ref_Freq('10MHZ')
SMW.Set_Ref_SyncBW('WIDE')                  # Oscilator locking BW
SMW.Set_RFState('ON')

SMW.write(':SOUR1:LFO1:SHAP PULS')          # Set LF1 shape to Pulse (square wave)
SMW.write(':SOUR1:LFO1:SHAP:PULS:PER 0.002')# Set Pulse Period to 2mSec
SMW.write(':SOUR1:LFO1:SHAP:PULS:DCYC 50')  # Set Pulse Duty cycle 50%
SMW.write(':SOUR1:PM1:SOUR LF1')            # Set PM source LF1
SMW.write(':SOUR1:PM1:DEV 0.174532')        # Set PM Deviation 0.174532 radian

###############################################################################
### FSW-Analog Demodulation
###############################################################################
FSW.Set_Channel('ADEM')
FSW.write('LAY:REPL:WIND "1","XTIM:PM"')    # PM Demod window
FSW.Set_SweepCont('ON')                     # Single sweep
FSW.Set_Ref_Source('INT')                   # Reference
FSW.Set_Freq(28e9)                          # RF Freq
FSW.Set_SweepTime(SwpTim/1000)              # Sweep Time
FSW.Set_Adem_dbw(DemodBW*1000)              # Demod BW
FSW.Set_Adem_Coupling('AC')                 # Coupling
FSW.Set_Adem_PM_Unit('DEG')                 # Units
FSW.Set_Adem_PM_Scale(4)                    # Y Scaling
FSW.Set_Adem_PM_RefPos(50)                  # Phase Reference Position
FSW.Set_Adem_PM_RefVal(1)                   # Phase Reference Value
FSW.Set_Trace_AvgCount(1)                   # Average Count
FSW.Set_In_YIG('ON')                        # YIG ON
FSW.write('CALC:FEED "XTIM:PM:TDOM"')

###############################################################################
### Loop
###############################################################################
FSW.Set_Mkr_AllOff()                        # All markers off
for mkr in range(NumMkrs):                  # Create markers
    FSW.Set_Mkr_On(mkr+1)
    FSW.Set_Mkr_Time((MkrOffset+mkr*Delay)/1000,mkr+1)

for phaseAngle in range(1,3):
    phaseMeas = []
    for numAvg in range(traceAvg):
        phaseMeas.append(MeasRelPhase(FSW))
    finalPhase = sum(phaseMeas) / float(len(phaseMeas))
    OutStr = ("%6.1f,%2d,%6.3f"%(DemodBW,phaseAngle*10,finalPhase))
    OFile.write(OutStr)

###############################################################################
### Close Nicely
###############################################################################
FSW.jav_Close()
SMW.jav_Close()
