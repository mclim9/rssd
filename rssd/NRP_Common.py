#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: NRP Power Sensor
### Author : Martin C Lim
### Date   : 2018.05.18
### Requird: python -m pip install pyvisa
#####################################################################
from yaVISA import jaVisa

class PMr(jaVisa,object):
   def __init__(self):
      try:
         super().__init__()            #Python3
      except:
         super(PMr,self).__init__()    #Python2
      self.Model = "NRP"
      
   #####################################################################
   ### NRP Common
   #####################################################################
   def Set_Freq(self,fFreq):
      self.query('SENS:FREQ %f;*OPC?'%fFreq)

   def Get_Power(self):
      self.write('UNIT:POW DBM')
      self.write('SENS:FUNC "POW:AVG"')
      self.query('INIT:IMM;*OPC?')        
      ReadPwr = self.query('FETCH?')
      return ReadPwr
      
   def Set_PowerOffset(self,fOffset):
      self.write('SENS:CORR:OFFS:STAT ON')
      self.write('SENS:CORR:OFFS %f'%fOffset)

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported
   NRP = PMr()
   NRP.jav_Open("192.168.1.114","Test.csv")
   NRP.Set_Freq(6e9)
