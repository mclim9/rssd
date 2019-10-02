# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Radio Communication Tester(RCT) Functions
### Author : Martin C Lim
### Date   : 2018.05.29
###############################################################################
from rssd.RCT.Common import RCT              #pylint: disable=E0611,E0401

class RCT(RCT):
    """ Rohde & Schwarz Radio Comm Tester Object """
    def __init__(self):
        super(RCT, self).__init__()
        self.Model = "CMW-GPRF"

    ###########################################################################
    ### BSE Get Functions
    ###########################################################################
    def Get_AmpSettings(self):
        """Get ExpectPwr; UserMargin; ExtAttn; MixerOffset settings"""
        expp = self.Get_5GNR_ExpPwr()
        user = self.Get_5GNR_UserMargin()
        exta = self.Get_5GNR_ExtAttn()
        mixr = self.Get_5GNR_MixerOff()
        return f'{expp:7.3f},{user:7.3f},{exta:7.3f},{mixr:2d}'

    def Get_5GNR_EVM(self):
        """ Arry4: EVM_RMS_HIGH
            Arry19:TxPwr 
            Arry20:PkPwr 
            Arry16:FrqErr"""
        # self.write('ABOR:NRMM:MEAS:MEV')
        self.query('INIT:NRMM:MEAS:MEV;*OPC?')
        rdStr = self.queryFloatArry('FETC:NRMM:MEAS:MEV:MOD:AVER?')
        try:
            rdStr = [rdStr[3], rdStr[18], rdStr[19], rdStr[15]]
        except:
            rdStr = [-9999,-9999,-9999,-9999]
        return rdStr

    def Get_5GNR_ExpPwr(self):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dBm """
        rdStr = self.queryFloat(f'CONF:NRMM:MEAS:RFS:ENP?')
        return rdStr

    def Get_5GNR_ExtAttn(self):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dB """
        rdStr = self.queryFloat(f'CONF:NRMM:MEAS:RFS:EATT?')
        return rdStr

    def Get_5GNR_MixerOff(self):
        """ExpPwr = Range + ExtAttn - UserMargin
           range: -10 to 10"""
        rdStr = self.queryInt(f'CONF:NRMM:MEAS:RFS:MLOF?')
        return rdStr

    def Get_5GNR_UserMargin(self):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dB """
        rdStr = self.queryFloat(f'CONF:NRMM:MEAS:RFS:UMAR?')
        return rdStr

    ###########################################################################
    ### BSE Init Functions
    ###########################################################################
    def Init_5GNR(self):
        self.write('SYST:GEN:ALL:OFF')
        self.write('SYST:MEAS:ALL:OFF')
        self.write('ABOR:NRMM:MEAS:MEV')
        self.query('INIT:NRMM:MEAS:MEV;*OPC?')

    ###########################################################################
    ### BSE Set Functions
    ###########################################################################
    def Set_5GNR_BWP_SubSpace(self,iSubSp):
        """60| 120"""
        self.write(f'CONF:NRMM:MEAS:CCAL:TXBW:SCSP S{iSubSp}K')

    def Set_5GNR_ChannelBW(self,iBW):
        """ 050 100 200 400"""
        self.write(f'CONF:NRMM:MEAS:CC1:CBAN B{iBW}')

    def Set_5GNR_ExpPwr(self, pwr):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dBm """
        self.write(f'CONF:NRMM:MEAS:RFS:ENP {pwr} DBM')

    def Set_5GNR_ExtAttn(self, pwr):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dB """
        self.write(f'CONF:NRMM:MEAS:RFS:EATT {pwr} DB')

    def Set_5GNR_Freq(self,freq):
        """MHz"""
        self.write(f'CONF:NRMM:MEAS:RFS:FREQ {freq} MHz')

    def Set_5GNR_MixerOff(self, pwr):
        """ExpPwr = Range + ExtAttn - UserMargin
           range: -10 to 10
           units: dB """
        self.write(f'CONF:NRMM:MEAS:RFS:MLOF {pwr}')

    def Set_5GNR_PhaseComp(self,state,freq):
        """ State: OFF | CAF | UDEF 
            Freq : Hz"""
        self.write(f'CONF:NRMM:MEAS:MEV:PCOM {state},{freq}')

    def Set_5GNR_Periodicity(self,period):
        """ Period: 05 | 0625 | 1 | 125 | 2 | 25 | 5 | 10 """
        self.write(f'CONF:NRMM:MEAS:ULDL:PER MS{period}')

    def Set_5GNR_UserMargin(self, pwr):
        """ExpPwr = Range + ExtAttn - UserMargin
           units: dB """
        self.write(f'CONF:NRMM:MEAS:RFS:UMAR {pwr} DB')


###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    CMW = RCT()
    CMW.jav_Open("192.168.1.160")
    CMW.Init_Syst()
    print(CMW.Get_5GNR_EVM())
    CMW.jav_Close()
