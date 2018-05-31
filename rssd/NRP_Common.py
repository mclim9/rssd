#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: NRP Power Sensor
### Author : Martin C Lim
### Date   : 2018.05.18
### Requird: python -m pip install pyvisa
### 
### VISAFmt: USB0::0x0AAD::0x0138::100961::INSTR
###          <VS>::<Manu>::<Modl>::<SerN>::INSTR
### 
#####################################################################
from yaVISA import jaVisa

class PMr(jaVisa):
   def __init__(self):
      super(PMr,self).__init__()    #Python2/3
      self.Model = "NRP"
      
   #####################################################################
   ### NRP Common
   #####################################################################
   def Get_Average(self):
      outp = self.queryInt('SENS:AVER:COUN?')
      return outp

   def Set_Average(self,iAvg):
      self.write('SENS:AVER:COUN %d'%iAvg)

   def Set_AverageMode(self,bAuto):
      if bAuto == 0:
         self.write('SENS:AVER:COUN:AUTO OFF')
      else:
         self.write('SENS:AVER:COUN:AUTO ON')

   def Get_Freq(self):
      outp = self.queryFloat(':SENS:FREQ?')
      return outp
      
   def Set_Freq(self,fFreq):
      self.query('SENS:FREQ %f;*OPC?'%fFreq)

   def Get_Offset(self):
      ### Offset = Loss
      ### +Num => +Reading
      ### -Num ==> -Reading
      outp = self.queryFloat('SENS:CORR:OFFS?')
      return outp
      
   def Get_Power(self):
      self.write('UNIT:POW DBM')
      self.write('SENS:FUNC "POW:AVG"')
      self.query('INIT:IMM;*OPC?')        
      outp = self.queryFloat('FETCH?')
      return outp
      
   def Set_PowerOffset(self,fOffset):
      self.write('SENS:CORR:OFFS:STAT ON')
      self.write('SENS:CORR:OFFS %f'%fOffset)

   def Set_PowerOffsetState(self,bState):
      if bState == 0:
         self.write('SENS:CORR:OFFS:STAT OFF')
      else:
         self.write('SENS:CORR:OFFS:STAT ON')

#####################################################################
### NRPM3M Source 0x0156
#####################################################################
   def Set_Gen_MasterPwr(self,bState,iSensor=1):
      ### This cmd sent automatically after 1min to prevent overheating.
      ### retrigger only after 5 minutes.  Damange otherwise.
      if bState == 1:
         self.write('CONT%d:APOW:STAT ON'%iSensor)
      else:
         self.write('CONT%d:APOW:STAT OFF'%iSensor)
         
   def Set_Gen_RFPwr(self,bState,iSensor=1):
      ### Suggested 1:10 duty cycle
      if bState == 1:
         self.write('OUTP%d:STAT ON'%iSensor)
      else:
         self.write('OUTP%d:STAT OFF'%iSensor)
         
   def Get_Gen_Freq(self,bState):
      self.write('SOUR:FREQ?')

   def Get_Gen_Freq(self,bState):
      self.write('SOUR:FREQ?')

   def Set_Gen_InitImm(self):
      self.query('INIT:IMM;*OPC?')
      
   def Set_Gen_EIRP(self,bState):
      self.query('FETC?')
      

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported
   NRP = PMr()
   NRP.jav_Open("192.168.1.114","Test.csv")
   NRP.Set_Freq(6e9)
   NRP.jav_Close()
