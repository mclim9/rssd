"""Phase Noise Analyzer Common Functions"""
from rssd.yaVISA import jaVisa              # pylint: disable=E0611,E0401

class PNA(jaVisa):
    """ Rohde & Schwarz Vector Signal Analyzer Object """
    def __init__(self):
        super(PNA, self).__init__()
        self.Model = "FSWP"

    ############################################################################
    ### FSW Get
    ############################################################################
    def Get_AttnMech(self):
        out = self.queryInt('INP:ATT?')
        return out

    def Get_Channels(self):                                                     #done
        ChList = self.query('INST:LIST?').split(',')
        return(ChList)

    def Get_Freq(self):                                                         #done
        rdStr = self.queryFloat(':SENS:FREQ:CENT?')
        return rdStr

    def Get_FreqLock(self):                                                     #done
        rdstr = self.query(':STAT:QUES:PNO:COND?')
        return rdstr

    def Get_IFOvld(self):
        self.Set_InitImm()
        rdStr = self.query("STAT:QUES:POW:COND?").strip()
        return rdStr

    def Get_Harm_Values(self):
        rdStr = 'TBD'
        return rdStr

    def Get_Mkr_Freq(self,iNum=1,iWind=1):
        MkrFreq = self.queryFloat(':CALC%d:MARK%d:X?'%(iWind,iNum))
        return float(MkrFreq)

    def Get_Mkr_XY(self,iNum=1,iWind=1):
        ValX = self.query(':CALC%d:MARK%d:X?'%(iWind,iNum)).strip()
        ValY = self.query(':CALC%d:MARK%d:Y?'%(iWind,iNum)).strip()
        return [ValX, ValY]

    def Get_Mkr_Y(self,iNum=1,iWind=1):
        ValY = self.queryFloat(':CALC%d:MARK%d:Y?'%(iWind,iNum))
        return ValY

    def Get_Ovld_Stat(self):
        self.Set_InitImm()
        Read = self.queryInt('STAT:QUES:POW:COND?')
        RF_Ovld = Read & 1      # pylint: disable=W0612
        RF_Udld = Read & 2      # pylint: disable=W0612
        IF_Ovld = Read & 4      # pylint: disable=W0612
        return Read

    def Get_Power(self):
        rdStr = self.query('POW:RLEV?')
        return rdStr

    def Get_PN_Decade(self):
        """Phase Noise per decade (Spot Noise)"""
        rdStr = self.query('CALC:SNO:DEC:Y?')
        return rdStr

    def Get_PN_Int(self):
        """Integrated Phase Noise
        :FETC<n>:RANG<j>:PNO<t>:IPN?
        <n>   : Window
        <j>   : Integration Range
        <t>   : Trace """
        rdStr = self.query(':FETC:RANG:PNO:IPN?')
        return rdStr

    def Get_RefLevel(self):
        RefLvl = self.queryFloat('DISP:TRAC:Y:RLEV?')
        return RefLvl

    def Get_Screenshot(self,file='screenshot'):
        ### File will be in FSW's C:\R_S\Instr\User
        self.write(f'MMEM:NAME "C:\\R_S\\INSTR\\USER\\{file}"')
        self.write('HCOP:CONT WIND')     #Print Displayed Windo
        self.write('HCOP:CMAP:DEF4')     #Screeen Colors
        self.write('HCOP:DEST "MMEM"')   #Send Data to file
        self.write('HCOP:DEV:LANG JPG')  #Save JPG
        self.write('HCOP:IMM')           #Create File

    def Get_SweepPoints(self):
        rdStr = self.queryInt(':SENS:SWE:POIN?')            #Number of trace points
        return rdStr

    def Get_SweepTime(self):
        rdStr = self.queryFloat('SENS:SWE:TIME?')           #Sweep/Capture Time
        return rdStr

    def Get_SweepType(self):
        #AUTO | SWE | FFT
        rdStr = self.query(':SENS:SWE:TYPE?')
        return rdStr

    def Get_SweepParams(self):
        # ,SwpTime,SwpPts,SwpType,SwpOpt,
        Pts = self.Get_SweepPoints()
        Tim = self.Get_SweepTime()
        Typ = self.Get_SweepType()
        return f'{Tim},{Pts},{Typ}'

    def Get_Trace_Data(self,trace=1):
        self.write('FORM ASCII ')
        DataY = self.query('TRAC%d:DATA? TRACE1'%trace)
        DataX = self.query('TRAC%d:DATA:X? TRACE1'%trace)
        return [DataX.split(','),DataY.split(',')]

    ###########################################################################
    ### Measurement Init
    ###########################################################################
    def Init_Harm(self):
        self.Set_Channel("Spectrum")
        self.write('CALC:MARK:FUNC:HARM ON')

    def Init_PhaseNoise(self):
        self.Set_Channel("Spectrum")
        self.write('CALC:MARK:FUNC:HARM ON')

    def Init_Spectral(self):
        self.Set_Channel("Spectrum")

    ###########################################################################
    ### Set Methods
    ###########################################################################
    def Set_AttnMech(self,fMAttn):
        #self.write('INP:EATT:STAT OFF')
        self.write('INP:ATT %.0f'%fMAttn)

    def Set_AttnAuto(self):
        self.write(':INP:ATT:AUTO ON')

    def Set_Autolevel(self):
        self.query(':SENS:ADJ:LEV;*OPC?')

    def Set_Autolevel_Proto(self,sState):
    ### Used by WLAN; K96.  Please use ADJ:LEV;
        self.write('CONF:POW:AUTO %s;*WAI'%sState)          #ON|OFF|1|0

    def Set_Channel(self,Chan,sName=""):
        """ SAN, IQ, NR5G, LTE, WLAN, PNOISE, NOISE, SPUR, ADEM, DDEM, V5GT, AMPL """
        if sName == "":
            sName = Chan
        ChList = self.query('INST:LIST?').split(',')
        #print("Chan:%s in %s"%(Chan,ChList))
        if ("'" + sName + "'") in ChList:
            pass
        else:
            self.query(":INST:CRE %s,'%s';*OPC?"%(Chan,sName))
        self.query(":INST:SEL '%s';*OPC?"%sName)

    def Set_DisplayUpdate(self,state):
        self.write('SYST:DISP:UPD %s'%state)                #Display Update State

    def Set_Freq(self,fFreq):
        self.write(':SENS:FREQ:CENT %.0f HZ'%fFreq)

    def Set_FreqStart(self,fFreq):                          #done
        self.write(':SENS:FREQ:STAR %f'%fFreq)

    def Set_FreqStep(self,fFreq):
        self.write(':SENS:FREQ:STEP %f'%fFreq)

    def Set_FreqStop(self,fFreq):                           #done
        self.write(':SENS:FREQ:STOP %f'%fFreq)

    def Set_Harm_num(self, num):
        self.write(f':CALC1:MARK1:FUNC:HARM:NHAR {num}')

    def Set_Harm_adjust(self):
        """ Adjusts Ref Lvl, Attn, SwpTime """
        self.write(':CALC1:MARK1:FUNC:HARM:PRE')

    def Set_InitImm(self):
        self.query('INIT:IMM;*OPC?')

    def Set_Input(self,sType):
        self.write('INP:SEL %s'%sType)                      #RF|AIQ|DIQ|FILE

    def Set_Mkr_AllOff(self,iWind=1):
        self.write(':CALC%d:MARK:AOFF'%(iWind))

    def Set_Mkr_Freq(self,fFreq,iNum=1,iWind=1):
        self.write(':CALC%d:MARK%d:X %fHz'%(iWind,iNum,fFreq))

    def Set_Mkr_Next(self,iNum=1,iWind=1):
        self.write(':CALC%d:MARK%d:MAX:NEXT'%(iWind,iNum))

    def Set_Mkr_On(self,iNum,iWind=1):
        self.write(':CALC%d:MARK%d ON'%(iWind,iNum))

    def Set_Mkr_Peak(self,iNum=1,iWind=1):
        self.write(':CALC%d:MARK%d:MAX:PEAK'%(iWind,iNum))

    def Set_Preamp(self,sState):
        #ON|OFF|1|0
        self.write('INP:GAIN:STAT %s;*WAI'%sState)

    def Set_PwrThreshold(self,dBm):
        self.write(f'SENS:ADJ:CONF:LEV:THR {dBm}')

    def Set_RefLevel(self,fReflevel):
        self.write('DISP:WIND:TRAC:Y:SCAL:RLEV %fdBm'%fReflevel)

    def Set_ResBW(self,fFreq):
        if fFreq == 0:
            self.write(':SENS:BAND:RES:AUTO ON')
        else:
            self.write(':SENS:BAND:RES %f'%fFreq)

    def Set_SamplingRate(self,fFreq):
        self.write('TRAC:IQ:SRAT %f'%fFreq)

    def Set_Span(self,fFreq):
        self.write('SENS:FREQ:SPAN %f'%fFreq)

    def Set_SweepType(self,sType):
        #AUTO | SWE | FFT
        self.write(f':SENS:SWE:TYPE {sType}')

    def Set_SweepOpt(self,sOpt):
        #AUTO | SPEed | DYN
        self.write(f':SENS:SWE:OPT {sOpt}')

    def Set_SweepCont(self,iON):
        ''' 0 1 '''
        if iON == 1:
            self.write('INIT:CONT ON')                      #Continuous Sweep
        else:
            self.write('INIT:CONT OFF')                     #Single Sweep

    def Set_SweepPoints(self,iNum):
        self.write(':SENS:SWE:POIN %f'%iNum)                #Number of trace points

    def Set_Trace_Avg(self,sType,trace=1):
        """LIN VID POW"""
        self.write('DISP:TRAC%d:MODE AVER'%trace)
        self.write('SENS:DET1:FUNC AVER')
        self.write('SENS:AVER:TYPE %s'%sType)               #LIN|VID

    def Set_Trace_AvgCount(self,iAvg):
        self.write('SENS:SWE:COUN %d'%(iAvg))

    def Set_Trace_AvgOff(self,trace=1):
        self.write('DISP:TRAC%d:MODE WRIT'%(trace))

    def Set_Trace_Detector(self,sDetect,iWind=1):
        """APE; NEG; POS; QPE; SAMP; RMS; CAV; CRMS"""
        self.write('SENS:WIND%d:DET %s'%(iWind,sDetect))

    def Set_VidBW(self,fFreq):
        if fFreq == 0:
            self.write(':SENS:BAND:VID:AUTO ON')
        else:
            self.write(':SENS:BAND:VID %f'%fFreq)

    def Set_Xcorr(self,iNum):                               #done
        self.write(f':SENS:SWE:XFAC {iNum}')

    def Set_XcorrOpt(self,State):                           #done
        """1 0"""
        if State in (1, '1', 'ON'):
            self.write(f':SENS:SWE:XOPT:STAT ON')
        else:
            self.write(f':SENS:SWE:XOPT:STAT OFF')

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    FSWP = PNA().jav_Open("192.168.1.108")
    print(FSWP.Get_Freq())
    print(FSWP.Get_PN_Int())
    FSWP.jav_ClrErr()
    del FSWP
