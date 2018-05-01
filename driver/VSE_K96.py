#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Explorer K96 Functions
### Author:  Martin C Lim
### Date:    2018.04.27
### Requird: python -m pip install pyvisa
import VSE_Common

class VSE(VSE_Common.VSE):
   def __init__(self):
      pass
      
   #####################################################################
   ### VSE General Settings
   #####################################################################
   def Set_Autolevel(sState):
   K2.write('CONF:POW:AUTO %s;*WAI'%sState);

   def Set_BurstSearch(sState):
      K2.write('DEM:FORM:BURS %s;*WAI'%sState);
      
   def Set_ConfigFile(sFile):
      K2.write('MMEM:LOAD:CFGF "%s";*WAI'%sFile);
   
   def Set_FilterAdjustable(sState):
      K2.write('INP:FILT:CHAN:STAT %s'%sState);	    	
      
   def Set_FSWIPAdd(sIP):
      K2.write('CONF:ADDR "TCPIP::%s"'%sIP);	#FSW IP Address

   def Set_Input(sType):
      K2.write('INP:SEL %s'%sType);	    	#RF|AIQ|DIQ|FILE

   #####################################################################
   ### Helper Functions
   #####################################################################
   def EVM_Wait():
      EVM = '';                              #init EVM read value
      K2.write('INIT:IMM');                  #Start Measurement
      while (EVM == ''):     		  #Loop until EVM present
         try:
            EVM = K2.query('FETC:SUMM:EVM?');
         except:
            pass
      asdf = K2.query('FETC:SUMM:EVM?;*WAI');            #Flush buffer of NaN
     
   def EVM_AutoCal():
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #%%%% Code Settings
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      debug=0;
      Backoff = 0;
      EVM_Wind = -0.1;              #EVM can degrade by this amount.
                                    #EVM Repeatability indicator
      #autostart = tic;
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #%%%% Code Start
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      if debug==1: print('   Autolvl EVM: ');
      Set_Autolevel("ON")
      EVM_Curr = Get_EVM();         #Set initial RefLvl & Attn
      RefLvl = Get_RefLevel()
      MAttn  = Get_AttnMech()
      if debug==1: print ("      Ref:%.2f MAttn:%.0f EVM:%.2f"%(RefLvl, MAttn, EVM_Curr))
      
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #%%%% Attn Sweep
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      if debug==1: print('   Attenu Swp: ');
      EVM_Prev = 1.00; 
      i=0;
      Set_Autolevel("OFF")            #Manually Set RefLvl & Attn
      while (i <= MAttn) & (i < 30):
         MechAttn = MAttn - i;
         Set_AttnMech(MAttn - i)
         EVM_Curr = Get_EVM();
         if debug==1: print ("      Ref:%.2f MAttn:%.0f EVM:%.2f"%(RefLvl, MechAttn, EVM_Curr))
         if EVM_Curr =='NAN':
            print "EVM NAN"
            break

         Diff = EVM_Prev - EVM_Curr;   #Positive = improvedEVM
         if (Diff > EVM_Wind):
            EVM_Prev = EVM_Curr;
            i = i + 1;
         else:
            if debug==1: print("      Break")
            i = i - 1;                 #Previous value
            break
      MechAttn = MAttn - i + Backoff;  #MechAttn Used for next step
      if (MechAttn < 0):
         MechAttn= 0
      Set_AttnMech(MechAttn)
         
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #%%%% Ref Sweep
      #%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
      #print('   RefLvl Swp: ');
      EVM_Prev = 1.00; 
      i=0;
      Set_Autolevel("OFF")            #Manually Set RefLvl & Attn
      for x in range(0):
         Set_RefLevel(RefLvl - i)
         EVM_Curr = Get_EVM();
         if debug==1: print ("      Ref:%.2f MAttn:%.0f EVM:%.2f"%(RefLvl-i, MechAttn, EVM_Curr))
         if EVM_Curr =='NAN':
            print "EVM NAN"
            break

         Diff = EVM_Prev - EVM_Curr;   #Positive = improvedEVM
         if (Diff > EVM_Wind):
            EVM_Prev = EVM_Curr;
            i = i + 1;
         else:
            i = i - 1;                 #Previous value
            Set_RefLevel(RefLvl - i)
            break
      EVM_Wait()

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   if 0:
      import sys
      print(sys.version)
   VSE = VSE()
   VSE.VISA_Open("127.0.0.1")
   VSE.Set_Channel("ADEM")
   VSE.Set_DisplayUpdate('ON')
   VSE.Set_Adem_dbw(500e6)
   VSE.Set_InitImm()
 
