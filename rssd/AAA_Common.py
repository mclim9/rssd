# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: AAA Common Functions
### Author : Martin C Lim
### Date   : 20xx.xx.xx
###  _____  _____   ____ _______ ____ _________     _______  ______ 
### |  __ \|  __ \ / __ \__   __/ __ \__   __\ \   / /  __ \|  ____|
### | |__) | |__) | |  | | | | | |  | | | |   \ \_/ /| |__) | |__    
### |  ___/|  _  /| |  | | | | | |  | | | |    \   / |  ___/|  __|  
### | |    | | \ \| |__| | | | | |__| | | |     | |  | |    | |____ 
### |_|    |_|  \_\\____/  |_|  \____/  |_|     |_|  |_|    |______|
###                         _            _           _ 
###                        | |          | |         | |
###             _   _ _ __ | |_ ___  ___| |_ ___  __| |
###            | | | | '_ \| __/ _ \/ __| __/ _ \/ _` |
###            | |_| | | | | ||  __/\__ \ ||  __/ (_| |
###             \__,_|_| |_|\__\___||___/\__\___|\__,_|
###
###############################################################################
from rssd.yaVISA import jaVisa

class AAA(jaVisa):
    """ Rohde & Schwarz AAA Object """
    def __init__(self):
        super(AAA, self).__init__()
        self.Model = "AAA"

    #####################################################################
    ### AAA Get Functions
    #####################################################################
    def Get_ACLR(self):
        rdStr = self.query(':CALC:MARK:FUNC:POW:RES? MCAC').split(',')
        return rdStr

    def Get_ChPwr(self):
        rdStr = self.queryFloat('FETC:SUMM:POW?')
        return rdStr 

    def Get_Channels(self):
        rdStr = self.query('INST:LIST?').split(',')
        return rdStr

    #####################################################################
    ### AAA Init Functions
    #####################################################################
    def Init_Measurement(self):
        #Configure instrument measurment
        pass

    #####################################################################
    ### AAA Set Functions
    #####################################################################
    def Set_DisplayUpdate(self,state):
        # Param: ON|OFF
        self.write(f'SYST:DISP:UPD {state}')            #Display Update State

    def Set_Freq(self,fFreq):
        self.write(f':SENS:FREQ:CENT {fFreq}')          #RF Freq

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    AAA_Inst = AAA().jav_Open("192.168.1.100")
    AAA_Inst.jav_IDN()
    AAA_Inst.jav_ClrErr()