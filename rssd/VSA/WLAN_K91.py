# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.03.12
### Requird: python -m pip install rssd
###
### Standrd |Modu|Freqncy|Mode|PPDU|BW |MIMO|BitRate
### --------|----|-------|----|----|---|----|-------
### 802.11b  DSSS 2.4     Legy  CCK  20 SISO   11Mbps
### 802.11a  OFDM     5.4 Legy          SISO   54Mbps
### 802.11g  both 2.4 5.4 Legy    L     SISO   54Mbps
### 802.11n  OFDM 2.4 5.4 GrnF   HT  40 MIMO  300Mbps
### 802.11ac OFDM     5.4 MixM  VHT 160 MIMO 1750Mbps
### 802.11ax OFDM 2.4 5.4 MixM   HE 160 MIMO   11Gbps
#####################################################################
from rssd.VSA.Common import VSA        #pylint: disable=E0611,E0401

class VSA(VSA):                        #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Analyzer 802.11 Object """
    def __init__(self):
        super(VSA, self).__init__()
        self.WLAN_Std  = 'N'
        self.WLAN_ChBW = 100       #MHz
        self.WLAN_MCS  = 1

    #####################################################################
    ### VSA Query
    #####################################################################
    def Get_ACLR(self):
        ACLR = self.queryFloatArry(':CALC:MARK:FUNC:POW:RES? MCAC')
        return ACLR

    def Get_Params_WLAN_EVM(self,header=0):
        """Retrieve Parameters for test logs"""
        if header != 1:
            Burst = self.Get_WLAN_BurstCount()
            Power = self.Get_WLAN_PPDUPwr()
            EVM   = self.Get_WLAN_EVM()
            outStr = f"{Burst},{Power:6.3f},{EVM:.2f}"
        else:
            outStr = 'BurstCnt,PPDUPwr,EVM'
        return outStr

    def Get_WLAN_BurstCount(self):
        rdStr = self.query(f'FETC:BURS:COUN:ALL?')
        rdStr = self.query(f'FETC:BURS:COUN?')
        return rdStr

    def Get_WLAN_PPDUPwr(self):
        try:
            rdStr = self.queryFloatArry(f'FETC:BURS:RMS:AVER?')[1]
        except:
            rdStr = -9999
        return rdStr

    def Get_WLAN_ChBW(self):
        #rdStr = self.query(f':SENS:BAND:CHAN:AUTO:TYPE?')
        rdStr = '<TBD>'
        return rdStr

    def Get_WLAN_EVM(self):
        rdStr = self.queryFloat('FETC:BURS:EVM:ALL:AVER?')
        return rdStr

    def Get_WLAN_Modulation(self):
        # FSW-->Demod -->
        rdStr = self.query(f':SENS:DEM:FORM:BAN?')      #AC
        return rdStr

    def Get_WLAN_MCS(self):
        # For n & ac
        rdStr = 'MCS' + self.query(f'SENS:DEM:FORM:MCS?')
        return rdStr

    def Get_WLAN_PPDU(self):
        std = self.Get_WLAN_Standard()
        if std == 'N':
            rdStr = self.query(':TRAC:DATA? TRACE1')
        elif std == 'AC':
            rdStr = self.query(':TRAC:DATA? TRACE1')
        elif std == 'AX':
            rdStr = self.query('FETCh:SFIeld:ALL?')
        else:
            rdStr = '<TBD>'
        return rdStr

    def Get_WLAN_SEM(self):
        rdStr = self.query(f':CALC1:LIM:FAIL?')
        return rdStr

    def Get_WLAN_Standard(self):
        #0:A 1:B 2/3:J 4:G 6:N 7:N-MIMO 8:AC 9:P 10:AX
        rdStr = self.queryInt(f':CONF:STAN?')
        if rdStr == 0:
            rdStr = 'A'
        elif rdStr == 1:
            rdStr = 'B'
        elif rdStr == 4:
            rdStr = 'G'
        elif rdStr == 6:
            rdStr = 'N'
        elif rdStr == 8:
            rdStr = 'AC'
        elif rdStr == 10:
            rdStr = 'AX'
        return rdStr

    #####################################################################
    ### Init WLAN
    #####################################################################
    def Init_WLAN(self):
        self.Set_Channel('WLAN')
        self.write(':SENS:DEM:FORM:BCON:AUTO 1')            #Auto PPDU Demod

    def Init_WLAN_ACLR(self):
        self.Set_Channel('WLAN')
        self.write(':CONF:BURS:SPEC:ACPR:IMM')              #ACLR

    def Init_WLAN_EVM(self):
        self.Set_Channel('WLAN')
        self.write(':CONF:BURS:IQ:IMM')                     #EVM
        self.write(':SENS:DEM:FORM:BCON:AUTO 1')            #Auto PPDU Demod

    def Init_WLAN_SEM(self):
        self.Set_Channel('WLAN')
        self.write(':CONF:BURS:SPEC:MASK:IMM')              #SEM

    #####################################################################
    ### VSA Settings
    #####################################################################
    def Set_WLAN_AnalysisMode(self):
        self.write(':SENS:DEM:FORM:BCON:AUTO 1')

    def Set_WLAN_Autolvl(self):
        """ Supports B40; B80; B2001 not supported."""
        #self.query('ADJ:LEV;*OPC?')
        self.write(':CONF:POW:AUTO ONCE;*WAI')      #FSVA

    def Set_WLAN_CaptureTime(self, swpTime):
        self.Set_SweepTime(swpTime)

    def Set_WLAN_ChBW(self,iBW):
        # iBW of 0 sets VSA to auto detect
        if iBW == 0:  # Auto
            self.write(f':SENS:BAND:CHAN:AUTO:TYPE ALL')
        else:
            self.write(f':SENS:BAND:CHAN:AUTO:TYPE MB{iBW:02d}')

    def Set_WLAN_MIMO_Streams(self, iAnt):
        self.write(f'CONF:WLAN:DUTC TX{iAnt}')

    def Set_WLAN_Modulation(self,iMod):
        self.write(f':CONF:LTE:UL:SUBF0:ALL:MOD {iMod}')

    def Set_WLAN_MCS(self,iMCS):
        # iMCS of 0 sets VSA to auto detect
        if iMCS == 0:
            self.write(f'SENS:DEM:FORM:MCS:MODE ALL')
        else:
            self.write(f'SENS:DEM:FORM:MCS:MODE MEAS')
            self.write(f'SENS:DEM:FORM:MCS {iMCS}')

    def Set_WLAN_Standard(self,sStd):
        """AC N AX"""
        #0:A 1:B 2/3:J 4:G 6:N 7:N-MIMO 8:AC 9:P 10:AX
        sStd.upper()
        if sStd == 'A':
            self.write(f':CONF:STAN 0')
        elif sStd == 'B':
            self.write(f':CONF:STAN 1')
        elif sStd == 'G':
            self.write(f':CONF:STAN 4')
        elif sStd == 'N':
            self.write(f':CONF:STAN 6')
        elif sStd == 'AC':
            self.write(f':CONF:STAN 8')
        elif sStd == 'AX':
            self.write(f':CONF:STAN 10')
        else:
            print(f'Set_WLAN_Standard {sStd} not supported')


#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    FSW = VSA()
    FSW.jav_Open("192.168.1.109")
    print(FSW.query(':TRAC:DATA? TRACE1'))
    #print(FSW.Get_WLAN_EVMParams())
    #FSW.Set_WLAN_Autolvl()
    FSW.jav_Close()
