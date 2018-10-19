#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator 5G NR Functions
### Author : Martin C Lim
### Date   : 2018.02.01
### Requird: python -m pip install rssd
#####################################################################
from rssd.SMW_Common import VSG

class VSG(VSG):
   def __init__(self):
      super(VSG,self).__init__()    #Python2/3
      self.Model = "SMW"
      self.ldir = "UL"
      self.BWP = 0
      self.User = 0
      
   #####################################################################
   ### SMW 5GNR Get Methods
   #####################################################################
   def Get_5GNR_BWP_Center(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:DFR?'%(self.sdir))
      return rdStr
      
   #####################################################################
   ### FSW 5G NR DMRS
   #####################################################################
   def Get_5GNR_BWP_Ch_DMRS_1stDMRSSym(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:PUSC:DMRS:APOS?'%(self.alloc))
      rdStr = "<TBD>"
      return rdStr

   def Get_5GNR_BWP_Ch_DMRS_AddPosition(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:PUSC:DMRS:IND?'%(self.alloc))
      rdStr = "<TBD>"
      return rdStr

   def Get_5GNR_BWP_Ch_DMRS_Config(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:PUSC:DMRS:CONF?'%(self.alloc))
      rdStr = "<TBD>"
      return rdStr

   def Get_5GNR_BWP_Ch_DMRS_Mapping(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:PUSC:DMRS:MAPT?'%(self.alloc))
      rdStr = "<TBD>"
      return rdStr

   def Get_5GNR_BWP_Ch_DMRS_MSymbLen(self):
      rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:PUSC:DMRS:LENG?'%(self.alloc))
      return rdStr

   def Get_5GNR_BWP_Ch_DMRS_RelPwr(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:PUSC:DMRS:APOS?')
      rdStr = "<TBD>"
      return rdStr

   def Get_5GNR_BWP_Ch_DMRS_SeqGenMeth(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:PUSC:DMRS:APOS?')
      rdStr = "<TBD>"
      return rdStr

   def Get_5GNR_BWP_Ch_DMRS_SeqGenSeed(self):
      #rdStr = self.query(':SOUR:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:PUSC:DMRS:APOS?')
      rdStr = "<TBD>"
      return rdStr

   def Get_5GNR_BWP_Ch_Modulation(self):
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:MOD?'%(self.alloc))
      return rdStr
      
   def Get_5GNR_BWP_Ch_ResBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:RBN?'%(self.alloc))
      return rdStr
      
   def Get_5GNR_BWP_Ch_ResBlockOffset(self):
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:RBOF?'%(self.alloc))
      return rdStr
      
   def Get_5GNR_BWP_Ch_SymbNum(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:SYMN?'%(self.alloc))
      return rdStr
      
   def Get_5GNR_BWP_Ch_SymbOff(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:SYM?'%(self.alloc))
      return rdStr
      
   def Get_5GNR_BWP_Count(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:NBWP?'%(self.sdir))
      return rdStr      

   def Get_5GNR_BWP_ResBlock(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:RBN?'%(self.sdir))
      return rdStr

   def Get_5GNR_BWP_ResBlockOffset(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:RBOF?'%(self.sdir))
      return rdStr      
      
   def Get_5GNR_BWP_SlotNum(self):
      ### Number of slots
      rdStr = self.query(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:SLOT?'%(self.alloc))
      return rdStr
      
   def Get_5GNR_BWP_SubSpace(self):
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:SCSP?'%(self.sdir))
      return rdStr

   def Get_5GNR_BWP_SubSpaceTotal(self):
      rdStr = []
      rdStr.append(self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S15K:NRB?'))
      rdStr.append(self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S30K:NRB?'))
      rdStr.append(self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S60K:NRB?'))
      rdStr.append(self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S120K:NRB?'))
      return rdStr
      
   def Get_5GNR_ChannelBW(self):
      ### 5;10;15;20;25;30;40;50;60;70;80;90;100;200;400
      rdStr = self.query(':SOUR1:BB:NR5G:NODE:CELL0:CBW?')
      return rdStr

   def Get_5GNR_RefA(self):
      rdStr = self.query(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:POIN?')
      return rdStr

   def Get_5GNR_TransPrecoding(self):
      rdStr = self.query(':SOUR1:BB:NR5G:NODE:CELL0:DUMR:TPST?')
      return rdStr

   #####################################################################
   ### FSW 5GNR Settings
   #####################################################################
   def Set_5GNR_BBState(self,iEnable):
      if (iEnable == 1) or (iEnable == 'ON'):
         self.jav_OPC_Wait(':SOUR1:BB:NR5G:STAT 1')
#         self.query('*OPC?')        # Wait for calculation
      else:
         self.write(':SOUR1:BB:NR5G:STAT 0')

   def Set_5GNR_BWP_Ch_Modulation(self,sMod):
      self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:MOD %s'%(self.alloc,sMod))
      
   def Set_5GNR_BWP_Ch_ResourceBlock(self,iRB):
      ### 5GNR-->Scheduling-->PUSCH-->No. RBs
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      #self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:RBN %d'%iRB)
      self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:RBN %d'%(self.alloc,iRB))

   def Set_5GNR_BWP_Ch_ResourceBlockOffset(self,iRBO):
      ### 5GNR-->Scheduling-->PUSCH-->No. RBs
      #self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:RBOF %d'%%(self.alloc,iRBO))
      self.write(':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER0:BWP0:ALL%d:RBOF 0'%(self.alloc))

   def Set_5GNR_BWP_ResBlockMax(self):
      ### RB = (CHBw * 0.95) / (SubSp * 12)
      MaxRB =  20
      rdStr = self.query(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:RBN %d'%(self.sdir,MaxRB))
      return rdStr
      
   def Set_5GNR_BWP_SubSpace(self,iSubSp):
      self.write(':SOUR1:BB:NR5G:NODE:CELL0:TXBW:S%dK:USE 1'%(iSubSp))
      self.write(':SOUR1:BB:NR5G:UBWP:USER0:CELL0:%s:BWP0:SCSP N%d'%(self.sdir,iSubSp))

   def Set_5GNR_ChannelBW(self,iBW):
      ### BW in MHz
      ### 5GNR-->NODE-->Carriers-->Channel BW
      self.write(':SOUR1:BB:NR5G:NODE:CELL0:CBW BW%d'%iBW)

   def Set_5GNR_Direction(self,sDirection):
      ### UP| DOWN
      if (sDirection == "UL") or (sDirection == "UP"):
         self.write(':SOUR1:BB:NR5G:LINK UP')
         self.sdir = "UL"
         self.alloc = 0       #Alloc 0:PUSCH
      elif (sDirection == "DL") or (sDirection == "DOWN"):
         self.write(':SOUR1:BB:NR5G:LINK DOWN')
         self.sdir = "DL"
         self.alloc = 1       #Alloc 0:Coreset 1:PDSCH
      else:
         print("Set_5GNR_Direction must be UP or DOWN")

   def Set_5GNR_FreqRange(self,iRange):
      ### 0:<3GHz 1:3-6GHz 2:>6GHz
      ### LOW; MIDD; HIGH
      if iRange == 'LOW':
         self.write(':SOUR1:BB:NR5G:NODE:CELL0:CARD LT3')
      elif iRange == 'MIDD':
         self.write(':SOUR1:BB:NR5G:NODE:CELL0:CARD BT36')
      elif iRange == 'HIGH':
         self.write(':SOUR1:BB:NR5G:NODE:CELL0:CARD GT6')
         
   def Set_5GNR_Parameters(self,sDir):
      self.Set_5GNR_Direction(sDir)

   
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported 
   SMW = VSG()
   SMW.jav_Open("192.168.1.114")
   SMW.Set_5GNR_FreqRange('LOW')
   SMW.jav_Close()
