# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Signal Generator Common Functions
### Author : Martin C Lim
### Date   : 2018.02.01
### Requird: python -m pip install pyvisa
#####################################################################
from rssd.yaVISA    import jaVisa        #pylint: disable=E0611,E0401
from time           import sleep

class VSG(jaVisa):
    """ Rohde & Schwarz Vector Signal Generator Object """
    def __init__(self):
        super(VSG,self).__init__()     #Python2/3
        self.Model = "SMW"

    #####################################################################
     ### SMW Get 
    #####################################################################
    def Get_ArbClockFreq(self):
        SCPI = self.queryFloat('SOUR:BB:ARB:CLOC?')
        return SCPI

    def Get_ArbName(self):
        WvName = self.query('BB:ARB:WAV:SEL?')
        return WvName

    def Get_ArbTime(self):
        Fs = self.Get_ArbClockFreq()
        Points = self.query('BB:ARB:WAV:POIN?').strip()
        WvTime = int(Points)/int(Fs)
        return WvTime

    def Get_ArbInfo(self):
        ClkFreq = self.Get_ArbClockFreq()
        ArbName = self.Get_ArbName()
        ArbTime = self.Get_ArbTime()
        return f'{ClkFreq},{ArbName},{ArbTime}'

    def Get_CrestFactor(self):
        PEP = self.Get_PowerPEP()
        RMS = self.Get_PowerRMS()
        return (PEP - RMS)

    def Get_Freq(self):
        rdStr = self.queryFloat(':SOUR1:FREQ:CW?')     #RF Freq
        return rdStr

    def Get_ListMode_IndexCurr(self):
        rdInt = self.queryInt('SOUR1:LIST:IND?')
        return rdInt

    def Get_ListMode_IndexStop(self):
        rdInt = self.queryInt('SOUR1:LIST:IND:STOP?')
        return rdInt

    def Get_NRPPower(self,NRP=2):
        self.write(':INIT%d:POW:CONT 1'%(NRP))
        self.write('SENS%d:UNIT DBM'%(NRP))
        self.write('SENS%d:TYPE?'%(NRP))
        SCPI = self.queryFloat(':READ%d:POW?'%(NRP))
        return SCPI

    def Get_OS_Dir(self):
        rdStr = self.query(f'MMEM:CDIR?')
        return rdStr

    def Get_OS_FileList(self,filter=''):
        """Return list of filenames in sDir"""
        rdStr   = self.query('MMEM:CATalog?').split('","')
        rdStr   = rdStr[2:]                                   #Filter out . and ..
        outList = []
        for i, file in enumerate(rdStr):
            rdStr[i] = rdStr[i].split(',')
            if (rdStr[i][0].find(filter) > -1):
                outList.append(rdStr[i][0])
        return outList


    def Get_PowerPEP(self,RF=1):
        SCPI = self.queryFloat('SOUR%d:POW:PEP?'%RF)
        return SCPI

    def Get_PowerRMS(self,RF=1):
        SCPI = self.queryFloat('SOUR%d:POW?'%RF)
        return SCPI

    def Get_PowerInfo(self):
        PEP = self.Get_PowerPEP()
        RMS = self.Get_PowerRMS()
        CRS = PEP - RMS
        return f'{PEP},{RMS},{CRS}'

    def Get_SysC_All(self):
        BBSour  = self.Get_SysC_BBSource()
        Fading  = self.Get_SysC_Fading()
        Mode    = self.Get_SysC_Mode()
        rdStr = f'{Mode},{Fading},{BBSour}'
        print(rdStr)
        return rdStr

    def Get_SysC_BBSource(self):
        rdStr = self.query('SCON:BAS:SOUR?')
        return rdStr

    def Get_SysC_Fading(self):
        rdStr = self.query('SCON:FAD?')
        return rdStr

    def Get_SysC_Mode(self):
        rdStr = self.query('SCON:MODE?')
        return rdStr

    #####################################################################
    ### SMW INIT
    #####################################################################
    def Init_Wideband(self):
        self.write('SOUR:POW:ATT:DIG 3')            #Set Digital Attenuation
        self.write('POW:ALC:STATE AUTO')            #Turn ALC ON|OFF|OFFT|AUTO|
        self.write('SOUR:POW:ALC:DAMP AUTO')      #Turn Driver AMP ON|OFF|AUTO
        self.write('SOUR:BB:IQG DB8')                #Baseband IQ gain
        
        ## Not so critical
        self.write('SOUR:AWGN:STAT 0')              #Turn AWGN off (default)
        self.write('BBIN:STAT OFF')                  #Turn BB Input off(default)

    #####################################################################
    ### SMW Settting Methods
    #####################################################################
    # def Set_IQ_Data(self):
    #     IData = [0.1,0.2,0.3]
    #     QData = [0.4,0.5,0.6]

    #     ### ASCII
    #     scpi  = ':MMEM:DATA:UNPR "NVWFM://var//user//wave.wv",#'        # Ascii Cmd
    #     iqsize= str(len(IData)*4)                                       # Calculate bytes of IQ data
    #     scpi  = scpi + str(len(iqsize)) + iqsize                        # Calculate length of iqsize string
    #     ### Binary
    #     iqdata= np.vstack((IData,QData)).reshape((-1,),order='F')       # Combine I&Q Data
    #     bits  = np.array(iqdata*32767, dtype='>i2')                     # Convert to big-endian 2byte int 
    #     ### ASCII + Binary
    #     cmd   = bytes(scpi, 'utf-8') + bits.tostring()                  # Add ASCII + Bin
    #     self.K2.write_raw(cmd)
    #     self.write('SOUR1:BB:ARB:WAV:CLOC "/var/user/wave.wv",1.1E6')    # Set Fs/Clk Rate
    #     self.write('BB:ARB:WAV:SEL "/var/user/wave.wv"')                 # Select Arb File

    def Set_ALC_RFDriveAmp(self,sState):
        """input: ON, OFF, AUTO, FIX """
        self.query('SOUR:POW:ALC:DAMP %s;*OPC?'%sState)

    def Set_ArbClockFreq(self,fFreq,RF=1):
        self.write('SOUR%d:BB:ARB:CLOC %f'%(RF,fFreq))

    def Set_ArbNextSeg(self,num):
        self.query('BB:ARB:WSEG:NEXT %d;*OPC?'%(num))

    def Set_ArbSeg(self,Seg):
         self.write('SOUR:BB:ARB:WSEG:NEXT %d'%Seg)
        #  self.write('SOUR:BB:ARB:WSEG:NEXT:EXEC')

    def Set_ArbState(self,sState):
        self.query(':SOUR:BB:ARB:STATE %s;*OPC?'%sState)

    def Set_ArbWv(self,InWv):
         self.query('BB:ARB:WAV:SEL "%s"; *OPC?'%InWv)

    def Set_BBState(self,sState):
        """'ON' 'OFF' 1 or 0"""
        if (sState == "ON") or (sState == 1):
            self.query(':SOUR1:BB:ARB:STAT 1;*OPC?')
        elif (sState == "OFF") or (sState == 0):
            self.query(':SOUR1:BB:ARB:STAT 0;*OPC?')

    def Set_Freq(self,freq):
        """Unit: Hz"""
        self.write(':SOUR1:FREQ:CW %f'%freq)     #RF Freq

    def Set_IQMod(self,sState):
        """input: ON, OFF """
        if (sState == 1) or (sState == 'ON'):
            self.query('SOUR:IQ:STAT ON;*OPC?')
        else:
            self.query('SOUR:IQ:STAT OFF;*OPC?')

    def Set_ListMode_Dwell(self, sec):
        self.write(f'SOUR1:LIST:DWEL {sec}')

    def Set_ListMode_File(self,sFile):
        if sFile.find('.lsw') == -1:
            sFile = sFile + '.lsw'
        self.write(f'SOUR1:LIST:SEL "/var/user/{sFile}"')

    def Set_ListMode(self,sState):
        """input: LIST CW"""
        self.query(f':SOUR1:FREQ:MODE {sState};*OPC?')

    def Set_ListMode_TrigExecute(self):
        self.query(':SOUR1:LIST:TRIG:EXEC;*OPC?')

    def Set_ListMode_TrigSource(self,sSource):
        """SING AUTO STEP ESTEP ESING"""
        # USER5 Valid Signal A
        # USER6 Valid SIgnal B
        
        if 'AUTO' in sSource:
            self.write(f'SOUR1:LIST:MODE AUTO')
            self.write(f'SOUR1:LIST:TRIG:SOUR AUTO')
        elif 'SING' in sSource:
            self.write(f'SOUR1:LIST:MODE AUTO')
            self.write(f'SOUR1:LIST:TRIG:SOUR SING')
        elif 'STEP' in sSource:
            self.write(f'SOUR1:LIST:MODE STEP')
            self.write(f'SOUR1:LIST:TRIG:SOUR SING')
        elif 'ESING' in sSource:
            self.write(f'SOUR1:LIST:MODE AUTO')
            self.write(f'SOUR1:LIST:TRIG:SOUR EXT')
        elif 'ESTEP' in sSource:
            self.write(f'SOUR1:LIST:MODE STEP')
            self.write(f'SOUR1:LIST:TRIG:SOUR EXT')

    def Set_ListMode_TrigWait(self):
        indx = 0
        stop = self.Get_ListMode_IndexStop()
        while indx != stop:
            sleep(0.1)
            indx = self.Get_ListMode_IndexCurr()

    def Set_ListMode_RMode(self, sMode):
        """RunMode: LIVE LEARned """
        self.write(f'SOUR:LIST:RMOD {sMode}')

    def Set_OS_Dir(self,sDir):
        self.write(f'MMEMory:CDIRectory "/var/user/{sDir}"')

    def Set_PhaseDelta(self,fPhase):
        self.write(':SOUR1:PHASE %d'%(fPhase))

    def Set_RFPwr(self,fPow):
        self.write('SOUR:POW %f'%fPow)

    def Set_RFState(self,sState):
        ''' 0 1 '''
        self.query('OUTP %s;*OPC?'%sState)

    def Set_Setting(self,sSettingFile):
        """*.savrcltxt SettingFile"""
        self.jav_OPC_Wait(f'SYST:RCL "/var/user/{sSettingFile}"')

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    # this won't be run when imported
    SMW = VSG().jav_Open("192.168.1.114")
    getVal = SMW.Get_OS_FileList('savrcltxt')
    SMW.Set_Setting('test.savrcltxt')
