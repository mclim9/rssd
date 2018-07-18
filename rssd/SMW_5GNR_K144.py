#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator 5G NR Functions
### Author : Martin C Lim
### Date   : 2018.02.01
### Requird: python -m pip install rssd
#####################################################################
import SMW_Common

class VSG(SMW_Common.VSG):
   def __init__(self):
      super(VSG,self).__init__()    #Python2/3
      self.Model = "SMW"
      
   #####################################################################
   ### SMW 5GNR Common
   #####################################################################
   def Set_5GNR_Direction(self,sDirection):
      ### UP| DOWN
      if (sDirection == "UL") or (sDirection == "UP"):
         self.write(':SOUR1:BB:NR5G:LINK UP')
         self.ldir = "UL"

      elif (sDirection == "DL") or (sDirection == "DOWN"):
         self.write(':SOUR1:BB:NR5G:LINK DOWN')
         self.ldir = "DL"
      else:
         print("Set_5GNR_Direction must be UL or DL")

   def Set_5GNR_ChannelBW(self,iBW):
      ### BW in MHz
      ### 5GNR-->NODE-->Carriers-->Channel BW
      self.write(':SOUR1:BB:NR5G:NODE:CELL0:CBW BW%d'%iBW)

   def Set_5GNR_ResourceBlock(self,iRB):
      ### 5GNR-->Scheduling-->PUSCH-->No. RBs
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      #self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBN %d'%iRB)
      self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBN 273')

   def Set_5GNR_ResourceBlockOffset(self,iRBO):
      ### 5GNR-->Scheduling-->PUSCH-->No. RBs
      #self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBOF %d'%iRBO)
      self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:RBOF 0')

   def Set_5GNR_Modulation(self,iMod):
      ### 5GNR-->Scheduling-->PUSCH-->Config-->MOdulation
      self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL0:MOD QPSK')

   #####################################################################
   ### FSW 5GNR Settings
   #####################################################################

   def Get_5GNR_UL_BWP_Count(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:NBWP?')
      return rdStr
      
   def Get_5GNR_UL_BWP_ResourceBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:RBN?')
      return rdStr
      
   def Get_5GNR_UL_BWP_ResourceBlockOffset(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:RBOF?')
      return rdStr      
      
   def Get_5GNR_UL_BWP_SlotNum(self):
      ### Number of slots
      rdStr = self.query(':CONF:NR5G:UL:CC:FRAM:BWP0:SCO?')
      return rdStr
      
   def Get_5GNR_UL_BWP_Slot_Modulation(self):
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:MOD?')
      return rdStr
      
   def Get_5GNR_UL_BWP_Slot_ResourceBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:RBN?')
      return rdStr
      
   def Get_5GNR_UL_BWP_Slot_ResourceBlockOffset(self):
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:RBOF?')
      return rdStr
      
   def Get_5GNR_UL_BWP_Slot_SymbNum(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:SYMN?')
      return rdStr
      
   def Get_5GNR_UL_BWP_Slot_SymbOff(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL1:SYM?')
      return rdStr
      
   def Get_5GNR_UL_ChannelBW(self):
      ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
      rdStr = self.query(':SOUR1:BB:NR5G:NODE:CELL0:CBW?')
      return rdStr
      
   def Get_5GNR_UL_SubSpace(self):
      rdStr = self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S30K:USE?')
      rdStr = self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S60K:USE?')
      return rdStr
      
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported 
   SMW = VSG()
   SMW.jav_Open("192.168.1.114")
   print(SMW.Get_5GNR_UL_ChannelBW())
   print(SMW.Get_5GNR_UL_SubSpace())
   print(SMW.Get_5GNR_UL_BWP_Count())
   print(SMW.Get_5GNR_UL_BWP_ResourceBlock())
   print(SMW.Get_5GNR_UL_BWP_ResourceBlockOffset())   
   print(SMW.Get_5GNR_UL_BWP_SlotNum())

   print(SMW.Get_5GNR_UL_BWP_Slot_Modulation())
   print(SMW.Get_5GNR_UL_BWP_Slot_ResourceBlock())
   print(SMW.Get_5GNR_UL_BWP_Slot_ResourceBlockOffset())
   print(SMW.Get_5GNR_UL_BWP_Slot_SymbNum())
   print(SMW.Get_5GNR_UL_BWP_Slot_SymbOff())
