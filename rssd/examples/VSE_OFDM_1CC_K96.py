##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Single OFDM CC K96 Example
### Author : mclim
### Date   : 2018.05.01
### Steps  : 800MHz FSW IQ Capture
###          FSW IQ Data --> File
###          File --> VSE --> EVM
###          Repeat w/ each CC
###
##########################################################
### User Entry
##########################################################
import os
BaseDir = os.path.dirname(os.path.realpath(__file__))
OutFile = BaseDir + "\\data\\" + __file__
IQFile  = BaseDir + "\\data\\" + __file__ + ".iqw"
OFDMCfg = BaseDir + "\\misc\\BBAnalog_1CC_100RB_64QAM_IQ-17symC.xml"

SMW_IP  = '192.168.1.114'
FSW_IP  = '192.168.1.109'
VSE_IP  = '127.0.0.1'               #Get local machine name
FreqArry= [10e9]                    #Center Frequency
PwrArry = [0,2]                     #SMW RMS Power
CC_Size = 100e6                     #Component Carrier Size
Fs      = 115.2e6                   #Sampling Rate
MeasTim = 500e-6

##########################################################
### Code Overhead
##########################################################
from rssd.SMW_Common import VSG
from rssd.FSW_Common import VSA
from rssd.VSE.K96    import VSE
import rssd.FileIO
import time

f = rssd.FileIO.FileIO()
DataFile = f.Init(OutFile)
SMW = VSG()                         #Create SMW Object
SMW.jav_Open(SMW_IP,f.sFName)      #Connect to SMW
FSW = VSA()                         #Create FSW Object
FSW.jav_Open(FSW_IP,f.sFName)      #Connect to FSW
VSE = VSE()                         #Create VSE Object
VSE.jav_Open(VSE_IP,f.sFName)      #Connect to VSE
if 0:
   SMW.jav_logSCPI()
   FSW.jav_logSCPI()
   VSE.jav_logSCPI()
   
##########################################################
### Setup Instruments
##########################################################
VSE.jav_Reset()
#time.sleep(6)
VSE.Init_K96()                      #Change Channel
VSE.Set_DisplayUpdate("ON")         #Display On
VSE.Set_SweepCont(0)                #Continuous Sweep Off
VSE.Set_IQ_SamplingRate(Fs)         #Sampling Rate
VSE.Set_File_InputIQW(Fs,IQFile)    #VSE Input File
VSE.Set_K96_File_Config(OFDMCfg)    #K96 Demod File
VSE.Set_K96_BurstSearch("OFF")      #Burst Search off
VSE.Set_K96_OFDMSymbols(14)

FSW.jav_Reset()
FSW.Init_IQ()                       #FSW IQ Channel
FSW.Set_IQ_SamplingRate(Fs)
FSW.Set_SweepTime(MeasTim)

SMW.Set_RFState("ON")

##########################################################
### Make Measurement
##########################################################

for Freq in FreqArry:
   ### Set Frequency
   SMW.Set_Freq(Freq)
   FSW.Set_Freq(Freq+50e6)
   VSE.Set_Freq(0)

   for Pwr in PwrArry:
      ### Set Power
      SMW.Set_RFPwr(Pwr)
      #FSW.Set_Autolevel_IFOvld()          #Maximize Dynamic Range

      ### Measure EVM
      FSW.Get_IQ_Data(IQFile)             #Save IQ Data to file
      VSE.Set_InitImm()                   #Update VSE
      EVM_Meas = VSE.Get_EVM_Params()     #Attn; RefLvl; Pwr; EVM
      f.write(EVM_Meas)                 
      VSE.jav_ClrErr()                   #Clear Errors
   #end PwrLoop
#end FreqLoop   

##########################################################
### Cleanup Automation
##########################################################
SMW.jav_Close()
FSW.jav_Close()
VSE.jav_Close()
