#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Yet(Just) Another VISA wrapper
### Author:  Martin C Lim
### Date:    2017.09.01
### Requird: python -m pip install pyvisa
### Descrip: Wrapper for common VISA commands
###          properties for: Make; Model; Version; IDN; last error
###          logSCPI --> file for 
#####################################################################
import visa
import time
import rssd.FileIO

class jaVisa():    
   ### Rohde & Schwarz VISA Class
   ### Instrument Common functions. 
   def __init__(self):
      self.dataIDN = ""
      self.filenm  = ""
      self.Make    = ""
      self.Model   = ""
      self.Device  = ""
      self.Version = ""
      self.prnty   = 1
      self.Ofile   = ""
      pass
      
   def jav_Clear(self):
      self.K2.clear()

   def jav_Close(self):
      try:
         errList = self.jav_ClrErr()
         self.K2.close()
         return errList
      except:
         pass

   def jav_ClrErr(self):
      ErrList = []
      while True:
         RdStr = self.query("SYST:ERR?").strip()
         ErrList.append(RdStr)
         RdStrSplit = RdStr.split(',')
         if RdStr == "<notRead>": break      #No readstring
         if RdStrSplit[0] == "0": break      #Read 0 error
         self.dLastErr = RdStr
         print("jav_ClrErr: %s-->%s"%(self.Model,RdStr))
      return ErrList 
         
   def jav_IDN(self):
      self.dataIDN = "Temp"                  #Temp for self.query
      self.dataIDN = self.query("*IDN?").strip()
      if self.dataIDN != "<notRead>":        #Data Returned?
         IDNStr = self.dataIDN.split(',')
         self.Make    = IDNStr[0]
         self.Model   = IDNStr[1]
         self.Device  = IDNStr[2]
         self.Version = IDNStr[3]
      else:
         self.dataIDN = ""                   #Reset if not read 
      print('jav_IDN   : %s'%(self.dataIDN))
      return self.dataIDN
            
   def jav_OPC_Wait(self, InCMD):
      start_time = time.time()
      self.write("*ESE 1")		               #Event Status Enable
      self.write("*SRE 32")		            #ServiceReqEnable-Bit5:Std Event
      self.write(InCMD + ";*OPC")	         #Initiate Read.  *OPC will trigger ESR
      #print ('   OPC Wait: ' +InCMD)
      read = "0"
      while (int(read) & 1) != 1:            #Loop until done
         try:
            read = self.query("*ESR?").strip()#Poll EventStatReg-Bit0:Op Complete		
         except:
            print("jav_OPCWai:*ESR? Error")
         time.sleep(0.5)
         delta = (time.time() - start_time)
         if delta > 300:
            print("jav_OPCWai: timeout")
            break
      print('jav_OPCWai: %0.2fsec'%(delta))
      
   def jav_Error(self):
      RdStr = self.query("SYST:ERR?").strip().split(',')
      return RdStr
      
   def jav_Open(self, IPAddr, fily=''):
      #*****************************************************************
      #*** Open VISA Connection
      #*****************************************************************
      #  VISA: 'TCPIP0::'+IP_Address+'::INSTR'
      #  VISA: 'TCPIP0::'+IP_Address+'::inst0'
      #  VISA: 'TCPIP0::'+IP_Address+'::hislip0'
      #  VISA: 'TCPIP0::'+IP_Address+'::hislip0::INSTR'
      rm = visa.ResourceManager()      #Create Resource Manager
      rmList = rm.list_resources()     #List VISA Resources
      try:
         self.K2 = rm.open_resource('TCPIP::'+IPAddr+'::inst0::INSTR')   #Create Visa Obj
         self.K2.timeout = 5000                  #Timeout, millisec
         self.jav_IDN()
         try:
            if fily != "":
               f=open(fily,'a')
               f.write(self.dataIDN + "\n")
               f.close()
         except:
            pass
         self.jav_ClrErr()
      except:
         #***********************************************************
         #*** VISA Failed/Try Socket
         #***********************************************************
         print ('jav_OpnErr: ' + IPAddr)
         self.K2 = 'NoVISA'
      return self.K2

   def jav_Reset(self):
      self.write("*RST;*CLS;*WAI")

   def jav_LogSCPI(self):
      self.f = rssd.FileIO.FileIO()
      self.Ofile = "yaVISA"
      DataFile = self.f.Init("yaVISA")

   def jav_ResList(self):
      try:
         rm = visa.ResourceManager()      #Create Resource Manager
         rmList = rm.list_resources()     #List VISA Resources
      except:
         rmList =["No VISA"]
      return rmList

   def jav_read_raw(self):
      return self.K2.read_raw()

   def jav_Super(self,SCPIList):
      ### Send SCPI list & Query if "?" 
      ### Collect read results into a list for return.
      OutList = []
      for cmd in SCPIList:
         if cmd.find('?') == -1:
            self.write(cmd)
         else:
            ReadStr = self.query(cmd)
            OutList.append(ReadStr)
      return OutList
      
   def query(self,cmd):
      read ="<notRead>"
      try:
         if self.dataIDN != "": 
            read = self.K2.query(cmd).strip()   #Write if connected
      except:
         if self.prnty: print("jav_RdErr : %s-->%s"%(self.Model,cmd))
      if self.Ofile != "" : self.f.write("%s,%s,%s,"%(self.Model,cmd,read))
      return read
      
   def write(self,cmd):
      try:
         if self.dataIDN != "": self.K2.write(cmd) #Write if connected
      except:
         if self.prnty: print("jav_WrtErr: %s-->%s"%(self.Model,cmd))
      if self.Ofile != "" : self.f.write("%s,%s"%(self.Model,cmd))      

if __name__ == "__main__":
   RS = jaVisa()
   #RS.jav_LogSCPI()
   #RS.jav_Open("127.0.0.1")
   RS.jav_Open("192.168.1.109")
   RS.write("FREQ:CENT 13MHz")
   print(RS.Device)
   print(RS.jav_Close())
