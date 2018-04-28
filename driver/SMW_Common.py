#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator Common Functions
### Author:  Martin C Lim
### Date:    2018.02.01
### Requird: python -m pip install pyvisa
###          libVISA_class
import yaVISA

class VSG(yaVISA.RSVisa):
   def __init__(self):
      pass
      
   #####################################################################
   ### SMW Arb
   #####################################################################
   def Set_ArbNextSeg(self,num):
      K2.query('BB:ARB:WSEG:NEXT %d;*OPC?'%d)

   def Set_ArbState(self,sState):
      K2.query('BB:ARB:STATE %s;*OPC?'%sState)

   def Set_ArbWv(self,InWv):
       K2.query('BB:ARB:WAV:SEL "%s"; *OPC?'%InWv)
      
   def Set_ArbSeg(self,Seg):
       K2.write('SOUR:BB:ARB:WSEG:NEXT %d'%Seg)
       K2.write('SOUR:BB:ARB:WSEG:NEXT:EXEC')

   def Get_ArbClockFreq(self):
      SCPI = K2.query('SOUR:BB:ARB:CLOC?')
      return float(SCPI)

   def Get_ArbTime(self):
      Fs = Get_ArbClockFreq()
      Points = K2.query('BB:ARB:WAV:POIN?').strip()
      WvTime = int(Points)/int(Fs)
      return WvTime
      
   #####################################################################
   ### SMW Generic
   #####################################################################
   def Init_Wideband(self):
      K2.write('SOUR:POW:ATT:DIG 3')         #Set Digital Attenuation
      K2.write('POW:ALC:STATE AUTO')         #Turn ALC ON|OFF|OFFT|AUTO|
      K2.write('SOUR:POW:ALC:DAMP AUTO')     #Turn Driver AMP ON|OFF|AUTO
      K2.write('SOUR:BB:IQG DB8')            #Baseband IQ gain
      
      ## Not so critical
      K2.write('SOUR:AWGN:STAT 0')           #Turn AWGN off (default)
      K2.write('BBIN:STAT OFF')              #Turn BB Input off(default)

   def Set_Freq(self,freq):
      K2.write(':SOUR1:FREQ:CW %f'%freq);    #RF Freq

   def Set_RFPwr(self,fPow):   #fPow
      K2.write('SOUR:POW %f'%fPow);          #RF Pwr
      
   def Set_RFState(self,sState):
      K2.query('OUTP %s;*OPC?'%sState)

   def Set_DriveAmp(self,sState):
      ### ON, OFF, AUTO, FIX, 
      K2.query('SOUR:POW:ALC:DAMP %s;*OPC?'%sState)
      

   #####################################################################
   ### Verizon 5G
   #####################################################################
   def Set_V5GState(self,sState):
      K2.write('SOUR1:BB:V5G:STAT %s;*OPC?'%sState)

   def Set_V5G_Wave(self,sWaveform):
      ### sWaveform = Uplink_Config_1
      K2.query('SOUR1:BB:V5G:SETT:PCON "%s";*OPC?'%sWaveform)
      #K2.write('SOUR1:BB:V5G:SETT:PCON "%s"'%sWaveform)


#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported
   SMW = VSG()
   SMW.VISA_Open("192.168.1.114")
   SMW.Set_RFPwr(-10)
