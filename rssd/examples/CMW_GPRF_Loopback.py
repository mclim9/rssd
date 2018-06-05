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
BaseDir = os.path.dirname(os.path.realpath(__file__))
OutFile = BaseDir + "\\data\\" + __file__
InpFile = BaseDir + "\\data\\" + __file__ + ".csv"

visa = '127.0.0.1'               #Get local machine name
freqArry = [1e9, 2e9, 3e9, 4e9, 5e9]

##########################################################
### Code Start
##########################################################
from rssd.FileIO     import FileIO
from rssd.CMW_GPRF   import BSE
from datetime        import datetime

f = FileIO()
IArry = f.initread(InpFile).readcsv()
OFile = f.Init(OutFile)

CMW = BSE()
CMW.jav_Open("127.0.0.1")
CMW.Set_Sys_TxPortLoss(1,10)
CMW.Set_Sys_TxPortLoss(2,30)
CMW.Set_Sys_RxPortLoss()
CMW.Init_VSG()

for i in range(1,3):
   for cond in IArry:
      CMW.Set_Gen_PortON(i)
      tick = datetime.now()
      CMW.Set_Gen_RFPwr(cond[0]-50)
      CMW.Set_Gen_Freq(cond[0])
      CMW.Set_Gen_RFState("ON")

      CMW.Init_Power(i)
      CMW.Set_VSA_Freq(cond[0])
      CMW.Set_VSA_RefLevl(cond[1])
      tock = datetime.now()
      OutStr = '%f,%f,%d,%s'%(freq,CMW.Get_ChPwr()[1],i,tock-tick)
      OFile.write (OutStr)
      Set_Gen_PortOFF(i)
   #end freq loop
#end port loop   

CMW.jav_ClrErr()
CMW.jav_Close()
OFile.close()
