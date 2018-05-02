##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Multiple CC K96 Example
### Author:  mclim
### Date:    2018.05.01
##########################################################
### User Entry
##########################################################
VSE_IP = '127.0.0.1'                  #Get local machine name
FSW_IP = '192.168.1.109'
Freq = 29e6
CC_Size = 100e6

##########################################################
### Code Start
##########################################################
import driver.VSE_K96

##########################################################
### Setup 
##########################################################
VSE = driver.VSE_K96.VSE()          #Create VSE Object
VSE.VISA_Open(VSE_IP)               #Connect to VSE
#VSE.Set_FSWIPAdd(FSW_IP)            #Define FSW_IP
VSE.Set_Init_K96()                  #Change Channel
VSE.Set_DisplayUpdate("ON")         #Display On

for i in range(0,0):
   #VSE.Set_Group("Group2")             #Create Group
   #VSE.Set_Channel("OFDMVSA")          #Create Channel
   #VSE.Set_Channel("OFDMVSA","K962")   #Create Channel 
   VSE.Set_Input("File")
   VSE.Set_InputFile("")
   VSE.Set_Freq(Freq+i*CC_Size)
   VSE.Set_ConfigFile("C:\\Users\\LIM_M\\ownCloud\\ATE\\00_Code\\RS_ATE_Python2\\utils\\BBAnalog_1CC_100RB_64QAM_IQ-17symC.xml")
   VSE.Set_SweepCont(0)                #Single Sweep

##########################################################
### Measure
##########################################################
VSE.Set_InitImm()                   #Take single sweep
VSE.EVM_Wait()                      #Wait for EVM ready
EVM_Meas = VSE.Get_EVM_Params()
print(EVM_Meas)
VSE.VISA_ClrErr()
 

