#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: Vector Network Analyzer Common Functions
### Author : Martin C Lim
### Date   : 2019.02.14
### Requird: python -m pip install rssd
###
#####################################################################
from rssd.yaVISA import jaVisa            # pylint: disable=E0611,E0401

class VNA(jaVisa):
    def __init__(self):
        super(VNA,self).__init__()     #Python2/3
        self.Model = "xxx"
    
    #####################################################################
    ### VNA GET Functions Alphabetical
    #####################################################################
    def Get_Trace_Names(self,dChan=1):
        rdStr = self.query(":CALC%d:PAR:CAT?"%(dChan))
        return rdStr

    def Get_Pwrcal_State(self):
        rdStr = self.query(f":SOUR:POW:CORR:STAT?")
        return rdStr

    def Get_Pwrcal_Rx_State(self):
        rdStr = self.query(f":SENS:CORR:STAT?")
        return rdStr

    def Save_Cal(self, sFName, dChan=1):
        #Save calibration to cal manager.
        if not sFName.lower().endswith(".cal"):
            sFName += ".cal"
        self.write(f":MMEM:STOR:CORR {dChan},'{sFName}'")

    def Save_Screen(self,sFName):
        self.write('HCOP:DEV:LANG BMP')
        self.write("MMEM:NAME '%s.BMP'"%(sFName))
        self.write('HCOP:DEST "MMEM"; :HCOP')

    def Save_State(self,sFName):
        self.write("MMEM:STOR:STAT 1,'%s'"%(sFName))

    def Save_Trace_SxP(self,sFName,dChan=1):                        #MMM
        self.write("MMEM:STOR:TRAC:CHAN %d,'%s.s2p'"%(dChan,sFName))
        #self.write(":MMEM:STOR:TRAC:PORT %d,'%s.s2p',COMP,1,2"%(dChan,sFName))

    def Save_Trace_CSV(self,sFName,dChan=1):
        self.write("MMEM:STOR:TRAC:CHAN %d,'%s.csv'"%(dChan,sFName))

    #####################################################################
    ### VNA SET Functions Alphabetical
    #####################################################################
    # def Set_Cal_Group(self,sName,dChan=1):                          #MMM
    #     #sName should end in '.cal'
    #     if not sName.lower().endswith(".cal"):
    #         sName += ".cal"
    #     self.write(":MMEM:LOAD:CORR:RES %d,%s"%(dChan,sName))       #Resolve Cal Group
    #     self.write(":MMEM:LOAD:CORR %s"%(sName))                    #Load cal group.

    def Set_FreqStart(self,fFreq,dChan=1):
        self.write(":SENS%d:FREQ:STAR %f"%(dChan,fFreq))

    def Set_FreqStop(self,fFreq,dChan=1):
        self.write(":SENS%d:FREQ:STOP %f"%(dChan,fFreq))            #RF Freq

    def Set_IFBW(self,fFreq,dChan=1):
        self.write("SENS%d:BAND %f"%(dChan,fFreq))
        
    def Set_InitImm(self):                                        
        self.query("INIT:IMM;*OPC?")
          
    def Set_PowerStart(self,fPwr,dChan=1):
        self.write(":SOUR%d:POW:STAR %f dBm"%(dChan,fPwr))

    def Set_PowerStop(self,fPwr,dChan=1):
        self.write(":SOUR%d:POW:STOP %f dBm"%(dChan,fPwr))

    def Set_Pwrcal_Init(self):
        self.write(f":SOUR:POW:CORR:COLL:FLAT ON")      #Flatness Cal
        self.write(f":SOUR:POW:CORR:COLL:RREC ON")      #Ref Rx Cal
        self.write(f":SOUR:POW:CORR:COLL:VER ON")       #Verification Sweep
        self.write(f":SOUR:POW:CORR:COLL:METH PMON")    #PMON | RFAF | RRON

    def Set_Pwrcal_NumReading(self,iNum,chan=1):
        self.write(f":SOUR{chan}:POW:CORR:NRE {iNum}")

    def Set_Pwrcal_Measure(self,iPort,dChan=1):
        self.write(f":SOUR{dChan}:POW:CORR:ACQ PORT,{iPort}")
    
    def Set_Pwrcal_Tolerance(self,fTol,dChan=1):
        self.write(f":SOUR:POW:CORR:COLL:AVER:NTOL {fTol}")
    
    def Set_Pwrcal_Rx(self,Source,Port,dChan=1):
        # CORR:POW:ACQ <What to Cal> <Port>,<SourceTYpe>,<Port#>,<AWAV/NOM>
        self.write(f":CORR:POW:ACQ BWAV,{Port},PORT,{Source},AWAV")
        self.query('CORR:POW:AWAV?')
    
    def Set_SweepCont(self,iON):
        if iON == 1:
            self.write("INIT:CONT ON")                          #Continuous Sweep
        else:
            self.write("INIT:CONT OFF")                         #Single Sweep

    def Set_SweepPoints(self,dPoints,dChan=1):
        self.write(":SENS%d:SWE:POIN %d"%(dChan,dPoints))  #RF Freq

    def Set_SweepTime(self,fSwpTime,dChan=1):
        if fSwpTime == 0:
            self.write("SENS%d:SWE:TIME:AUTO ON"%(dChan))  #Auto        
        else:
            self.write("SENS%d:SWE:TIME %f"%(dChan,fSwpTime))  #Sweep/Capture Time

    def Set_Trace_Avg(self,state,dChan=1):
        if state == 1:
            self.write("SENS%d:AVER:STAT ON"%(dChan))
        else:
            self.write("SENS%d:AVER:STAT OFF"%(dChan))

    def Set_Trace_AvgCount(self,iAvg,dChan=1):
        self.write("SENS%d:AVER:COUN %d"%(dChan,iAvg))

    def Set_Trace_DelAll(self):
        self.write("CALC:PAR:DEL:ALL")

    def Set_Trace_MeasAdd(self,sMeas,dChan=1):
        # S11/S21/S12/S22 ..... Sxxyy
        # Y11/Y21/Y12/Y22 ..... Yxxyy
        # A1D2/A1D4/A2D1  ..... A<port>G<port>
        # B1D2/B1D4/B2D1  ..... B<port>G<port>
        # IP3UI/IP3UO      ..... IP<order:3|5|7|9><side:U|L><DUT:I|O>
        self.write(f"CALC{dChan}:PAR:SDEF '{sMeas}','{sMeas}'")     #<TrcName>,<Measurement>
        self.write(f'DISP:WIND1:TRAC:EFE "{sMeas}"')                #Displays Trace

    def Set_Trace_MeasAdd_AWave(self,APort,GenPort,dChan=1):
        #Default: SAM; RMS; PEAK; AVG
        self.Set_Trace_MeasAdd(f'A{APort}D{GenPort}RMS')

    def Set_Trace_MeasAdd_BWave(self,BPort,GenPort,dChan=1):
        self.Set_Trace_MeasAdd(f'B{BPort}D{GenPort}RMS')

    def Set_Trace_MeasAdd_SParam(self,Port1,Port2,dChan=1):
        self.Set_Trace_MeasAdd(f'S{Port1}{Port2}')

    def Set_Trace_MeasAdd_PwrMtr(self,GenPort,dChan=1):
        self.Set_Trace_MeasAdd(f'Pmtr{1}D{GenPort}')

    # def Set_Trace_MeasAdd_IMD3(self,dChan=1):                         #mmm
    #     self.write("SENS%d:FREQ:IMOD:ORD3 ON"%(dChan))
    #     self.Set_Trace_MeasAdd("IP3UI")
    #     self.Set_Trace_MeasAdd("IP3LI")

    def Set_Trace_MeasDel(self,sTrcName,dChan=1):
        self.write("CALC%d:PAR:DEL '%s'"%(dChan,sTrcName))

    #####################################################################
    ### VNA TEST Functions
    #####################################################################
    def Test_PwrCal(self):
        self.Set_Pwrcal_Init()
        self.Set_Pwrcal_Tolerance(0.1)
        self.Set_Pwrcal_NumReading(10)
        self.Set_Pwrcal_Measure(2)                   #Take Power cal on Port2
        print(self.Get_Pwrcal_State())               #Power cal state 0:OFF  1:ON

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    # this won't be run when imported
    ZVA = VNA().jav_openvisa('TCPIP0::192.168.1.30::inst0')
    #ZVA.Test_PwrCal()
    print(ZVA.Get_Pwrcal_State())
    ZVA.jav_Close()
