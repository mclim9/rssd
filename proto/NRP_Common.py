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
      outp = self.query(':SENS:FREQ?')
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
      self.write('INIT:IMM')        
      outp = self.queryFloat('FETCH?')
      return outp

   def Get_PowerAll(self):
      ### NRP3M
      self.write('UNIT:POW DBM')
#      self.write('SENS:FUNC "POW:AVG"')
      self.write('SENS:CHAN1:ENAB ON')
      self.write('SENS:CHAN2:ENAB ON')
      self.write('SENS:CHAN3:ENAB ON')
      self.query('INIT:IMM;*OPC?')
      outp = self.queryFloat('FETCH:ALL?')
      return outp
      
   def Set_PowerOffset(self,fOffset):
      self.write('SENS:CORR:OFFS:STAT ON')
      self.write('SENS:CORR:OFFS %f'%fOffset)

   def Set_PowerOffsetState(self,bState):
      if bState == 0:
         self.write('SENS:CORR:OFFS:STAT OFF')
      else:
         self.write('SENS:CORR:OFFS:STAT ON')

   def Set_InitImm(self):
      self.query('INIT:IMM;*OPC?')
      

#####################################################################
### NRPM3M 0x0195
#####################################################################
   def Set_Sys_LED(self,bState,iSensor=1):
      if bState == 1:
         self.write('SYST:LED:CHAN%d:COL 255'%iSensor)
      else:
         self.write('SYST:LED:CHAN%d:COL 0'%iSensor)
               
#####################################################################
### NRPM3M 0x0195
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
         self.write('SYST:LED:CHAN%d:COL 255'%iSensor)
      else:
         self.write('OUTP%d:STAT OFF'%iSensor)
         self.write('SYST:LED:CHAN%d:COL 0'%iSensor)
         
   def Get_Gen_Freq(self):
      self.write('SOUR:FREQ?')

   def Set_Gen_Freq(self,fFreq):
      self.write('SOUR:FREQ %f'%fFreq)

   def Set_Gen_EIRP(self,bState):
      self.query('FETC?')
      
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported
   NRP = PMr()
#   NRP.jav_Open("192.168.1.114","Test.csv")
   NRP.jav_openvisa("USB0::0x0AAD::0x0196::900105::INSTR")
#   NRP.jav_logscpi()
   NRP.jav_Reset()
   NRP.Set_Freq(24e9)

   print(NRP.Get_PowerAll())        #Power Before SG on
   for i in range(1,4):
      NRP.Set_Gen_MasterPwr(1,i)
      NRP.Set_Gen_RFPwr(1,i)
      NRP.Set_Gen_Freq(24e9)
      NRP.Get_Gen_Freq()
      print(NRP.Get_PowerAll())        #Power SG on 
      NRP.Set_Gen_RFPwr(0,i)
      NRP.Set_Gen_MasterPwr(0,i)
   NRP.jav_Close()
