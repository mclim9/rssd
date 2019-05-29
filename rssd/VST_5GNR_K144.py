# -*- coding: future_fstrings -*-
##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose : FSW/SMW 5G NR Demo
### Author  : mclim
### Date    : 2018.07.05
### Descrip : FSW 3.20-18.7.1.0 Beta
###           SMW 4.30 SP2
##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.SMW_5GNR_K144 import VSG  #pylint: disable=E0611,E0401
from rssd.FSW_5GNR_K144 import VSA  #pylint: disable=E0611,E0401

class VST(object):
    """ Rohde & Schwarz Vector Signal Transciever 5GNR Object """
    def __init__(self):
        self.Freq      = 19e9
        self.SWM_Out   = 0
        self.NR_Dir    = 'DL'
        self.NR_Deploy = 'HIGH'     #LOW:MIDD:HIGH
        self.NR_ChBW   = 100        #MHz
        self.NR_SubSp  = 120        #kHz
        self.NR_RB     = 66         #RB
        self.NR_RBO    = 0          #RB Offset
        self.NR_Mod    = 'QAM64'    #QPSK; QAM16; QAM64; QAM256; PITB
        self.NR_TF     = 'OFF'

    def Get_5GNR_All(self):
        DMRS = 0

        odata =  [[] for i in range(3)]
        odata[0].append("[[Parameter]]  ")
        odata[0].append("Direction      ")
        odata[0].append("FreqRange      ")
        odata[0].append("RefA,MHz       ")
        odata[0].append("Ch BW          ")
        odata[0].append("TransPrecoding ")
        odata[0].append("====SS/PBCH====")
        odata[0].append("SubSpacing     ")
        odata[0].append("===User/BWP====")
        odata[0].append("SubSpacing     ")
        odata[0].append("Num BWP        ")
        odata[0].append("BWP_RB         ")
        odata[0].append("BWP_RBoff      ")
        odata[0].append("====Channel====")
        odata[0].append("User_BWP_Mod   ")
        odata[0].append("User_BWP_RB    ")
        odata[0].append("User_BWP_RBOff ")
        odata[0].append("User_BWP_SymNum")
        odata[0].append("User_BWP_SymOff")
        odata[0].append("User_BWP_Cntr  ")
        if DMRS:
            odata[0].append("=====DMRS======")
            odata[0].append("DMRS Config    ")
            odata[0].append("DMRS Mapping   ")
            odata[0].append("DMRS FirstSym  ")
            odata[0].append("DMRS Add Positn")
            odata[0].append("DMRS Length    ")
            odata[0].append("DMRS SeqGenMeth")
            odata[0].append("DMRS SeqGenSeed")
            odata[0].append("DMRS Rel Power ")

        try:
            # self.SMW.Set_5GNR_Parameters(self.NR_Dir)
            odata[1].append("[-SMW-]")
            odata[1].append(self.SMW.Get_5GNR_Direction())
            odata[1].append(self.SMW.Get_5GNR_FreqRange())
            odata[1].append(self.SMW.Get_5GNR_RefA()/1e6)
            odata[1].append(self.SMW.Get_5GNR_ChannelBW()) 
            odata[1].append(self.SMW.Get_5GNR_TransPrecoding())
            odata[1].append("=SSB==")
            odata[1].append(self.SMW.Get_5GNR_SSB_SubSpace())
            odata[1].append("=User=")
            odata[1].append(self.SMW.Get_5GNR_BWP_SubSpace())
            odata[1].append(self.SMW.Get_5GNR_BWP_Count())
            odata[1].append(self.SMW.Get_5GNR_BWP_ResBlock())
            odata[1].append(self.SMW.Get_5GNR_BWP_ResBlockOffset())
            odata[1].append("==Ch==")
            odata[1].append(self.SMW.Get_5GNR_BWP_Ch_Modulation())
            odata[1].append(self.SMW.Get_5GNR_BWP_Ch_ResBlock())
            odata[1].append(self.SMW.Get_5GNR_BWP_Ch_ResBlockOffset())
            odata[1].append(self.SMW.Get_5GNR_BWP_Ch_SymbNum())
            odata[1].append(self.SMW.Get_5GNR_BWP_Ch_SymbOff())
            odata[1].append(self.SMW.Get_5GNR_BWP_Center()/1e6)
            if DMRS:
                odata[1].append("=DMRS=")
                odata[1].append(self.SMW.Get_5GNR_BWP_Ch_DMRS_Config())
                odata[1].append(self.SMW.Get_5GNR_BWP_Ch_DMRS_Mapping())
                odata[1].append(self.SMW.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym())
                odata[1].append(self.SMW.Get_5GNR_BWP_Ch_DMRS_AddPosition())
                odata[1].append(self.SMW.Get_5GNR_BWP_Ch_DMRS_MSymbLen())
                odata[1].append(self.SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth())
                odata[1].append(self.SMW.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed())
                odata[1].append(self.SMW.Get_5GNR_BWP_Ch_DMRS_RelPwr())
        except:
            pass
            
        try:
            self.FSW.Init_5GNR()
            odata[2].append("[-FSW-]")
            odata[2].append(self.FSW.Get_5GNR_Direction())
            odata[2].append(self.FSW.Get_5GNR_FreqRange())
            odata[2].append(self.FSW.Get_5GNR_RefA()/1e6)
            odata[2].append(self.FSW.Get_5GNR_ChannelBW())
            odata[2].append(self.FSW.Get_5GNR_TransPrecoding())
            odata[2].append("=SSB==")
            odata[2].append(self.FSW.Get_5GNR_SSB_SubSpace())
            odata[2].append("=User=")
            odata[2].append(self.FSW.Get_5GNR_BWP_SubSpace())
            odata[2].append(self.FSW.Get_5GNR_BWP_Count())
            odata[2].append(self.FSW.Get_5GNR_BWP_ResBlock())
            odata[2].append(self.FSW.Get_5GNR_BWP_ResBlockOffset())
            odata[2].append("==Ch==")
            odata[2].append(self.FSW.Get_5GNR_BWP_Ch_Modulation())
            odata[2].append(self.FSW.Get_5GNR_BWP_Ch_ResBlock())
            odata[2].append(self.FSW.Get_5GNR_BWP_Ch_ResBlockOffset())
            odata[2].append(self.FSW.Get_5GNR_BWP_Ch_SymbNum())
            odata[2].append(self.FSW.Get_5GNR_BWP_Ch_SymbOff())
            odata[2].append(self.FSW.Get_5GNR_BWP_Center()/1e6)
            if DMRS:
                odata[2].append("=DMRS=")
                odata[2].append(self.FSW.Get_5GNR_BWP_Ch_DMRS_Config())
                odata[2].append(self.FSW.Get_5GNR_BWP_Ch_DMRS_Mapping())
                odata[2].append(self.FSW.Get_5GNR_BWP_Ch_DMRS_1stDMRSSym())
                odata[2].append(self.FSW.Get_5GNR_BWP_Ch_DMRS_AddPosition())
                odata[2].append(self.FSW.Get_5GNR_BWP_Ch_DMRS_MSymbLen())
                odata[2].append(self.FSW.Get_5GNR_BWP_Ch_DMRS_SeqGenMeth())
                odata[2].append(self.FSW.Get_5GNR_BWP_Ch_DMRS_SeqGenSeed())
                odata[2].append(self.FSW.Get_5GNR_BWP_Ch_DMRS_RelPwr())
        except:
            pass
        print('SMW/FSW Values: %d %d'%(len(odata[2]),len(odata[2]))) 

        return odata

    def Get_5GNR_All_print(self):
        data = self.Get_5GNR_All()
        for i in range(len(data[0])):
            try:
                print("%s\t%s\t%s"%(data[0][i],data[1][i],data[2][i]))
            except: 
            #     try:
            #         print("%s\t%s\t%s"%(data[0][i],data[1][i],'<notRead>'))
            #     except:
            #         print("%s\t%s\t%s"%(data[0][i],'<notRead>',data[2][i]))
                pass

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

    def Set_5GNR_All(self):
        try:
            ### SMW Settings
            self.SMW.Set_Freq(self.Freq)
            self.SMW.Set_5GNR_BBState('OFF')
            self.SMW.Set_5GNR_Direction(self.NR_Dir)
            self.SMW.Set_5GNR_TransPrecoding(self.NR_TF)
            self.SMW.Set_5GNR_FreqRange(self.NR_Deploy)
            self.SMW.Set_5GNR_ChannelBW(self.NR_ChBW)
            self.SMW.Set_5GNR_BWP_SubSpace(self.NR_SubSp)
            self.SMW.Set_5GNR_BWP_ResBlock(self.NR_RB)
            self.SMW.Set_5GNR_BWP_ResBlockOffset(self.NR_RBO)
            self.SMW.Set_5GNR_BWP_Ch_ResBlock(self.NR_RB)
            self.SMW.Set_5GNR_BWP_Corset_ResBlock(self.NR_RB)
            #self.SMW.Set_5GNR_BWP_Ch_ResBlockOffset(NR_RBO)
            self.SMW.Set_5GNR_BWP_Ch_Modulation(self.NR_Mod)
            self.SMW.Set_5GNR_SSB()
            self.SMW.Set_5GNR_BBState('ON')
            self.SMW.Set_RFState('ON')                            #Turn RF Output on
            self.SMW.Set_RFPwr(self.SWM_Out)                      #Output Power
        except:
            print("NR5G_SetSettings: SMW Error")

        try:
            ### FSW Setting
            self.FSW.Init_5GNR()
            self.FSW.Set_Freq(self.Freq)
            self.FSW.Set_5GNR_Direction(self.NR_Dir)
            self.FSW.Set_5GNR_TransPrecoding(self.NR_TF)
            self.FSW.Set_5GNR_FreqRange(self.NR_Deploy)
            self.FSW.Set_5GNR_ChannelBW(self.NR_ChBW)
            self.FSW.Set_5GNR_BWP_SubSpace(self.NR_SubSp)
            self.FSW.Set_5GNR_BWP_ResBlock(self.NR_RB)
            self.FSW.Set_5GNR_BWP_ResBlockOffset(self.NR_RBO)
            self.FSW.Set_5GNR_BWP_Ch_ResBlock(self.NR_RB)
            self.FSW.Set_5GNR_BWP_Corset_ResBlock(self.NR_RB)
            #self.FSW.Set_5GNR_BWP_Ch_ResBlockOffset(self.NR_RBO)
            self.FSW.Set_5GNR_BWP_Ch_Modulation(self.NR_Mod)
            self.FSW.Set_SweepCont(1)
            self.FSW.Set_InitImm()
        except:
            print("NR5G_SetSettings: FSW Error")
        return 0


##########################################################
### Instrument Settings
##########################################################
if __name__ == "__main__":
    NR5G = VST().jav_Open('192.168.1.114','192.168.1.109')
    NR5G.NR_ChBW = 200
    NR5G.Get_5GNR_All_print()
    NR5G.jav_Close()
