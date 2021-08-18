##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Sweep FSW/SMW Frequncy
### Author:  mclim
### Date:    2018.05.17
##########################################################
### User Entry
##########################################################
import os
BaseDir = os.path.dirname(os.path.realpath(__file__))
OutFile = BaseDir + "\\data\\SMW_FSW_Sweep"

print(__file__)

SMW_IP = '192.168.1.115'                    #IP Address
FreqStart = int(51e9)
FreqStop = int(75e9)
FreqStep = int(1e9)
fSpan = 100e6
SWM_Out = -20
Mixer = 1

##########################################################
### Code Start
##########################################################
from rssd.VSG.Common import VSG
from rssd.FileIO     import FileIO

f = FileIO()
DataFile = f.Init(OutFile)
SMW = VSG()
SMW.jav_Open(SMW_IP,f.sFName)

##########################################################
### Instrument Settings
##########################################################
SMW.Set_RFPwr(SWM_Out)                    #Output Power
SMW.Set_RFState('ON')                     #Turn RF Output on

f.write(SMW.query('FREQ:MULT:EXT:TYPE?'))   #SMZ #
f.write(SMW.query('FREQ:MULT:EXT:SNUM?'))   #Serial Num
f.write(SMW.query('FREQ:MULT:EXT:LOAD:VERS?'))
f.write(SMW.query('FREQ:MULT:EXT:FMAX?'))
f.write(SMW.query('FREQ:MULT:EXT:FMIN?'))
f.write(SMW.query('FREQ:MULT:EXT:REV?'))    #Revision

f.write("Power")
f.write(SMW.query('FREQ:MULT:EXT:PMAX?'))    #Revision
f.write(SMW.query('FREQ:MULT:EXT:PMIN?'))    #Revision
f.write(SMW.query('FREQ:MULT:EXT:STAT?'))
SMW.write("MMEM:CDIR '/smz/firmware/'")
f.write(SMW.query("FREQ:MULT:EXT:FIRM:CAT?"))
f.write(SMW.query("FREQ:MULT:EXT:CORR:POW:POIN?"))


SMW.jav_ClrErr()                          #Clear Errors
