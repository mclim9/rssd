# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: OSP Open Switch Platform Common Functions
### Author : Martin C Lim
### Date   : 2018.06.15
#####################################################################
from rssd.yaVISA import jaVisa

class OSP(jaVisa):
    """ Rohde & Schwarz Open Switch Platform Object """
    def __init__(self):
        super(OSP, self).__init__()
        self.Model = "OSP1x0"

    #####################################################################
    ### OSP Switching Functions
    #####################################################################
    def Get_OSP_Info(self):
        return self.query('DIAG:SERV:HWIN?').split(',')

    def Get_OSP_Modules(self):
        rdstr = self.query('ROUT:MOD:CAT?')
        return rdstr

    def Get_SW_SPDT(self,slot=11,sw=1):
        """ Slot, Switch """
        # ROUT:CLOS? (@F01A11(0161))
        outstr = f'ROUT:CLOS? (@F01A{slot:02d}(01{sw:02d}))'
        print(outstr)
        state = self.queryInt(outstr)
        print("A%02d SW%d @Pos%d"%(slot,sw,state))
        return int(state)

    def Get_SW_SP6T(self,slot=11,sw=1):
        """ Slot, Switch """
        # ROUT:CLOS? (@F01A11(0161))
        for pos in range(0,7):
            state = self.queryInt('ROUT:CLOS? (@F01A%02d(%02d%02d))'%(slot,pos,sw))[0]
            if state == 1:
                CurrState = pos
                print(f"A{slot:02d} SW{sw:02d} @Pos{pos:02d}")
        return CurrState

    def Set_CompatabilityMode(self,sState):
        """
            F01Mxx --> F01A1x nomenclature
            ON OFF 1 0
        """
        self.write(f'CONF:COMP {sState}')

    def Set_SW(self,slot=11,sw=1,pos=1):
        # ROUT:CLOS (@F01A11(0161))
        outstr = f'ROUT:CLOS (@F01A{slot:02d}({pos:02d}{sw:02d}))'
        print(outstr)
        self.write(outstr)

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    RFU3 = OSP()
    RFU3.jav_openvisa('TCPIP0::192.168.1.150::INSTR')
    RFU3.Set_CompatabilityMode(1)
    print(RFU3.Get_OSP_Info())
    print(RFU3.Get_SW_SPDT(11,12))
    RFU3.Set_SW(11,12,0)
    # RFU3.query('ROUT:CLOS? (@F01A11(0111))')
    RFU3.jav_ClrErr()
