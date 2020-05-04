##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Demonstrate CMW100 Gen Purpose RF Loopback
### Author:  mclim
### Date:    2018.05.31 
##########################################################
### User Entry
##########################################################
import os
# import tkMessageBox

BaseDir = os.path.dirname(os.path.realpath(__file__))
OutFile = BaseDir +  __file__
InpFile = BaseDir +  __file__ + ".csv"

visa = '127.0.0.1'                    #Get local machine name
repeat = 1
ports = [1,2,3,4,5,6,7,8]

##########################################################
### Function Definition
##########################################################
def CMW_Set(freq, pwr):
    CMW.Set_Gen_RFPwr(pwr)
    CMW.Set_Gen_Freq(freq)
    CMW.Set_Gen_RFState("ON")

    CMW.Init_MeasPower(i)
    CMW.Set_VSA_Freq(freq)
    CMW.Set_VSA_RefLevl(pwr)

##########################################################
### Code Start
##########################################################
from rssd.FileIO        import FileIO
from rssd.RCT.GPRF      import RCT
from datetime           import datetime

f = FileIO()
f.debug = 0 
IArry = f.initread(InpFile).readcsv()
OFile = f.Init(OutFile)

CMW = RCT()
CMW.jav_Open("127.0.0.1")

for port in ports:
	CMW.Set_Sys_TxPortLoss(port,0)
	CMW.Set_Sys_RxPortLoss(port,0)
CMW.Init_VSG()

OFile.write ('\nDate,Iter,Freq,Pwr,MPwr,Port,Time,Diff')
for r in range (0,repeat):          #Repeatability Loop
    print("Loop%d"%r)
    for cond in IArry:              #Condition Loop
        for i in [2]:               #Port Loop
            freq = float(cond[0])
            pwr  = float(cond[1])
            CMW.Set_Gen_PortON(i)
            tick = datetime.now()
            CMW.Set_Gen_RFPwr(pwr)
            CMW.Set_Gen_Freq(freq)
            CMW.Set_Gen_RFState("ON")

            CMW.Init_MeasPower(i)
            CMW.Set_VSA_Freq(freq)
            CMW.Set_VSA_RefLevl(pwr)
            tock = datetime.now()
            MPwr = CMW.Get_ChPwr()[1]
            OutStr = '%d,%d,%.3f,%.3f,%d,%s,%f'%(r,freq,pwr,MPwr,i,tock-tick,pwr-MPwr)
            OFile.write (OutStr)
            #CMW.Set_Gen_PortOFF(i)
            #exit()
        #end port loop
    #end condition loop
#end repeatability loop
CMW.jav_ClrErr()
CMW.jav_Close()
