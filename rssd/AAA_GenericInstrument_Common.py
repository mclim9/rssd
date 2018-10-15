#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: AAA Common Functions
### Author : Martin C Lim
### Date   : 20xx.xx.xx
###  _____  _____   ____ _______ ____ _________     _______  ______ 
### |  __ \|  __ \ / __ \__   __/ __ \__   __\ \   / /  __ \|  ____|
### | |__) | |__) | |  | | | | | |  | | | |   \ \_/ /| |__) | |__   
### |  ___/|  _  /| |  | | | | | |  | | | |    \   / |  ___/|  __|  
### | |    | | \ \| |__| | | | | |__| | | |     | |  | |    | |____ 
### |_|    |_|  \_\\____/  |_|  \____/  |_|     |_|  |_|    |______|
###                         _            _           _ 
###                        | |          | |         | |             
###             _   _ _ __ | |_ ___  ___| |_ ___  __| |
###            | | | | '_ \| __/ _ \/ __| __/ _ \/ _` |
###            | |_| | | | | ||  __/\__ \ ||  __/ (_| |
###             \__,_|_| |_|\__\___||___/\__\___|\__,_|
###
#####################################################################
from rssd.yaVISA import jaVisa

class AAA(jaVisa):
   def __init__(self):
      super(AAA, self).__init__()
      self.Model = "AAA"
      
   #####################################################################
   ### AAA Functions Alphabetical
   #####################################################################
   def Get_ACLR(self):
      ACLR = self.query(':CALC:MARK:FUNC:POW:RES? MCAC').split(',')
      return ACLR

   def Get_ChPwr(self):
      out = self.queryFloat('FETC:SUMM:POW?')
      return out 

   def Get_Channels(self):
      ChList = self.query('INST:LIST?').split(',')
      return(ChList)
      
   def Init_Measurement(self):
      #Configure instrument measurment
      
   def Set_DisplayUpdate(self,state):
      # Param: ON|OFF
      self.write('SYST:DISP:UPD %s'%state);     #Display Update State
       
   def Set_Freq(self,fFreq):
      self.write(':SENS:FREQ:CENT %.0f HZ'%fFreq);         #RF Freq

   def Set_VidBW(self,fFreq):
      if fFreq == 0:
         self.write(':SENS:BAND:VID:AUTO ON');
      else:
         self.write(':SENS:BAND:VID %f'%fFreq);
      
#####################################################################
### Run if Main  (Won't run when imported)
#####################################################################
if __name__ == "__main__":
   AAA_Inst = AAA()
   AAA_Inst.jav_Open("192.168.1.100")
   AAA_Inst.jav_IDN()
   AAA_Inst.jav_ClrErr()
