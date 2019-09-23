# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator LTE Functions
### Author : Martin C Lim
### Date   : 2019.03.05
### Options: K54  802.11 a/b/g/n
###          K86  802.11 ac
###          K141 802.11 ad
###          K142 802.11 ax
###
### Standrd |Modu|Freqncy|Mode|PPDU|BW |MIMO|BitRate
### --------|----|-------|----|----|---|----|-------
### 802.11b  DSSS 2.4     Legy  CCK 20 SISO   11Mbps
### 802.11a  OFDM     5.4 Legy         SISO   54Mbps
### 802.11g  both 2.4 5.4 Legy   L     SISO   54Mbps
### 802.11n  OFDM 2.4 5.4 GrnF  HT  40 MIMO  300Mbps
### 802.11ac OFDM     5.4 MixM VHT 160 MIMO 1750Mbps
### 802.11ax OFDM 2.4 5.4 MixM  HE 160 MIMO   11Gbps
#####################################################################
from rssd.VSG.Common import VSG     #pylint: disable=E0611,E0401

class VSG(VSG):                     #pylint: disable=E0102
    """ Rohde & Schwarz Vector Signal Generator 802.11 Object """
    def __init__(self):
        super(VSG,self).__init__()    #Python2/3
        self.Model = "SMW"
        self.WLAN_Std  = 'N'
        self.WLAN_ChBW = 20       #MHz
        self.WLAN_MCS  = 1

    #####################################################################
    ### VSG Query
    #####################################################################
    def Get_WLAN_ChBW(self):
        rdStr = self.query(f':SOUR:BB:WLNN:BW?')
        return rdStr

    def Get_WLAN_MCS(self):
        #WLAN-->Frame Blocks-->PPDU Conf..--> MCS Config
        rdStr = self.query(f':SOUR:BB:WLNN:FBL1:MCS?')
        return rdStr

    def Get_WLAN_Modulation(self):
        #WLAN-->Frame Blocks-->PPDU Conf..--> MCS Config
        rdStr = self.query(f':SOUR:BB:WLNN:FBL1:MOD1?')
        return rdStr

    def Get_WLAN_PPDU(self):
        #n : HT
        #ac: VHT
        #ax: HE 
        rdStr = self.query(f':SOUR:BB:WLNN:FBL1:TMOD?')
        return rdStr

    def Get_WLAN_Standard(self):
        rdStr = self.query(f':SOUR:BB:WLNN:FBL1:TMOD?')
        if rdStr[0] == 'L':
            return 'A'
        elif (rdStr[:3] == 'CCK') or (rdStr[:3] == 'PBC'):
            return 'B'
        elif rdStr[:2] == 'HT':
            return 'N'
        elif rdStr[:1] == 'V':
            return 'AC'
        elif rdStr[:2] == 'HE':
            return 'AX'
            

    #####################################################################
    ### VSG Setting
    #####################################################################
    def Set_WLAN_BBState(self, sState):
        if (sState == 1) or (sState == 'ON'):
            self.jav_OPC_Wait(':SOUR1:BB:WLNN:STAT 1')
        else:
            self.write(':SOUR1:BB:WLNN:STAT 0')

    def Set_WLAN_ChBW(self,iChBW):
        self.write(f':SOUR:BB:WLNN:BW BW{iChBW:02d}')
        self.WLAN_ChBW = iChBW

    def Set_WLAN_MCS(self,iMCS):
        #WLAN-->Frame Blocks-->PPDU Conf..--> MCS Config
        self.write(f':SOUR:BB:WLNN:FBL1:MCS MCS{iMCS}')

    def Set_WLAN_Modulation(self, sMod):
        #WLAN-->Frame Blocks-->PPDU Conf..--> MCS Config
        self.write(f':SOUR:BB:WLNN:FBL1:MOD1 {sMod}')

    def Set_WLAN_Standard(self, sStd):
        #WLAN-->Frame Blocks-->TxMode
        sStd.upper()
        if sStd == 'B':
            self.write(f':SOUR:BB:WLNN:FBL1:PMOD LEG')  #Set Physical Mode
            self.write(f':SOUR:BB:WLNN:FBL1:TMOD CCK')
        elif sStd == 'G' or sStd == 'A':
            self.write(f':SOUR:BB:WLNN:FBL1:PMOD LEG')  #Set Physical Mode
            self.write(f':SOUR:BB:WLNN:FBL1:TMOD L{self.WLAN_ChBW}')
        elif sStd == 'N':
            self.write(f':SOUR:BB:WLNN:FBL1:PMOD MIX')  #Set Physical Mode
            self.write(f':SOUR:BB:WLNN:FBL1:TMOD HT{self.WLAN_ChBW}')
        elif sStd == 'AC':
            self.write(f':SOUR:BB:WLNN:FBL1:PMOD MIX')  #Set Physical Mode
            self.write(f':SOUR:BB:WLNN:FBL1:TMOD V{self.WLAN_ChBW}')
        elif sStd == 'AX':
            self.write(f':SOUR:BB:WLNN:FBL1:PMOD MIX')  #Set Physical Mode
            self.write(f':SOUR:BB:WLNN:FBL1:TMOD HE{self.WLAN_ChBW}')
        else:
            print(f'Set_WLAN_Standard: {sStd} not supported')


#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   WLAN = VSG()
   WLAN.jav_Open("192.168.1.114")
   print(WLAN.Get_WLAN_Standard())
   WLAN.jav_Close()