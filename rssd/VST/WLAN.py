# -*- coding: future_fstrings -*-
##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose : FSW/SMW LTE Demo
### Author  : mclim
### Date    : 2019.03.05
### Descrip : FSW 3.20-18.7.1.0 Beta
###           SMW 4.30 SP2
##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.VSG.WLAN_K54  import VSG  #pylint: disable=E0611,E0401
from rssd.VSA.WLAN_K91  import VSA  #pylint: disable=E0611,E0401

class VST(object):
    """ Rohde & Schwarz Vector Signal Transciever 802.11 Object """
    def __init__(self):
        self.Freq      = 2.5e9
        self.SWM_Out   = 0
        self.WLAN_Std  = 'N'
        self.WLAN_ChBW = 100        #MHz
        self.WLAN_MCS  = 1
        self.WLAN_Mod  = 'QAM64'    #QPSK; QAM16; QAM64; QAM256

    def Get_WLAN_All(self):
        odata =  [[] for i in range(3)]
        odata[0].append("[[Parameter]]  ")
        odata[0].append("Standard       ")
        odata[0].append("Ch BW          ")
        odata[0].append("PPDU           ")
        odata[0].append("MCS            ")
        odata[0].append("Mod            ")

        try:
            odata[1].append("[-SMW-]")
            odata[1].append(self.SMW.Get_WLAN_Standard())
            odata[1].append(self.SMW.Get_WLAN_ChBW())
            odata[1].append(self.SMW.Get_WLAN_PPDU())
            odata[1].append(self.SMW.Get_WLAN_MCS())
            odata[1].append(self.SMW.Get_WLAN_Modulation())
        except:
            pass
            
        try:
            self.FSW.Init_WLAN()
            odata[2].append("[-FSW-]")
            odata[2].append(self.FSW.Get_WLAN_Standard())
            odata[2].append(self.FSW.Get_WLAN_ChBW())
            odata[2].append(self.FSW.Get_WLAN_PPDU())
            odata[2].append(self.FSW.Get_WLAN_MCS())
            odata[2].append(self.FSW.Get_WLAN_Modulation())
        except:
            pass
        print('SMW/FSW Values: %d %d'%(len(odata[2]),len(odata[2]))) 

        return odata

    def Get_WLAN_All_print(self):
        data = self.Get_WLAN_All()
        for i in range(len(data[0])):
            try:
                print("%s\t%s\t%s"%(data[0][i],data[1][i],data[2][i]))
            except: 
                try:
                    print("%s\t%s\t%s"%(data[0][i],data[1][i],'<notRead>'))
                except:
                    print("%s\t%s\t%s"%(data[0][i],'<notRead>',data[2][i]))

    def jav_Open(self,SMW_IP,FSW_IP,OFile=''):
        self.SMW = VSG().jav_Open(SMW_IP,OFile,prnt=0)  #Create SMW Object
        self.FSW = VSA().jav_Open(FSW_IP,OFile,prnt=0)  #Create FSW Object
        return self

    def jav_Close(self):
        self.SMW.jav_Close()
        self.FSW.jav_Close() 
    
    def jav_Clear(self):
        self.SMW.jav_Clear()
        self.FSW.jav_Clear() 

    def Set_WLAN_All(self):
        try:
            ### SMW Settings
            self.SMW.Set_Freq(self.Freq)
            self.SMW.Set_WLAN_BBState('OFF')
            self.SMW.Set_WLAN_ChBW(self.WLAN_ChBW)
            self.SMW.Set_WLAN_Standard(self.WLAN_Std)
            self.SMW.Set_WLAN_MCS(self.WLAN_MCS)
            self.SMW.Set_WLAN_BBState('ON')
            self.SMW.Set_RFState('ON')                      #Turn RF Output on
        except:
            print("WLAN_SetSettings: SMW Error")

        try:
            ### FSW Setting
            self.FSW.Init_WLAN()
            self.FSW.Set_Freq(self.Freq)
            self.FSW.Set_WLAN_Standard(self.WLAN_Std)
            self.FSW.Set_WLAN_ChBW(self.WLAN_ChBW)
            self.FSW.Set_WLAN_MCS(self.WLAN_MCS)
        except:
            print("WLAN_SetSettings: FSW Error")
        return 0


##########################################################
### Instrument Settings
##########################################################
if __name__ == "__main__":
    WLAN = VST().jav_Open('192.168.1.114','192.168.1.109')
    WLAN.WLAN_Std  = 'AC'
    WLAN.WLAN_ChBW = 160
    WLAN.WLAN_MCS  = 5
    WLAN.Set_WLAN_All()
    WLAN.Get_WLAN_All_print()
    WLAN.jav_Close()
