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
   ### SMW 5GNR Settings
   #####################################################################
   def Set_5GNR_Direction(self,sDirection):
      ### UP| DOWN
      if (sDirection == "UL") or (sDirection == "UP"):
         self.write(':SOUR1:BB:NR5G:LINK UP')
         self.ldir = sDirection

      elif (sDirection == "DL") or (sDirection == "DOWN"):
         self.write(':SOUR1:BB:NR5G:LINK DOWN')
         self.ldir = sDirection
      else:
         print("Set_5GNR_Direction must be UL or DL")

   def Set_5GNR_ChannelBW(self,iBW):
      ### BW in MHz
      ### 5GNR-->NODE-->Carriers-->Channel BW
      self.write(':SOUR1:BB:NR5G:NODE:CELL0:CBW BW%d'%iBW)

   def Set_5GNR_SubSpace(self,iSubSp):
      ### 5GNR-->NODE-->TxBW-->Use
      self.write(':CONF:NR5G:UL:SUBF0:ALL:RBOF %d'%iSubSp) 

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
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported 
   SMW = VSG()
#   SMW.jav_Open("192.168.1.114","Test.csv")
   SMW.jav_Open("127.0.0.1")
#   SMW.Set_Freq(6e9)
