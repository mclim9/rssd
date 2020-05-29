###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Vector Signal Explorer K96 Functions
### Author : Martin C Lim
### Date   : 2018.04.27
###############################################################################
import time            #EVM Wait
from rssd.VSE.Common import VSE

class VSE(VSE):
    """ Rohde & Schwarz VSE K96 Object """
    def __init__(self):
        super(VSE, self).__init__()
        self.Model = 'K96'

    ###########################################################################
    ### VSE General Settings
    ##########################################################################
    def Init_K96(self):
        self.Set_Channel('OFDMVSA')
        time.sleep(10)
        self.write("SENS:DEM:FSYN DATA")                # Pilot and Data Aided
        self.write("SENS:TRAC:TIME ON")                 # Timing tracking ON
        self.write("SENS:TRAC:LEV ON")                  # Leveltracking ON

    def Set_K96_BurstSearch(self,sState):
        self.write('DEM:FORM:BURS %s;*WAI'%sState)      #ON|OFF|1|0

    def Set_K96_File_Config(self,sFile):
        self.write("MMEM:LOAD:CFGF '%s';*WAI"%sFile)

    def Set_K96_FilterAdjustable(self,sState):
        self.write('INP:FILT:CHAN:STAT %s'%sState)      #ON|OFF|1|0

    def Set_K96_Frames(self,iNum):
        self.write('SENS:DEM:FORM:MAXF %d'%iNum)        #Number of frames to analyze

    def Set_K96_FSWIPAdd(self,sIP):                     #For FS-K96
        self.write('CONF:ADDR "TCPIP::%s"'%sIP)         #FSW IP Address

    def Set_K96_OFDMSymbols(self,iNum):
        self.write('SENS:DEM:FORM:NOFS %d'%iNum)        #FSW IP Address

    ###########################################################################
    ### Helper Functions
    ###########################################################################
    def K96_EVM_Wait(self):
        EVM = ''                                        #init EVM read value
        t0 = time.time()
        self.write('INIT:IMM')                          #Start Measurement
        while (EVM == ''):                              #Loop until EVM present
            delta = (time.time() - t0)
            try:
                EVM = self.Get_EVM()
            except:
                pass
            if delta > 10:                              #EVM_Wait Timeout
                break
        print("K96_EVM_Wait: %.3f sec"%(delta))
        self.Get_EVM()                                  #Flush buffer of NaN

    def K96_EVM_AutoCal(self):
        #######################################################################
        ### Code Settings
        #######################################################################
        debug=0
        Backoff = 0
        EVM_Wind = -0.1                                 #EVM can degrade by this amount.
                                                        #EVM Repeatability indicator
        #######################################################################
        ### Code Start
        #######################################################################
        if debug==1: print('    Autolvl EVM: ')
        self.Set_Autolevel("ON")
        EVM_Curr = self.Get_EVM()                       #Set initial RefLvl & Attn
        RefLvl = self.Get_RefLevel()
        MAttn  = self.Get_AttnMech()
        if debug==1: print("        Ref:%.2f MAttn:%.0f EVM:%.2f"%(RefLvl, MAttn, EVM_Curr))

        #######################################################################
        ### Attn Sweep
        #######################################################################
        if debug==1: print('    Attenu Swp: ')
        EVM_Prev = 1.00
        i=0
        self.Set_Autolevel("OFF")                       #Manually Set RefLvl & Attn
        while (i <= MAttn) & (i < 30):
            MechAttn = MAttn - i
            self.Set_AttnMech(MAttn - i)
            EVM_Curr = self.Get_EVM()
            if debug==1: print("        Ref:%.2f MAttn:%.0f EVM:%.2f"%(RefLvl, MechAttn, EVM_Curr))
            if EVM_Curr =='NAN':
                print("EVM NAN")
                break

            Diff = EVM_Prev - EVM_Curr                 #Positive = improvedEVM
            if (Diff > EVM_Wind):
                EVM_Prev = EVM_Curr
                i = i + 1
            else:
                if debug==1: print("        Break")
                i = i - 1                               #Previous value
                break
        MechAttn = MAttn - i + Backoff                  #MechAttn Used for next step
        if (MechAttn < 0):
            MechAttn= 0
        self.Set_AttnMech(MechAttn)

        #######################################################################
        ### Ref Sweep
        #######################################################################
        #print('    RefLvl Swp: ')
        EVM_Prev = 1.00
        i=0
        self.Set_Autolevel("OFF")                            #Manually Set RefLvl & Attn
        for x in range(0):
            self.Set_RefLevel(RefLvl - i)
            EVM_Curr = self.Get_EVM()
            if debug==1: print("        Ref:%.2f MAttn:%.0f EVM:%.2f"%(RefLvl-i, MechAttn, EVM_Curr))
            if EVM_Curr =='NAN':
                print("EVM NAN")
                break

            Diff = EVM_Prev - EVM_Curr                  #Positive = improvedEVM
            if (Diff > EVM_Wind):
                EVM_Prev = EVM_Curr
                i = i + 1
            else:
                i = i - 1                               #Previous value
                self.Set_RefLevel(RefLvl - i)
                break
        self.EVM_Wait()

###############################################################################
### Run if Main
###############################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    VSE = VSE()
    VSE.jav_Open("127.0.0.1")
    VSE.Set_DisplayUpdate('ON')
    VSE.Init_K96()
    #VSE.Get_EVM_Params()
    #VSE.Set_InitImm()
    VSE.jav_ClrErr()
