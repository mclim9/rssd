##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: FSW/SMW 5G NR Demo
### Author:  mclim
### Date:    2018.09.10
### Descrip: FSW 3.20-18.7.1.0 Beta
###          SMW 4.30 SP2
##########################################################
### User Entry
##########################################################
SMW_IP   = '192.168.1.114'                    #IP Address
FSW_IP   = '192.168.1.109'                    #IP Address
odata =  [[] for i in range(3)]

##########################################################
### Code Start
##########################################################
from rssd.FSW_5GNR_K144    import VSA
from rssd.SMW_5GNR_K144    import VSG
from rssd.FileIO           import FileIO

OFile = FileIO().makeFile(__file__)
SMW = VSG().jav_Open(SMW_IP,OFile)  #Create SMW Object
FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

##########################################################
### Instrument Settings
##########################################################
odata[0].append("               ")
odata[0].append("RefA,MHz       ")
odata[0].append("Ch BW          ")
odata[0].append("TransPrecoding ")
odata[0].append("===User/BWP====")
odata[0].append("SubSpacing     ")
odata[0].append("Num BWP        ")
odata[0].append("BWP_RB         ")
odata[0].append("BWP_RBoff      ")
odata[0].append("====Channel====")
odata[0].append("User_BWP_Mod   ")
odata[0].append("User_BWP_RB    ")
odata[0].append("User_BWP_RBOff ")
odata[0].append("User_BWP_SymNum")
odata[0].append("User_BWP_SymOff")
odata[0].append("User_BWP_Cntr  ")
odata[0].append("=====DMRS======")
odata[0].append("DMRS Config    ")
odata[0].append("DMRS Mapping   ")
odata[0].append("DMRS FirstSym  ")
odata[0].append("DMRS Add Positn")
odata[0].append("DMRS Length    ")
odata[0].append("DMRS SeqGenMeth")
odata[0].append("DMRS SeqGenSeed")
odata[0].append("DMRS Rel Power ")

try:
   SMW.Set_5GNR_Parameters("UL")
   odata[1].append("[[SMW]]")
   odata[1].append(int(SMW.Get_5GNR_RefA())/1e6)
   odata[1].append(SMW.Get_5GNR_ChannelBW()) 
   odata[1].append(SMW.Get_5GNR_TransPrecoding())
   odata[1].append("=User=")
   odata[1].append(SMW.Get_5GNR_BWP_SubSpace())
   odata[1].append(SMW.Get_5GNR_BWP_Count())
   odata[1].append(SMW.Get_5GNR_BWP_ResBlock())
   odata[1].append(SMW.Get_5GNR_BWP_ResBlockOffset())
   odata[1].append("==Ch==")
   odata[1].append(SMW.Get_5GNR_BWP_Ch_Modulation())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_ResBlock())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_ResBlockOffset())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_SymbNum())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_SymbOff())
   odata[1].append(int(SMW.Get_5GNR_BWP_Center())/1e6)
   odata[1].append("=DMRS=")
   odata[1].append(SMW.Get_5GNR_BWP_Ch_DMRS_Config())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_DMRS_Mapping())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_DMRS_AddPosition())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_DMRS_MSymbLen())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed())
   odata[1].append(SMW.Get_5GNR_BWP_Ch_DMRS_RelPwr())
except:
   pass
print(len(odata[1]))
   
try:
   FSW.Init_5GNR()
   FSW.Set_5GNR_Parameters("UL")
   odata[2].append("[[FSW]]")
   odata[2].append(int(FSW.Get_5GNR_RefA())/1e6)
   odata[2].append(FSW.Get_5GNR_ChannelBW())
   odata[2].append(FSW.Get_5GNR_TransPrecoding())
   odata[2].append("=User=")
   odata[2].append(FSW.Get_5GNR_BWP_SubSpace())
   odata[2].append(FSW.Get_5GNR_BWP_Count())
   odata[2].append(FSW.Get_5GNR_BWP_ResBlock())
   odata[2].append(FSW.Get_5GNR_BWP_ResBlockOffset())
   odata[2].append("==CH==")
   odata[2].append(FSW.Get_5GNR_BWP_Ch_Modulation())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_ResBlock())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_ResBlockOffset())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_SymbNum())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_SymbOff())
   odata[2].append(int(FSW.Get_5GNR_BWP_Center())/1e6)
   odata[2].append("=DMRS=")
   odata[2].append(FSW.Get_5GNR_BWP_Ch_DMRS_Config())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_DMRS_Mapping())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_DMRS_AddPosition())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_DMRS_MSymbLen())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed())
   odata[2].append(FSW.Get_5GNR_BWP_Ch_DMRS_RelPwr())
except:
   pass
print(len(odata[2]))

for i in range(len(odata[0])):
   try:
      print("%s\t%s\t%s"%(odata[0][i],odata[1][i],odata[2][i]))
   except: 
      try:
         print("%s\t%s\t%s"%(odata[0][i],odata[1][i],'<not read>'))
      except:
         print("%s\t%s\t%s"%(odata[0][i],'<not read>',odata[2][i]))

SMW.jav_ClrErr()                          #Clear Errors
FSW.jav_ClrErr()                          #Clear Errors
