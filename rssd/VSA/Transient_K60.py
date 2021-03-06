"""Vector Signal Analyzer Transient Analysis Functions"""
from __future__ import print_function
from rssd.VSA.Common import VSA

class VSA(VSA):
    """ Rohde & Schwarz Vector Signal Analyzer Transient Object """
    def __init__(self):
        super(VSA, self).__init__()        #Python 2/3
        self.QRange     = 'ALL'

    #####################################################################
    ### Transient Analysis Get
    #####################################################################
    def Get_TA_HopTable(self):
        self.write(f'SENS:SIGN:MOD HOP')
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
        self.write(f'SENS:SIGN:MOD CHIR')
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
        """Returns large table"""
        TATable = self.queryFloatArry('CALC:CHRD:STAT:DATA?')
        return TATable

    def Get_TA_ChirpStats_TimeBegin(self):
        # Chirp Stat Col2
        #Manual 11.9.2  CURR | ALL
        rdStr = self.query(f'SENS:CHIR:TIM:BEG:AVER? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:TIM:BEG:SDEV? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:TIM:BEG:MAX? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:TIM:BEG:MIN? {self.QRange}')
        print(rdStr)
        return rdStr

    def Get_TA_ChirpStats_TimeLength(self):
        # Chirp Stat Col3
        #Manual 11.9.2  CURR | ALL
        rdStr = self.query(f'SENS:CHIR:TIM:LENG:AVER? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:TIM:LENG:SDEV? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:TIM:LENG:MAX? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:TIM:LENG:MIN? {self.QRange}')
        print(rdStr)
        return rdStr

    def Get_TA_ChirpStats_Rate(self):
        # Chirp Stat Col4
        #Manual 11.9.2  CURR | ALL
        rdStr = self.query(f'SENS:CHIR:TIM:RATE:AVER? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:TIM:RATE:SDEV? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:TIM:RATE:MAX? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:TIM:RATE:MIN? {self.QRange}')
        print(rdStr)
        return rdStr

    def Get_TA_ChirpStats_StateDev(self):
        # Chirp Stat Col5
        #Manual 11.9.2  CURR | ALL
        rdStr = self.query(f'SENS:CHIR:FREQ:CHER:AVER? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:CHER:SDEV? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:CHER:MAX? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:CHER:MIN? {self.QRange}')
        print(rdStr)
        return rdStr

    def Get_TA_ChirpStats_AvgFreq(self):
        # Chirp Stat Col6
        #Manual 11.9.2  CURR | ALL
        rdStr = self.query(f'SENS:CHIR:FREQ:FREQ:AVER? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:FREQ:SDEV? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:FREQ:MAX? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:FREQ:MIN? {self.QRange}')
        print(rdStr)
        return rdStr

    def Get_TA_ChirpStats_Bandwidth(self):
        # Chirp Stat Col7
        #Manual 11.9.2  CURR | ALL
        rdStr = self.query(f'SENS:CHIR:FREQ:BWID:AVER? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:BWID:SDEV? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:BWID:MAX? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:BWID:MIN? {self.QRange}')
        print(rdStr)
        return rdStr

    def Get_TA_ChirpStats_FreqDevAvg(self):
        # Chirp Stat Col13
        #Manual 11.9.2  CURR | ALL
        rdStr = self.query(f'SENS:CHIR:FREQ:AVGF:AVER? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:AVGF:SDEV? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:AVGF:MAX? {self.QRange}')
        rdStr = self.query(f'SENS:CHIR:FREQ:AVGF:MIN? {self.QRange}')
        print(rdStr)
        return rdStr

    def Get_TA_TestStuff(self):
        TATable = self.query('CALC:CHRD:STAT:DATA?').split(',')
        print(len(TATable))
        #print(TATable)
        #self.write("MMEM:STOR6:TAB ALL,'C:\\R_S\\Instr\\asdf.data'")

    #####################################################################
    ### Transient Analysis Init
    #####################################################################
    def Init_TranAna(self):
        self.Set_Channel('TA')

    #####################################################################
    ### Transient Analysis Set
    #####################################################################
    def Set_TA_Mode(self, sMode):
        """CHIR HOP"""
        if sMode == 'HOP':
            self.write(':SENS:SIGN:MOD HOP')
        elif sMode in ('CHIR','CHIRP'):
            self.write(':SENS:SIGN:MOD CHIR')
        else:
            print('K60 Mode Not supported')

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
