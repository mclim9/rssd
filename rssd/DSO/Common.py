"""Digital Storage Oscilloscope Common Functions"""
###############################################################################
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

class DSO(jaVisa):
    """ Rohde & Schwarz Digital Storage Oscilloscope Object """
    def __init__(self):
        super(DSO, self).__init__()
        self.Model = "DSO"

#####################################################################
### DSO Get Functions
#####################################################################
    def Get_AcqTime(self):
        """ Seconds """
        rdStr = self.query(f':TIM:RANG?')
        return rdStr

    def Get_ChState(self, ch=1):
        rdStr = self.query(f':chAN{ch}:STAT?')
        return rdStr

    def Get_SamplingRate(self):
        """ MHz? """
        rdStr = self.query(f':ACQ:SRR?')
        return rdStr

    def Get_TimeRes(self):
        """ Seconds """
        rdStr = self.query(f':ACQ:RES?')
        return rdStr

    def Get_TimeScale(self):
        """ Seconds """
        rdStr = self.query(f':TIM:SCAL?')
        return rdStr

    def Get_Trace(self,ch,Wave):
        """ ASCII Trace """
        self.write(f'FORM ASCII')
        YVals = self.query(f':chAN{ch}:WAV{Wave}:DATA?')
        Headr = self.queryFloatArry(f':chAN{ch}:WAV{Wave}:DATA:HEAD?')
        Start = Headr[0]
        Stops = Headr[1]
        Sampl = Headr[2]
        return YVals

###############################################################################
###  DSO Get Cursor Functions
###############################################################################

    def Get_Cursor_X_Delta(self, ch=1):
        rdStr = self.query(f':CURS{ch}:XDEL:VAL?')
        return rdStr

    def Get_Cursor_X_Delta_Inverse(self, ch=1):
        rdStr = self.query(f':CURS{ch}:XDEL:INV?')
        return rdStr

    def Get_Cursor_Y_Delta(self, ch=1):
        rdStr = self.query(f':CURS{ch}:YDEL:VAL?')
        return rdStr

    def Get_Cursor_Y_Delta_Slope(self, ch=1):
        rdStr = self.query(f':CURS{ch}:YDEL:SLOP?')
        return rdStr

###############################################################################
###  DSO Get Measurement Functions
###############################################################################

    def Get_Meas_Res_Actual(self, mode, ch=1):
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        rdStr = self.query(f':MEAS{ch}:RES:ACT? {mode}')
        return rdStr

    def Get_Meas_Res_Average(self, mode, ch=1):
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        rdStr = self.query(f':MEAS{ch}:RES:AVG? {mode}')
        return rdStr

    def Get_Meas_Res_Event_Count(self, mode, ch=1):
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        rdStr = self.query(f':MEAS{ch}:RES:EVTC? {mode}')
        return rdStr

    def Get_Meas_Res_Negetive_Peak(self, mode, ch=1):
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        rdStr = self.query(f':MEAS{ch}:RES:NPE? {mode}')
        return rdStr

    def Get_Meas_Res_Positive_Peak(self, mode, ch=1):
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        rdStr = self.query(f':MEAS{ch}:RES:PPE? {mode}')
        return rdStr

    def Get_Meas_Res_Reliability(self, mode, ch=1):
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        rdStr = self.query(f':MEAS{ch}:RES:REL? {mode}')
        return rdStr

    def Get_Meas_Res_RMS(self, mode, ch=1):
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        rdStr = self.query(f':MEAS{ch}:RES:RMS? {mode}')
        return rdStr

    def Get_Meas_Res_Wave_Count(self, mode, ch=1):
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        rdStr = self.query(f':MEAS{ch}:RES:WFMC? {mode}')
        return rdStr

    def Get_Meas_Res_Std_Dev(self, mode, ch=1):
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        rdStr = self.query(f':MEAS{ch}:RES:STDD? {mode}')
        return rdStr  

#####################################################################
### DSO Init Functions
#####################################################################
    def Init_Measurement(self):
        #Configure instrument measurment
        pass


#####################################################################
### DSO Set Functions
#####################################################################
    def Set_AcqTime(self, sec):
        """ Seconds """
        self.write(f':TIM:RANG {sec}')

    def Set_Autoset(self):
        self.write(f':AUT')

    def Set_ChCoupling(self, state, ch=1):
        """ AC DC DCL """
        self.write(f':chAN{ch}:COUP {state}')        #Display Update State

    def Set_ChStatus(self, state, ch=1):
        """ ON OFF """
        self.write(f':chAN{ch}:STAT {state}')        #Display Update State

    def Set_ChState(self, state, ch=1):
        """ ON OFF """
        self.write(f':chAN{ch}:STAT {state}') 

    def Set_DisplayUpdate(self, state):
        """ ON OFF """
        self.write(f'SYST:DISP:UPD {state}')        #Display Update State

    def Set_System_Preset(self):
        self.write(f'SYST:PRES') 

    def Set_SweepCont(self, state):
        """ ON OFF """
        if ('ON' in state.upper()) or (state == 1):
            self.write(f'RUN')                      #Continuous
        else:
            self.write(f'SING')                     #Single

    def Set_TimeRef(self, sec):
        """ Seconds """
        self.write(f':TIM:REF {sec}')

    def Set_TimeScale(self, sec):
        """ Seconds """
        self.write(f':TIM:SCAL {sec}')

    def Set_TimeRes(self, sec):
        """ Seconds """
        self.write(f':ACQ:RES {sec}')

    def Set_VoltOffset(self, volt, ch=1):
        """ Volts """
        self.write(f':chAN{ch}:OFFS {volt}')

    def Set_VoltRange(self, volt, ch=1):
        """ Volts """
        self.write(f':chAN{ch}:RANG {volt}')

    def Set_VoltScale(self, volt, ch=1):
        """ Volts """
        self.write(f':chAN{ch}:SCAL {volt}')

###############################################################################
###  DSO Set Cursor Functions
###############################################################################
    def Set_Cursor_All_Off(self,ch=1):    
        """  1 to 4 """
        self.write(f':CURS{ch}:AOFF') 

    def Set_Cursor_State(self, state, ch=1):   
        """ ON OFF , 1 to 4 """
        self.write(f':CURS{ch}:STAT {state}') 

    def Set_Cursor_Source(self,source,ch=1):   
        """ ON OFF , Mx CxWx x = 1 to 4 """
        self.write(f':CURS{ch}:SOUR {source}') 

    def Set_Cursor_Function(self,function,ch=1):   
        """ HOR VERT PAIR ,  1 to 4 """
        self.write(f':CURS{ch}:FUNC {function}')

    def Set_Cursor_Tracking(self, state, ch=1):   
        """ ON OFF ,  1 to 4 """
        self.write(f':CURS{ch}:TRAC:STAT {state}')

    def Set_Cursor_Style(self, style,ch=1):   
        """ LINe LRHombus VLRHombus RHOMbus ,  1 to 4 """
        self.write(f':CURS{ch}:STYL {style}')

    def Set_Cursor_Max_Peak(self,ch=1):   
        """  1 to 4 """
        self.write(f':CURS{ch}:MAX:PEAK')

###############################################################################
###  DSO Set Measurement Functions
###############################################################################

    def Set_Meas_All_Off(self,ch=1):   
        """  1 to 8 """
        self.write(f':MEAS{ch}:AOFF')

    def Set_Meas_All_On(self,ch=1):   
        """  1 to 8 """
        self.write(f':MEAS{ch}:AON')

    def Set_Meas_Additional(self, mode, state, ch=1):   
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        self.write(f':MEAS{ch}:ADD {mode} {state}')

    def Set_Meas_Clear_Statistics(self, ch=1):
        """ Clear Statistics """
        self.write(f':MEAS{ch}:CLE')

    def Set_Meas_Main(self, mode, ch=1):   
        """ HIGH LOW AMP MAX MIN PDELta MEAN RMS STDD POVershoot 
            AREA RTIMe FTIMe PPULse PER FREQ PULCnt DELay ..."""
        self.write(f':MEAS{ch}:MAIN {mode}')

    def Set_Meas_Enable(self, mode, ch=1):
        """ ON OFF, ch """
        self.write(f':MEAS{ch}:ENAB {mode}')
    
    def Set_Meas_Source(self, mode, ch=1):
        """ CxWx, ch """
        self.write(f':MEAS{ch}:ENAB {mode}')

    def Set_Meas_Statistics(self, state, ch=1):   
        """ ON OFF , ch """
        self.write(f':MEAS{ch}:STAT:ENAB {state}')
###############################################################################
###  DSO Set Display Functions
###############################################################################
    def Set_Meas_Display_Position(self, mode):   
        """ PREView FLOAt DOCK """
        self.write(f':DISP:RES:DEF {mode}')

###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    DSO_Inst = DSO().jav_Open("192.168.1.100")
    DSO_Inst.jav_IDN()
    DSO_Inst.jav_ClrErr()
    