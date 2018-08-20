#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: AAA Common Functions
### Author : Martin C Lim
### Date   : 2018.08.08
### Strctr : pyvisa-->yavisa-->AAA_Common.py
#####################################################################
from rssd.yaVISA import jaVisa

class AAA(jaVisa):
   def __init__(self):
      super(AAA, self).__init__()
      self.Model = "AAA"
      
   #####################################################################
   ### AAA Display
   #####################################################################
   def Get_Channels(self):
      ChList = self.query('INST:LIST?').split(',')
      return(ChList)
      
   def Set_DisplayUpdate(self,state):
      # Param: ON|OFF
      self.write('SYST:DISP:UPD %s'%state);     #Display Update State
       
   #####################################################################
   ### AAA Common Functions
   #####################################################################
   def Set_Freq(self,fFreq):
      self.write(':SENS:FREQ:CENT %.0f HZ'%fFreq);         #RF Freq

   def Set_VidBW(self,fFreq):
      if fFreq == 0:
         self.write(':SENS:BAND:VID:AUTO ON');
      else:
         self.write(':SENS:BAND:VID %f'%fFreq);
      
   #####################################################################
   ### AAA Common Query
   #####################################################################
   def Get_ACLR(self):
      ACLR = self.query(':CALC:MARK:FUNC:POW:RES? MCAC').split(',')
      return ACLR

   def Get_ChPwr(self):
      out = self.queryFloat('FETC:SUMM:POW?')
      return out 
      
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   AAA_Inst = AAA()
   AAA_Inst.jav_Open("192.168.1.100")
   AAA_Inst.jav_IDN()
   AAA_Inst.jav_ClrErr()
