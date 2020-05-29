from __future__ import print_function
# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose : Vector Signal Analyzer Transient Analysis Functions
### Author  : Martin C Lim
### Date    : 2018.08.14
from rssd.VSA.Common import VSA

class VSA(VSA):
    """ Rohde & Schwarz Vector Signal Analyzer Transient Object """
    def __init__(self):
        super(VSA, self).__init__()        #Python 2/3

    #####################################################################
    ### FSW V5G
    #####################################################################
    def Init_TranAna(self):
        self.Set_Channel('TA')

    #####################################################################
    ### FSW TA Settings
    #####################################################################

    #####################################################################
    ### FSW Common Query
    #####################################################################
    def Get_TA_HopTable(self):
        self.write('SENS:SIGN:MOD HOP')
        TATable = self.query('CALC:HOPD:TABL:RES? 1,3').split(',')
        numEle = 27
        print("Table size: %d"%(len(TATable)))
        for i,elem in enumerate(TATable):
            print(elem,end=' ')
            if (i % numEle) == (numEle-1):
                print('<break>\r\n')
        return 1

    def Get_TA_ChirpTable(self):
        #Manual 11.9.2
        self.write('SENS:SIGN:MOD CHIR')
        TATable = self.query('CALC:CHRD:TABL:RES? 1,2').split(',')
        numEle = 27
        print("Table size: %d"%(len(TATable)))
        for i,elem in enumerate(TATable):
            print(elem,end=' ')
            if (i % numEle) == (numEle-1):
                print('<break>\r\n')
        return 1

    def Get_TA_ChirpStat(self):
        #Manual 11.9.2
        TATable = self.query('CALC:CHRD:STAT:DATA?').split(',')
        print(TATable)

    def Get_TA_ChirpStats_TimeBegin(self):
        # Chirp Stat Col2
        #Manual 11.9.2  CURR | ALL
        QRange = 'ALL'
        print(self.query('SENS:CHIR:TIM:BEG:AVER? %s'%QRange))
        print(self.query('SENS:CHIR:TIM:BEG:SDEV? %s'%QRange))
        print(self.query('SENS:CHIR:TIM:BEG:MAX? %s'%QRange))
        print(self.query('SENS:CHIR:TIM:BEG:MIN? %s'%QRange))
        print()

    def Get_TA_ChirpStats_TimeLength(self):
        # Chirp Stat Col3
        #Manual 11.9.2  CURR | ALL
        QRange = 'ALL'
        print(self.query('SENS:CHIR:TIM:LENG:AVER? %s'%QRange))
        print(self.query('SENS:CHIR:TIM:LENG:SDEV? %s'%QRange))
        print(self.query('SENS:CHIR:TIM:LENG:MAX? %s'%QRange))
        print(self.query('SENS:CHIR:TIM:LENG:MIN? %s'%QRange))
        print()

    def Get_TA_ChirpStats_Rate(self):
        # Chirp Stat Col4
        #Manual 11.9.2  CURR | ALL
        QRange = 'ALL'
        print(self.query('SENS:CHIR:TIM:RATE:AVER? %s'%QRange))
        print(self.query('SENS:CHIR:TIM:RATE:SDEV? %s'%QRange))
        print(self.query('SENS:CHIR:TIM:RATE:MAX? %s'%QRange))
        print(self.query('SENS:CHIR:TIM:RATE:MIN? %s'%QRange))
        print()

    def Get_TA_ChirpStats_StateDev(self):
        # Chirp Stat Col5
        #Manual 11.9.2  CURR | ALL
        QRange = 'ALL'
        print(self.query('SENS:CHIR:FREQ:CHER:AVER? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:CHER:SDEV? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:CHER:MAX? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:CHER:MIN? %s'%QRange))
        print()

    def Get_TA_ChirpStats_AvgFreq(self):
        # Chirp Stat Col6
        #Manual 11.9.2  CURR | ALL
        QRange = 'ALL'
        print(self.query('SENS:CHIR:FREQ:FREQ:AVER? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:FREQ:SDEV? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:FREQ:MAX? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:FREQ:MIN? %s'%QRange))
        print()

    def Get_TA_ChirpStats_Bandwidth(self):
        # Chirp Stat Col7
        #Manual 11.9.2  CURR | ALL
        QRange = 'ALL'
        print(self.query('SENS:CHIR:FREQ:BWID:AVER? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:BWID:SDEV? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:BWID:MAX? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:BWID:MIN? %s'%QRange))
        print()

    def Get_TA_ChirpStats_FreqDevAvg(self):
        # Chirp Stat Col13
        #Manual 11.9.2  CURR | ALL
        QRange = 'ALL'
        print(self.query('SENS:CHIR:FREQ:AVGF:AVER? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:AVGF:SDEV? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:AVGF:MAX? %s'%QRange))
        print(self.query('SENS:CHIR:FREQ:AVGF:MIN? %s'%QRange))
        print()

    def Get_TA_TestStuff(self):
        TATable = self.query('CALC:CHRD:STAT:DATA?').split(',')
        print(len(TATable))
        #print(TATable)
        #self.write("MMEM:STOR6:TAB ALL,'C:\\R_S\\Instr\\asdf.data'")

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    FSW = VSA()
    FSW.jav_Open("192.168.1.109")
    #FSW.Init_TranAna()
    FSW.Get_TA_ChirpStats_TimeBegin()
    FSW.Get_TA_ChirpStats_TimeLength()
    FSW.Get_TA_ChirpStats_Rate()
    FSW.Get_TA_ChirpStats_StateDev()
    FSW.Get_TA_ChirpStats_AvgFreq()
    FSW.Get_TA_ChirpStats_Bandwidth()
    FSW.Get_TA_ChirpStats_FreqDevAvg()
    FSW.Get_TA_TestStuff()
