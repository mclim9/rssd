#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Generic FSW/SMW ATE
### Author:  Martin C Lim
### Date:    2017.08.21
###
#####################################################################
### User Input
#####################################################################
FSW_IP = '192.168.1.109'
SMW_IP = '192.168.1.114'
InFile = '00_RSATE.csv'
WvArry = ['V5GTF_xPUSCH_64QAM_100RB']

PwrArry = range(-50,10,2)  #(Start,Stop,Step)
FreqArry = [20e9,26e9]

#####################################################################
### Code Begin
#####################################################################
import os
import time
import VSA_FSW
import VSG_SMW
OutFile = "Data\\RSATE-%s.csv"%time.strftime("%y%m%d")

#####################################################################
### Function Definition
#####################################################################
def Output(inStr):
   print(inStr),
   f = open(OutFile, 'a')          #Open File
   f.write(inStr+'\n')
   f.close()
   return 1

def K96_Config(fPower):
   Fs = VSG_SMW.Get_ArbClockFreq()
   ATim = VSG_SMW.Get_ArbTime()
   VAS_K96.Set_SamplingRate(Fs)
   VAS_K96.Set_ConfigFile(K96File)
   VAS_K96.Set_SweepTime(ATim*2)
   VAS_K96.Set_RefLevel(fPower)
   #if fPower < -20:
   #   VAS_K96.Set_Preamp("ON")
   #else:
   VAS_K96.Set_Preamp("OFF")
   
#####################################################################
### Overhead
#####################################################################
#sDate = time.strftime("%y%m%d-%H%M%S")
f = open(OutFile, 'a')          #Open File
f.write('\n')
VSA_FSW.Init(FSW_IP,f)
VSG_SMW.Init(SMW_IP,f)
f.close()

#####################################################################
### SMW-Setup
#####################################################################
VSG_SMW.IDN()
#VSG_SMW.Reset()
VSG_SMW.Set_ArbWv('/var/user/CW__I_0__Q_0.wv')  #Dummy Arb for below
VSG_SMW.Init_Wideband()                         #Set dig attn
VSG_SMW.Set_ArbState("ON")
VSG_SMW.Set_RFState("ON")

#####################################################################
### FSW-Setup
#####################################################################
VSA_FSW.Set_DisplayUpdate(1)
VSA_FSW.Set_Channel("V5GT")         #V5G Application
VSA_FSW.Set_V5G_Direction("UL")     #Demodulate Uplink signal

#####################################################################
### Loop code
#####################################################################
Output("Date  ,Time  ,Freq ,InPwr ,Mod ,RFBW    ,Spacing     ,Mod  ,A,Ref ,ChPwr,EVM")
print(" ")
t0 = time.time()
i = 0
iTotal = len(WvArry) * len(FreqArry) * len(PwrArry)
for Wv in WvArry:
   VSG_SMW.VISA_Clear()
   if 1:
      ArbWv = '/var/user/%s.wv'%Wv
      VSG_SMW.Set_ArbWv(ArbWv)
   else:
      VSG_SMW.Set_V5G_Wave("Uplink_Config_1");
      VSG_SMW.Set_V5GState("ON")
      VSA_FSW.Set_V5G_Allocation("UL_allocation.allocation")
   for Freq in FreqArry:
      VSA_FSW.Set_Freq(Freq)
      VSG_SMW.Set_Freq(Freq)
      for Pwr in PwrArry:
#         if 1:
         try:
            VSG_SMW.Set_RFPwr(Pwr)
            VSG_SMW.Set_DriveAmp("AUTO")
            #***************************
            ### Measure
            #***************************
            #VSA_FSW.Get_InitImm()
            #VSA_FSW.Set_Autolevel()
            VSA_FSW.Set_V5G_AutoEVM()
            time.sleep(60)
            EVM_Meas = VSA_FSW.Get_EVM_n_Params()
            sDate = time.strftime("%y%m%d,%H%M%S")       #Date String
            Conditions = "%s,%5.3f,%6.2f"%(sDate,Freq/1e9,Pwr) #Condition String
            Output("%s,%s,%s,"%(Conditions,Wv.replace("_",","),EVM_Meas)) #Record Data

            #***************************
            ### Time Calc
            #***************************
            i += 1
            delta = (time.time() - t0)
            timeLeft = ((delta*iTotal/i)-delta)
            timeDone = time.ctime(time.time() + timeLeft)
            print("Iter:%d/%d Time:%.2fmin  Done:%s"%(i,iTotal,delta/60,timeDone))
         except:
            print("error Happened")
      #End Pwr Loop
   #End Freq Loop
#End Wave Loop
         
#####################################################################
### Close Nicely
#####################################################################
#VSG_SMW.Set_RFState("OFF")
if 0:
   VSG_SMW.Close()
   VSA_FSW.Close()
