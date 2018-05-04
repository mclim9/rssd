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
SMW_IP = '192.168.1.114'
FSW_IP = '192.168.1.109'
VSE_IP = '127.0.0.1'                #Get local machine name
Freq = 29e9                         #Center Frequency
CC_Size = 100e6                     #Component Carrier Size
Fs = 115.2e6                        #Sampling Rate

BaseDir = "C:\\Users\\LIM_M\\ownCloud\\ATE\\00_Code\\RS_ATE_Python2\\"
IQFile  = BaseDir + "file2.iqw"
OFDMCfg = BaseDir + "misc\\BBAnalog_1CC_100RB_64QAM_IQ-17symC.xml"
##########################################################
### Code Overhead
##########################################################
import driver.SMW_Common
import driver.FSW_Common
import driver.VSE_K96
import utils.FileIO

f = utils.FileIO.FileIO()
DataFile = f.Init("Datalog")
SMW = driver.SMW_Common.VSG()       #Create SMW Object
SMW.VISA_Open(SMW_IP,DataFile)      #Connect to SMW
FSW = driver.FSW_Common.VSA()       #Create FSW Object
FSW.VISA_Open(FSW_IP,DataFile)      #Connect to FSW
VSE = driver.VSE_K96.VSE()          #Create VSE Object
VSE.VISA_Open(VSE_IP,DataFile)      #Connect to VSE

##########################################################
### Setup Instruments
##########################################################
VSE.Set_Init_K96()                  #Change Channel
VSE.Set_DisplayUpdate("ON")         #Display On
VSE.Set_SweepCont(0)
VSE.Set_IQ_SamplingRate(Fs)         #Sampling Rate
VSE.Set_File_InputIQW(Fs,IQFile)
VSE.Set_File_K96Config(OFDMCfg)
FSW.Init_IQ()
FSW.Set_IQ_SamplingRate(Fs)

'''
for i in range(0,0):
   #VSE.Set_Group("Group2")         #Create Group
   #VSE.Set_Channel("OFDMVSA","K96")#Create Channel 
   VSE.Set_Input("File")            #FILE|RF
   VSE.Set_InputFile(IQFile)
   VSE.Set_Freq(Freq+i*CC_Size)
   VSE.Set_File_K96Config(OFDMCfg)
   VSE.Set_SweepCont(0)             #Single Sweep
'''

##########################################################
### Make Measurement
##########################################################

### Set Frequency
SMW.Set_Freq(Freq)
FSW.Set_Freq(Freq)

FSW.Get_IQ_Data()                   #Take single sweep
VSE.Set_InitImm()
EVM_Meas = VSE.Get_EVM_Params()     #Attn; RefLvl; Pwr; EVM
print(EVM_Meas)                 
VSE.VISA_ClrErr()                   #Clear Errors

