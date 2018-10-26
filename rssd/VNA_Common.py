#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Network Analyzer Common Functions
### Author : Martin C Lim
### Date   : 2018.10.15
### Requird: python -m pip install pyvisa
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

class VNA(jaVisa):
   def __init__(self):
      super(VNA,self).__init__()    #Python2/3
      self.Model = "xxx"
   
   #####################################################################
   ### VNA Functions Alphabetical
   #####################################################################
   def Get_Trace_Names(self,dChan=1):
      rdStr = self.write(":CALC%d:PAR:CAT?"%(dChan))
      return rdStr
      
   def Get_Trace_Save(self,dChan,sFName):
      self.write(":MMEM:STOR:TRAC:PORT %d,'%s.s4p',COMP,1,2,3,4"%(dChan,sFName))
      #self.write(":MMEM:STOR:TRAC:PORT %d,'%s.s2p',COMP,1,2"%(dChan,sFName))

   def Set_Cal_Group(self,sName,dChan=1):
      #sName should end in '.cal'
      if not sName.lower().endswith(".cal"):
         sName += ".cal"
      self.write(":MMEM:LOAD:CORR:RES %d,%s"%(dChan,sName))    #Resolve Cal Group
      self.write(":MMEM:LOAD:CORR %s"%(sName))                 #Load cal group.

   def Set_Cal_Group_Disolve(self):
      self.write(":MMEM:LOAD:CORR:RES")

   def Set_Call_Save(self, sName, dChan=1):
      if not sName.lower().endswith(".cal"):
         sName += ".cal"
      self.write(":MMEM:STOR:CORR d,'%s'"%(dChan,sName))

   def Set_Channel(self,dChan,sName=""):
      ##################################################################
      ### SANALYZER, IQ, PNOISE, NOISE, Spur, ADEM, V5GT, LTE, OFDMVSA
      ##################################################################
      if sName == "":
         sName = Chan
      ChList = self.query(":CALC%d:PAR:CAT?"%(dChan)).split(",")
      #print("Chan:%s in %s"%(Chan,ChList))
      if ("'%s'"%sName) in ChList:
         pass
      else:
         self.query(":INST:CRE %s,'%s';*OPC?"%(dChan,sName))
      self.query(":INST:SEL '%s';*OPC?"%sName)
      
   def Set_FreqStart(self,fFreq,dChan=1):
      self.write(":SENS%d:FREQ:STAR %f"%(dChan,fFreq))

   def Set_FreqStep(self,fFreq,dChan=1):
      self.write(":SENS%d:FREQ:STEP %f"%(dChan,fFreq))   #RF Freq

   def Set_FreqStop(self,fFreq,dChan=1):
      self.write(":SENS%d:FREQ:STOP %f"%(dChan,fFreq))   #RF Freq

   def Set_IFBW(self,fFreq,dChan=1):
      self.write("SENS%d:BAND %f"%(dChan,fFreq))
      
   def Set_InitImm(self,dChan=1):
      self.query("INIT%d:IMM*OPC?"%(dChan))
        
   def Set_PowerStart(self,fPwr,dChan=1):
      self.write(":SOUR%d:POW:STAR %f dBm"%(dChan,fPwr))

   def Set_PowerStep(self,fPwr,dChan=1):
      self.write(":SOUR%d:POW:STEP %f dBm"%(dChan,fPwr))

   def Set_PowerStop(self,fPwr,dChan=1):
      self.write(":SOUR%d:POW:STOP %f dBm"%(dChan,fPwr))

   def Set_SweepCont(self,iON,dChan=1):
      if iON == 1:
         self.write("INIT%d:CONT ON")                    #Continuous Sweep
      else:
         self.write("INIT%d:CONT OFF")                   #Single Sweep

   def Set_SweepPoints(self,dPoints,dChan=1):
      self.write(":SENS%d:SWE:POIN %d"%(dChan,dPoints))  #RF Freq

   def Set_SweepTime(self,fSwpTime,dChan=1):
      self.write("SENS%d:SWE:TIME %f"%(dChan,fSwpTime))  #Sweep/Capture Time

   def Set_Trace_Add(self,dChan=1):
      rdStr = self.write("CALC%d:PAR:SDEF")
      return rdStr
      
   def Set_Trace_Avg(self,sType,dChan=1):
      self.write("DISP:TRAC%d:MODE AVER"%dTrace)
      self.write("SENS:DET1:FUNC AVER")
      self.write("SENS:AVER:TYPE %s"%sType)  #LIN|VID

   def Set_Trace_AvgCount(self,iAvg,dChan=1):
      self.write("SENS%d:SWE:COUN %d"%(dChan,iAvg))

   def Set_Trace_DelAll(self,sMeas,dChan=1):
      self.write("CALC:PAR:DEL:ALL")

   def Set_Trace_MeasAdd(self,sMeas,dChan=1):
      # S11/S21/S12/S22 ..... Sxxyy
      # Y11/Y21/Y12/Y22 ..... Yxxyy
      # A1G2/A1G4/A2G1  ..... A<port>G<port>
      # B1G2/B1G4/B2G1  ..... B<port>G<port>
      # IP3UI/IP3UO     ..... IP<order:3|5|7|9><side:U|L><DUT:I|O>
      sTrcName = Set_Trace_Add()
      self.write("CALC%d:PAR:SDEF '%s','%s'"%(dChan,sTrcName,sMeas))

   def Set_Trace_MeasAdd_AWave(self,APort,GenPort,dChan=1):
      self.Set_Trace_MeasAdd("A%dG%d"%(PortA,GenPort,dChan))

   def Set_Trace_MeasAdd_BWave(self,BPort,GenPort,dChan=1):
      self.Set_Trace_MeasAdd("B%dG%d"%(BPort,GenPort,dChan))

   def Set_Trace_MeasAdd_SParam(self,Port1,Port2,dChan=1):
      self.Set_Trace_MeasAdd("S%d%d"%(Port1,Port2,dChan))

   def Set_Trace_MeasAdd_IMD3(self,dChan=1):
      self.write("SENS%d:FREQ:IMOD:ORD3 ON"%(dChan))
      self.Set_Trace_MeasAdd("IP3UI"%(dChan))
      self.Set_Trace_MeasAdd("IP3LI"%(dChan))

   def Set_Trace_MeasDel(self,sTrcName,dChan=1):
      self.write("CALC%d:PAR:DEL '%s'"%(dChan,sTrcName))

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   # this won't be run when imported
   ZVA = VNA().jav_openvisa('TCPIP0::localhost::5025::SOCKET')
#   ZVA.Set_Freq(6e9)
   ZVA.jav_Close()
