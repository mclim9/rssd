# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Vector Signal Analyzer Common Functions
### Author:  Martin C Lim
### Date:    2018.02.01
#####################################################################
from rssd.yaVISA import jaVisa              # pylint: disable=E0611,E0401
try:
    import rssd.VSA_Leveling as VSAL        # pylint: disable=E0611,E0401
except:
    pass

class VSA(jaVisa):
    """ Rohde & Schwarz Vector Signal Analyzer Object """
    def __init__(self):
        super(VSA, self).__init__()
        self.Model = "FSW"
        
    #####################################################################
    ### FSW Get
    #####################################################################
    def Get_ACLR(self):
        ACLR = self.query(':CALC:MARK:FUNC:POW:RES? MCAC')
        return ACLR

    def Get_Mkr_BandACLR(self):
        for i in range(1,3+1):
            if i == 1:
                ACLR = f'{self.Get_Mkr_Band(i)[1]:7.3f}'
            else:
                ACLR = f'{ACLR},{self.Get_Mkr_Band(i)[1]:7.3f}'
        return ACLR

    def Get_Params_Amp(self,header=0):
        """Retrieve Parameters for test logs"""
        if header != 1:
            attn    = self.Get_AttnMech()
            prea    = self.Get_Preamp()
            refl    = self.Get_RefLevel()
            outStr  = f'{attn:2d},{prea},{refl:7.3f}'
        else:
            outStr = 'Attn,PreAmp,RefLvl'
        return outStr

    def Get_AttnMech(self):
        out = self.queryInt('INP:ATT?')
        return out 

    def Get_CCDF(self):
        P10_00 = self.queryFloat(f'CALC:STAT:CCDF:X1? P10;*WAI')
        P01_00 = self.queryFloat(f'CALC:STAT:CCDF:X1? P1;*WAI')
        P00_10 = self.queryFloat(f'CALC:STAT:CCDF:X1? P0_1;*WAI')
        P00_01 = self.queryFloat(f'CALC:STAT:CCDF:X1? P0_01;*WAI')
        CrestF = self.queryFloat(f'CALC:STAT:RES? CFAC')
        return f'{CrestF:.4f},{P10_00:.2f},{P01_00:.2f},{P00_10:.2f},{P00_01:.2f}'

    def Get_ChPwr(self):
        out = self.queryFloat('FETC:SUMM:POW?')
        return out 

    def Get_ChannelName(self):
        ChList  = self.Get_Channels()
        CurrApp = self.query('INST?')
        match   = [x for x in ChList if CurrApp in x]
        index   = ChList.index(match[0])
        self.CurrCh  = ChList[index+1]
        return(self.CurrCh)

    def Get_Channels(self):
        ChList  = self.query('INST:LIST?').replace("\'","").split(',')
        return ChList

    def Get_EVM(self):
        #EVM = self.query('FETC:SUMM:EVM:ALL:AVER?')
        out = self.queryFloat('FETC:SUMM:EVM?;*WAI').strip()
        return out

    def Get_Params_EVM(self):
        MAttn   = self.Get_AttnMech()
        RefLvl  = self.Get_RefLevel()
        Power   = self.Get_ChPwr()
        EVM     = self.Get_EVM()
        return f"{MAttn:.2f},{RefLvl:.2f},{Power:6.2f},{EVM:.2f}"

    def Get_Freq(self):
        rdStr = self.queryFloat(':SENS:FREQ:CENT?')
        return rdStr

    def Get_Harm(self):
        rdStr = self.queryFloatArry(':CALC:MARK:FUNC:HARM:LIST?')
        return rdStr

    def Get_IFOvld(self):
        self.Set_InitImm()
        rdStr = self.query("STAT:QUES:POW:COND?").strip()
        return rdStr

    def Get_IQ_Data(self,sFilename="file.iqw"):
        ####################################################################
        """ Get the IQ data and store to IQW file to process in VSE """
        ####################################################################
        self.write("FORM REAL,32")
        self.write("TRAC:IQ:DATA:FORM IQP")
        self.write("TRAC:IQ:DATA?")
        data = self.jav_read_raw()

        samples = self.Get_IQ_RecLength()

        # Read num of digits to get for No of floats
        if int(samples) < 125000000:
          digits = data[1]
        else:
          digits = "10"

        """
        # Don't need this but including for completeness
        # Reads total number of bytes that holds IQ data

        i = 2
        totalbytes = ""
        while i <= int(digits)+1:
          totalbytes = totalbytes + data [i]
          i += 1
        """
          
        iqfile = open (sFilename, "wb")
        iqfile.write(data[2 + int(digits):])
        iqfile.close()

    def Get_IQ_Data_Ascii(self,MLEN=1e3):
        CSVd = ""
        self.write('Format:DATA ASCII')        
        self.write('TRAC:IQ:DATA:FORM IQP')
        RLEN = self.Get_IQ_RecLength()                  #Sweep Points
        numLoops  = int(round(RLEN/MLEN))+1
        for i in range(numLoops):                      # pylint: disable=E0602
            SCPI = "TRAC:IQ:DATA:MEM? %d,%d"%((i * MLEN),MLEN)  #TRAC:IQ:DATA:MEM? <MemStrt>,<MLEN>
            CSVd = CSVd + self.query(SCPI)                #IQ Dump
        print("Memory Done Reading %d"%len(CSVd.split(',')))
        return CSVd

    def Get_IQ_Data_Ascii2(self,MLEN=1e3):
        CSVd = ""
        self.write('FORMAT:DATA ASCII')
        self.write('TRAC:IQ:DATA:FORM IQP')
        CSVd = self.query("TRAC:IQ:DATA:MEM?")
        #print("Memory Done Reading %d"%len(CSVd.split(',')))
        return CSVd

    def Get_IQ_Data_Bin(self):
        import struct
        self.write('FORMAT:DATA REAL,32')
        self.write('TRAC:IQ:DATA:FORM IQP')
        self.write('TRAC:IQ:DATA:MEM?')
        rdStr = self.K2.read_raw()
        numBytes = int(chr(rdStr[1]))       # Number of Bytes
        numIQ    = int(rdStr[2:2+numBytes])
        IQBytes  = rdStr[(numBytes+2):-1]    # Remove Header
        IQAscii  = struct.unpack("<" + 'f' * int(numIQ/4),IQBytes)
        return IQBytes

    def Get_IQ_RecLength(self):
        RLEN = self.queryInt('TRAC:IQ:RLEN?')	        #Record(Samples) Length
        return RLEN

    def Get_IQ_SamplingRate(self):
        # SamplingRate = IQ_BW / 0.8
        rdStr = self.queryFloat('TRAC:IQ:SRAT?')        #Sampling Rate
        return rdStr

    def Get_Mkr_Band(self,iNum=1,iWind=1):
        ValX = self.queryFloat(':CALC%d:MARK%d:X?'%(iWind,iNum))
        ValY = self.queryFloat(':CALC%d:MARK%d:FUNC:BPOW:RES?'%(iWind,iNum))
        return [ValX, ValY]

    def Get_Mkr_Freq(self,iNum=1,iWind=1):
        MkrFreq = self.queryFloat(':CALC%d:MARK%d:X?'%(iWind,iNum))
        return float(MkrFreq)

    def Get_Mkr_Noise(self,iNum=1,iWind=1):
        ValX = self.queryFloat(':CALC%d:MARK%d:X?'%(iWind,iNum))
        ValY = self.queryFloat(':CALC%d:MARK%d:FUNC:NOIS:RES?'%(iWind,iNum))
        return [ValX, ValY]

    def Get_Mkr_TimeDomain(self,iNum=1,iWind=1):
      # self.write(':CALC:MARK%d:FUNC:SUMM:STAT ON'%iNum)
        #MkrFreq = self.query(':CALC%d:MARK%d:X?'%(iWind,iNum)).strip()
        MkrPwr  = self.query(':CALC%d:MARK%d:FUNC:SUMM:RMS:RES?'%(iWind,iNum)).strip()
        return float(MkrPwr)

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

    def Get_Preamp(self):
        return self.queryInt(f'INP:GAIN:STAT?')

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

    def Get_SweepOpt(self):
        #AUTO | SPEed | DYN
        rdStr = self.query(':SENS:SWE:OPT?')
        return rdStr
        
    def Get_SweepPoints(self):
        rdStr = self.queryInt(':SENS:SWE:POIN?')                 #Number of trace points
        return rdStr

    def Get_SweepTime(self):
        rdStr = self.queryFloat('SENS:SWE:TIME?')                 #Sweep/Capture Time
        return rdStr

    def Get_SweepType(self):
        #AUTO | SWE | FFT
        rdStr = self.query(':SENS:SWE:TYPE?')
        return rdStr

    def Get_Params_Sweep(self,header=0):
        # SwpTime,SwpPts,SwpType,SwpOpt,
        if header != 1:
            Time    = self.Get_SweepTime()
            Points  = self.Get_SweepPoints()
            Type    = self.Get_SweepType()
            Opt     = self.Get_SweepOpt()
            outStr  = f'{Time:5.3f},{Points},{Type},{Opt}'
        else:
            outStr  = 'SwpTimeM,SwpPts,SwpType,SwpOpt'
        return outStr

    def Get_System_ErrorExt(self):
        rdStr = self.query(':SYST:ERR:EXT? ALL')
        return rdStr

    def Get_Params_System(self,header=0):
        if header != 1:
            error  = self.jav_Error()
            ext    = self.Get_System_ErrorExt().replace('"','')
            outStr = f'{error[0]:>4},{error[1]:10.10},{ext:10.10}'
        else:
            outStr  = 'ErrNo,ErrMsg,ExtError'
        return outStr

    def Get_Trace_Data(self,trace=1):
        self.write('FORM ASCII ')
        DataY = self.query('TRAC%d:DATA? TRACE1'%trace)
        DataX = self.query('TRAC%d:DATA:X? TRACE1'%trace)
        return [DataX.split(','),DataY.split(',')]

    def Get_Trace_Detector(self,trace=1):
        rdStr = self.query(f'SENS:WIND1:DET{trace}?')
        return rdStr

    def Get_Trace_Mode(self,trace=1):
        rdStr = self.query(f'DISP:TRAC{trace}:MODE?')
        return rdStr

    def Get_Params_Trace(self,header=0,trace=1):
        if header != 1:
            mode    = self.Get_Trace_Mode(trace)
            detect  = self.Get_Trace_Detector(trace)
            avgtype = self.Get_Trace_AvgType()
            outStr  = f'{mode},{detect},{avgtype}'
        else:
            outStr  = 'TrcMode,TrcDet,AvgMode'
        return outStr

    def Get_Trace_AvgType(self):
        rdStr   = self.query('SENS:AVER:TYPE?')
        return rdStr

    #####################################################################
    ### Measurement Init
    #####################################################################
    def Init_ACLR(self, sName=""):
        self.Set_Channel("SAN",sName)
        # self.Set_ChannelName("Spectrum",sName)
        self.write('CALC:MARK:FUNC:POW:SEL ACP')

    def Init_CCDF(self, sName=""):
        self.Set_Channel("Spectrum",sName)
        self.write('CALC:STAT:CCDF ON;*WAI')

    def Init_Harm(self, sName=""):
        self.Set_Channel("Spectrum",sName)
        self.write('CALC:MARK:FUNC:HARM ON')

    def Init_IQ(self, sName=""):
        self.Set_Channel("IQ",sName)

    #####################################################################
    ### Set Methods
    #####################################################################
    #####################################################################
    ### FSW ACLR
    #####################################################################
    def Set_ACLR_AdjBW(self,dCHBW):
        self.write(f'POW:ACH:BAND:ACH {dCHBW};ALT1 {dCHBW};ALT2 {dCHBW}')

    def Set_ACLR_AdjSpace(self,dCHBW):
        self.write(f'POW:ACH:SPAC:ACH {dCHBW};ALT1 {2*dCHBW};ALT2 {3*dCHBW}')

    def Set_ACLR_CHBW(self,dCHBW):
        self.write('POW:ACH:BAND %d'%dCHBW)

    def Set_ACLR_NumAdj(self,iAdj):
        self.write(f'POW:ACH:ACP {iAdj}')                           #two adjacent channels

    def Set_AttnMech(self,fMAttn):
        #self.write('INP:EATT:STAT OFF')
        self.write('INP:ATT %.0f'%fMAttn)

    def Set_AttnAuto(self):
        self.write(':INP:ATT:AUTO ON')

    def Set_Autolevel(self):
        self.query(':SENS:ADJ:LEV;*OPC?')

    def Set_Autolevel_Proto(self,sState):
    ### Used by WLAN; K96.  Please use ADJ:LEV;
        self.write('CONF:POW:AUTO %s;*WAI'%sState)      #ON|OFF|1|0

    def Set_Autolevel_IFOvld(self):
        ####################################################################
        """ Algorithm designed by Darren Tipton, RSUK"""
        """ Optimise level for Mixer Input => Optimal EVM """
        """ Optimises for signals using IF gain as well as 1dB steps """     
        ####################################################################
        optmix = 10                            # Optimal mixer level
        self.Set_SweepCont(0)
        self.Set_Autolevel()
        level = self.Get_Mkr_TimeDomain()
        
        """ Switch Pre-Amp """                                                                                 
        if level >= -20:
            self.query("INP:GAIN:STAT OFF; *OPC?")
            gain = 0
            maxmix = 0
        else:
            self.query("INP:GAIN:STAT ON; *OPC?")      
            gain = 20
            maxmix = -30
        
        rfatt = level + gain - optmix       #Calc RfAttn for optimal mixer level
        if rfatt < 0: rfatt = 0             #If calculated RF atten < 0, set 0
        self.Set_AttnMech(rfatt)            #Set Attenuation
         
        reflev = maxmix + rfatt
        self.Set_RefLevel(reflev)          #Set RefLevel

        ifovl = self.Get_Ovld_Stat()      #Check Overload
        print ("Inital: Ovl:%d Attn:%d RfLvl:%d"%(ifovl,rfatt,reflev))

        """ Optimising for attenuation """
        while ifovl != 0:
            print ("ATloop: Ovl:%d Attn:%d RfLvl:%d"%(ifovl,rfatt,reflev))
            rfatt = rfatt + 1
            self.Set_AttnMech(rfatt)

            reflev = maxmix + rfatt
            self.Set_RefLevel(reflev)

            """ Check if there is IF Overload """
            ifovl = self.Get_Ovld_Stat()

        """ Optimising for reference level """
        while reflev > (-20 - gain) and ifovl == 0:
            print ("RefLop: Ovl:%d Attn:%d RfLvl:%d"%(ifovl,rfatt,reflev))
            reflev = reflev - 1
            self.Set_RefLevel(reflev)

            """ Check if there is IF Overload """          
            ifovl = self.Get_Ovld_Stat()
         
        """ Final check for IF Overload """
        if ifovl != 0:
            reflev = reflev + 1
            self.Set_RefLevel(reflev)
        print ("Final : Ovl:%d Attn:%d RfLvl:%d"%(ifovl,rfatt,reflev))

    def Set_Autolevel_IQIF(self,tables):
        VSAL.Optimise_FSx_Level(self,tables)

    #####################################################################
    ### FSW CCDF
    #####################################################################
    def Set_CCDF(self,sState):
        self.write(f'CALC:STAT:CCDF {sState} ;*WAI') #ON|OFF|1|0

    def Set_CCDF_BW(self,BW):
        self.Set_ResBW(BW)

    def Set_CCDF_Samples(self,iSamples):
        self.write(f'CALC:STAT:NSAM {iSamples}')

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

    def Set_ChannelName(self,newName,oldName):
        self.write(f":INST:REN '{newName}', '{oldName}'")

    def Set_ChannelSelect(self,sName):
        self.query(":INST:SEL '%s';*OPC?"%sName)

    def Set_DisplayUpdate(self,state):
        self.write('SYST:DISP:UPD %s'%state)      #Display Update State
         
    #####################################################################
    ### FSW Equalization K544
    #####################################################################
    def Set_EQ_File(self,sFile):
        #self.write('SENS:CORR:FRES:Input1:USER:SLIS1:SEL "c:\\R_S\\Instr\\Debug\\K544\\IFH.s2p"')
        self.write('SENS:CORR:FRES:Input1:USER:SLIS1:SEL "%s"'%sFile)
        
    def Set_EQ_State(self,sState):
        FSW.write('SENS:CORR:FRES:Input1:USER:PRES')
        self.write('SENS:CORR:FRES:Input1:USER:STATe %s'%sState)

    def Set_Freq(self,fFreq):
        """Hz"""
        self.write(':SENS:FREQ:CENT %.0f HZ'%fFreq)

    def Set_FreqStart(self,fFreq):
        """Hz"""
        self.write(':SENS:FREQ:STAR %f'%fFreq)

    def Set_FreqStep(self,fFreq):
        """Hz"""
        self.write(':SENS:FREQ:STEP %f'%fFreq)

    def Set_FreqStop(self,fFreq):
        """Hz"""
        self.write(':SENS:FREQ:STOP %f'%fFreq)

    def Set_Harm_num(self, num):
        self.write(f':CALC1:MARK1:FUNC:HARM:NHAR {num}')

    def Set_Harm_adjust(self):
        """ Adjusts Ref Lvl, Attn, SwpTime """
        self.write(':CALC1:MARK1:FUNC:HARM:PRE')
    #####################################################################
    ### FSW IQ Analyzer
    #####################################################################
    def Set_IQ_ACLR(self, ChBW, ChSpace):
        ## Author: Darren Tipton, RSUK
        Freq = self.Get_Freq()

        #Configure Advanced FFT parameters
        self.Set_IQ_Adv_Mode()
        self.Set_IQ_Adv_TransAlgo('AVER')
        self.Set_IQ_Adv_FFTLenth(16384)                     #Reduce RBW
        self.Set_IQ_Adv_Window('BLAC')
        self.Set_IQ_Adv_WindowLenth(16384)                  #Reduce RBW

        self.Set_IQ_BW(3.1*ChSpace)
        self.Set_IQ_SpectrumWindow()                        # Add Spectrum Trace
        self.Set_Trace_Detector('RMS')                      # RMS detector
        self.Set_Mkr_Freq(Freq,1)                           # Tx Freq
        self.Set_Mkr_Band(ChBW,1)                           # Tx RFBW
        self.Set_Mkr_Freq(Freq-ChSpace,2)                   # Adj- Freq
        self.Set_Mkr_Band(ChBW,2)                           # Adj- RFBW
        self.Set_Mkr_Freq(Freq+ChSpace,3)                   # Adj+ Freq
        self.Set_Mkr_Band(ChBW,3)                           # Adj+ RFB
        self.Set_SweepCont(0)

    def Set_IQ_Adv_FFTLenth(self, dLength):
        self.write(f'IQ:FFT:LENG {dLength}')    

    def Set_IQ_Adv_Mode(self):
        self.write("IQ:BAND:MODE FFT")

    def Set_IQ_Adv_TransAlgo(self, sInput):
        # AVER SING
        self.write(f"IQ:FFT:ALG {sInput}")

    def Set_IQ_Adv_Window(self, sInput):
        # BLAC FLAT GAUS RECT P5
        self.write(f'IQ:FFT:WIND:TYPE {sInput}')

    def Set_IQ_Adv_WindowLenth(self, dLength):
        self.write("IQ:FFT:WIND:LENG 16384")

    def Set_IQ_BW(self,fFreq):
        # IQ_BW = SamplingRate * 0.8
        self.write('TRAC:IQ:BWID %f'%fFreq)        #Analysis BW

    def Set_IQ_RecLength(self,iLen):
        self.query('TRAC:IQ:RLEN %d'%iLen)          #Record(Samples) Length
        
    def Set_IQ_Samples(self,iNum):
        # Samples = MeasTime * SamplingRate
        self.write('TRAC:IQ:RLEN %d'%iNum)         #Samples

    def Set_IQ_SamplingRate(self,fFreq):
        # SamplingRate = IQ_BW / 0.8
        self.write('TRAC:IQ:SRAT %f'%fFreq)        #Sampling Rate

    def Set_IQ_SpectrumWindow(self):
        if 0:
            windList = self.query('LAY:CAT:WIND?').split(',')
            numWind = len(windList)
            if numWind > 2:
                for indx in range(2,int(numWind/2)+1):
                    self.write(f'LAY:REM "{indx}"')
            self.write(":LAY:ADD:WIND? '1',RIGH,FREQ")
            self.write(":DISP:WIND2:SUBW:SEL")
        else:
            self.write("LAY:REPL '1',Freq")

    def Set_IQ_Time(self,fSwpTime):
        self.Set_SweepTime(fSwpTime)

    def Set_IQ_WideBandMax(self,fFreq):
        """Hz"""
        self.write('TRAC:IQ:WBAN:STAT ON')                  #Wideband reduction activated
        self.write('TRAC:IQ:WBAN:MBW %f; *WAI'%fFreq)

    def Set_In_HPFilter(self,sState):                       #Filter for 1-3GHz meas
        """0 1 ON OFF"""
        self.write('INP:FILT:HPASs:STATe %s'%sState)

    def Set_In_YIG(self,sState):
        """0 1 ON OFF"""
        self.write('INP:FILT:YIG:STATe %s'%sState)

    def Set_InitImm(self):
        self.query('INIT:IMM;*OPC?')
            
    def Set_Input(self,sType):
        """ RF|AIQ|DIQ|FILE """
        self.write('INP:SEL %s'%sType)

    #####################################################################
    ### FSW marker
    #####################################################################
    def Set_Mkr_AllOff(self,iWind=1):
        self.write(':CALC%d:MARK:AOFF'%(iWind))

    def Set_Mkr_Band(self,fFreq,iNum=1,iWind=1):
        self.write(f':CALC{iWind}:MARK{iNum}:FUNC:BPOW:STAT ON')
        self.write(f':CALC{iWind}:MARK{iNum}:FUNC:BPOW:SPAN {fFreq}')

    def Set_Mkr_BandDelta(self,fFreq,iNum=1,iWind=1):
        self.write(f':CALC{iWind}:DELT{iNum}:STAT ON')
        self.write(f':CALC{iWind}:DELT{iNum}:FUNC:BPOW:STAT ON')
        self.write(f':CALC{iWind}:DELT{iNum}:FUNC:BPOW:SPAN {fFreq}')
        self.write(f':CALC{iWind}:DELT{iNum}:FUNC:BPOW:MODE RPOW')

    def Set_Mkr_BandSetRef(self):
        self.Set_AttnAuto()
        self.Set_SweepCont(0)
        self.Set_InitImm()                                   # Take Sweep
        ChPwr = self.Get_Mkr_Band(1)[1]
        self.Set_RefLevel(ChPwr + 5)
        if ChPwr > -24:         #FSVA:-24
            self.Set_Preamp(0)
        else:
            self.Set_Preamp(1)
            self.write('INP:GAIN:VAL 15')

    def Set_Mkr_Freq(self,fFreq,iNum=1,iWind=1):
        self.write(':CALC%d:MARK%d:X %fHz'%(iWind,iNum,fFreq))

    def Set_Mkr_Next(self,iNum=1,iWind=1):
        self.write(':CALC%d:MARK%d:MAX:NEXT'%(iWind,iNum))

    def Set_Mkr_On(self,iNum,iWind=1):
        self.write(':CALC%d:MARK%d ON'%(iWind,iNum))

    def Set_Mkr_Peak(self,iNum=1,iWind=1):
        self.write(':CALC%d:MARK%d:MAX:PEAK'%(iWind,iNum))

    def Set_Mkr_Time(self,fSec,iNum=1):
        self.write(':CALC1:MARK%d:X %fS'%(iNum,fSec))

    def Set_NoiseCorr(self,state):
        """0 1 ON OFF"""
        self.write(f':SENS:POW:NCOR {state}')

    def Set_Param_Couple_All(self):
        self.write("INST:COUP:CENT ALL")
        self.write("INST:COUP:RLEV ALL")
        self.write("INST:COUP:ATTEN ALL")
        self.write("INST:COUP:GAIN ALL")
        # self.query(":INST:COUP:USER1:NEW? 'Level','All Windows','Reference Level','LTE','All Windows','Reference Level',BID,ON")
        # self.query(":INST:COUP:USER2:NEW? 'Level','All Windows','Attenuation','LTE','All Windows','Attenuation',BID,ON")
        # self.query(":INST:COUP:USER3:NEW? 'Level','All Windows','Center Frequency','LTE','All Windows','Center Frequency',BID,ON")
        # self.query(":INST:COUP:USER4:NEW? 'Level','All Windows','Preamplifier','LTE','All Windows','Preamplifier',BID,ON")

        # self.query(":INST:COUP:USER1:NEW? 'Level','All Windows','Reference Level','IQACP','All Windows','Reference Level',BID,ON")
        # self.query(":INST:COUP:USER2:NEW? 'Level','All Windows','Attenuation','IQACP','All Windows','Attenuation',BID,ON")
        # self.query(":INST:COUP:USER3:NEW? 'Level','All Windows','Center Frequency','IQACP','All Windows','Center Frequency',BID,ON")
        # self.query(":INST:COUP:USER4:NEW? 'Level','All Windows','Preamplifier','IQACP','All Windows','Preamplifier',BID,ON")

    def Set_Preamp(self,sState):
        """0 1 ON OFF"""
        self.write('INP:GAIN:STAT %s;*WAI'%sState)

    def Set_PreampToggle(self,ChPwr,fToggle):
        if ChPwr < fToggle:     #FSVA:-23  FSW:-27
            self.Set_Preamp('ON')
        else:
            self.Set_Preamp('OFF')

    def Set_RefLevel(self,fReflevel):
        self.write('DISP:WIND:TRAC:Y:SCAL:RLEV %fdBm'%fReflevel)

    def Set_ResBW(self,fFreq):
        if fFreq == 0:
            self.write(':SENS:BAND:RES:AUTO ON')
        else:
            self.write(':SENS:BAND:RES %f'%fFreq)

    def Set_SamplingRate(self,fFreq):
        self.write('TRAC:IQ:SRAT %f'%fFreq)

    def Set_Savestate(self,sFilename):
        self.write(f':MMEM:STOR:STAT 1,"C:\\R_S\\Instr\\user\\{sFilename}"')

    def Set_Span(self,fFreq):
        self.write('SENS:FREQ:SPAN %f'%fFreq)
        
    def Set_SweepTime(self,fSwpTime):
        """Auto if fSwpTime == 0"""
        if fSwpTime == 0:
            self.write(':SENS:SWE:TIME:AUTO ON')
        else:
            self.write('SENS:SWE:TIME %f'%fSwpTime)             #Sweep/Capture Time

    def Set_SweepType(self,sType):
        #AUTO | SWE | FFT
        self.write(f':SENS:SWE:TYPE {sType}')
       
    def Set_SweepOpt(self,sOpt):
        #AUTO | SPEed | DYN
        self.write(f':SENS:SWE:OPT {sOpt}')
       
    def Set_SweepCont(self,iON):
        """0 | 1 """
        if iON == 1:
            self.write('INIT:CONT ON')                      #Continuous Sweep
        else:
            self.write('INIT:CONT OFF')                     #Single Sweep

    def Set_SweepPoints(self,iNum):
        self.write(':SENS:SWE:POIN %f'%iNum)                #Number of trace points

    def Set_Trace_Avg(self,sType,trace=1):
        """LIN VID POW"""
        self.Set_Trace_Mode('AVER',trace)
        self.Set_Trace_Detector('AVER')
        self.Set_Trace_AvgType(sType)

    def Set_Trace_AvgCount(self,iAvg,trace=1):
        self.write('SENS:SWE:COUN %d'%(iAvg))

    def Set_Trace_AvgOff(self,trace=1):
        self.write('DISP:TRAC%d:MODE WRIT'%(trace))

    def Set_Trace_AvgType(self,sType):
        """LIN VID POW"""
        self.write(f'SENS:AVER:TYPE {sType}')

    def Set_Trace_Detector(self,sDetect,iWind=1):
        """APE; NEG; POS; QPE; SAMP; RMS; AVER; CAV; CRMS"""
        self.write('SENS:WIND%d:DET %s'%(iWind,sDetect))

    def Set_Trace_Mode(self,sMode,trace=1):
        """WRIT AVER MAXH MINH VIEW BLAN"""
        self.write(f'DISP:TRAC{trace}:MODE {sMode}')

    ####################################################################
    ### FSW Trigger
    #####################################################################
    def Set_Trig1_Source(self,sDetect):
        """IMM; EXT; EXT2; EXT3; RFP; IFP; TIME; VID; PSEN""" 
        self.write('TRIG:SEQ:SOUR %s'%sDetect)
    
    def Set_Trig2_Dir(self,sDir):
        if (sDir == 'OUT'):
            self.write('OUTP:TRIG2:DIR OUTP')
        else:
            self.write('OUTP:TRIG2:DIR INP')
        
    def Set_Trig2_OutType(self,sDir):
        #DEV : Device
        #TARM: Trigger Armed
        #UDEF: User Defined
        self.write('OUTP:TRIG2:OTYP %s')

    def Set_VidBW(self,fFreq):
        if fFreq == 0:
            self.write(':SENS:BAND:VID:AUTO ON')
        else:
            self.write(':SENS:BAND:VID %f'%fFreq)

    def Set_YIG(self,sState):
        """ON|OFF|1|0"""
        self.write('INP:FILT:YIG:STAT %s;*WAI'%sState)


#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    import timeit
    FSW = VSA().jav_Open("192.168.1.109")
    print(FSW.Get_ChannelName())
    FSW.jav_ClrErr()
    del FSW
