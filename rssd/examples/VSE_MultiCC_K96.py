##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : Multiple CC K96 Example
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

SMW_IP  = '192.168.1.114'
FSW_IP  = '192.168.1.109'
VSE_IP  = '127.0.0.1'               #Get local machine name
Freq    = 29e9                      #Center Frequency
Pwr     = 0                         #SMW RMS Power
CC_Size = 100e6                     #Component Carrier Size
Fs      = 115.2e6                   #Sampling Rate
MeasTim = 500e-6

#BaseDir = "C:\\Users\\LIM_M\\ownCloud\\ATE\\00_Code\\RSSD\\"
OutFile = BaseDir + "\\data\\MultiCC_K96"
IQFile  = BaseDir + "\\file.iqw"
OFDMCfg = BaseDir + "\\misc\\BBAnalog_1CC_100RB_64QAM_IQ-17symC.xml"

##########################################################
### Code Overhead
##########################################################
import rssd.SMW_Common
import rssd.FSW_Common
import rssd.VSE_K96
import rssd.FileIO

f = rssd.FileIO.FileIO()
DataFile = f.Init(OutFile)
SMW = rssd.SMW_Common.VSG()         #Create SMW Object
SMW.VISA_Open(SMW_IP,DataFile)      #Connect to SMW
FSW = rssd.FSW_Common.VSA()         #Create FSW Object
FSW.VISA_Open(FSW_IP,DataFile)      #Connect to FSW
VSE = rssd.VSE_K96.VSE()            #Create VSE Object
VSE.VISA_Open(VSE_IP,DataFile)      #Connect to VSE

##########################################################
### Setup Instruments
##########################################################
VSE.Set_Init_K96()                  #Change Channel
VSE.Set_DisplayUpdate("ON")         #Display On
VSE.Set_SweepCont(0)                #Set Single Sweep
VSE.Set_IQ_SamplingRate(Fs)         #Sampling Rate
VSE.Set_File_InputIQW(Fs,IQFile)    #VSE Input File
VSE.Set_K96_File_Config(OFDMCfg)    #K96 Demod File
VSE.Set_K96_BurstSearch("OFF")
VSE.Set_K96_OFDMSymbols(14)

FSW.Init_IQ()
FSW.Set_IQ_SamplingRate(Fs)
FSW.Set_SweepTime(MeasTim)

##########################################################
### Make Measurement
##########################################################

### Set Frequency
SMW.Set_Freq(Freq)
FSW.Set_Freq(Freq)

### Set Power
SMW.Set_RFPwr(Pwr)
FSW.Set_Autolevel_IFOvld()          #Maximize Dynamic Range
FSW.Get_IQ_Data(IQFile)             #Save IQ Data to file
VSE.Set_Freq(0)
VSE.Set_InitImm()                   #Update VSE
EVM_Meas = VSE.Get_EVM_Params()     #Attn; RefLvl; Pwr; EVM
f.write(EVM_Meas)                 
VSE.VISA_ClrErr()                   #Clear Errors

##########################################################
### Cleanup Automation
##########################################################
SMW.VISA_Close()
FSW.VISA_Close()
VSE.VISA_Close()
