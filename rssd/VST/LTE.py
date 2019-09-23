# -*- coding: future_fstrings -*-
##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose : FSW/SMW LTE Demo
### Author  : mclim
### Date    : 2019.03.05
### Descrip : FSW 3.20-18.7.1.0 Beta
###           SMW 4.30 SP2
##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.SMW_LTE_K55    import VSG  #pylint: disable=E0611,E0401
from rssd.FSW_LTE_K100   import VSA  #pylint: disable=E0611,E0401

class VST(object):
    def __init__(self):
        self.Freq      = 2.5e9
        self.SWM_Out  = 0
        self.LTE_Dir    = 'DL'
        self.LTE_ChBW  = 100        #MHz
        self.LTE_RB     = 66        #RB
        self.LTE_RBO    = 0         #RB Offset
        self.LTE_Mod    = 'QAM64'   #QPSK; QAM16; QAM64; QAM256
        self.LTE_CC     = 1

    def Get_LTE_All(self):
        odata =  [[] for i in range(3)]
        odata[0].append("[[Parameter]]  ")
        odata[0].append("Direction      ")
        odata[0].append("Duplex         ")
        odata[0].append("Ch BW          ")
        odata[0].append("===User/BWP====")
        odata[0].append("RB             ")
        odata[0].append("RBoff          ")
        odata[0].append("Mod            ")

        try:
            odata[1].append("[-SMW-]")
            odata[1].append(self.SMW.Get_LTE_Direction())
            odata[1].append(self.SMW.Get_LTE_Duplex())            
            odata[1].append(self.SMW.Get_LTE_ChBW()) 
            odata[1].append("=User=")
            odata[1].append(self.SMW.Get_LTE_ResBlock())
            odata[1].append(self.SMW.Get_LTE_ResBlockOffset())
            odata[1].append(self.SMW.Get_LTE_Modulation())
        except:
            pass
            
        try:
            self.FSW.Init_LTE()
            odata[2].append("[-FSW-]")
            odata[2].append(self.FSW.Get_LTE_Direction())
            odata[2].append(self.FSW.Get_LTE_Duplex())
            odata[2].append(self.FSW.Get_LTE_ChBW())
            odata[2].append("=User=")
            odata[2].append(self.FSW.Get_LTE_ResBlock())
            odata[2].append(self.FSW.Get_LTE_ResBlockOffset())
            odata[2].append(self.FSW.Get_LTE_Modulation())
        except:
            pass
        print('SMW/FSW Values: %d %d'%(len(odata[2]),len(odata[2]))) 

        return odata

    def Get_LTE_All_print(self):
        data = self.Get_LTE_All()
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

    def Set_LTE_All(self):
        try:
            ### SMW Settings
            self.SMW.Set_Freq(self.Freq)
            self.SMW.Set_LTE_BBState('OFF')
            self.SMW.Set_LTE_Direction(self.LTE_Dir)
            self.SMW.Set_LTE_ChBW(self.LTE_ChBW)
            self.SMW.Set_LTE_ResBlock(self.LTE_RB)
            self.SMW.Set_LTE_ResBlockOffset(self.LTE_RBO)
            self.SMW.Set_LTE_Modulation(self.LTE_Mod)
            self.SMW.Set_LTE_BBState('ON')
            self.SMW.Set_RFState('ON')                          #Turn RF Output on
            self.SMW.Set_RFPwr(self.SWM_Out)                    #Output Power
        except:
            print("NR5G_SetSettings: SMW Error")

        try:
            ### FSW Setting
            self.FSW.Init_LTE()
            self.FSW.Set_Freq(self.Freq)
            self.FSW.Set_LTE_Direction(self.LTE_Dir)
            self.FSW.Set_LTE_ChBW(self.LTE_ChBW)
            self.FSW.Set_LTE_ResBlock(self.LTE_RB)
            self.FSW.Set_LTE_ResBlockOffset(self.LTE_RBO)
            self.FSW.Set_LTE_Modulation(self.LTE_Mod)
            self.FSW.Set_SweepCont(1)
            self.FSW.Set_InitImm()
        except:
            print("NR5G_SetSettings: FSW Error")
        return 0


##########################################################
### Instrument Settings
##########################################################
if __name__ == "__main__":
    LTE = VST().jav_Open('192.168.1.114','192.168.1.109')
    LTE.LTE_ChBW = 10
    LTE.Set_LTE_All()
    LTE.Get_LTE_All_print()
    LTE.jav_Close()
