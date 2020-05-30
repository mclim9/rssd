########################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Purpose: CMP200A Example
### Author:  mclim
### Date:    2019.09.09
########################################################################
### User Entry
########################################################################
CMP_IP      = '192.168.1.160'                   #IP Address
SMW_IP      = '192.168.1.114'                   #IP Address
FreqArry    = [24e9, 26e9, 28e9, 31e9, 37.50e9, 38.5e9, 44.0e9]
pwrArry     = range(-50,8,2)                    #Power Array
# modArry     = ['QAM64']                       #QPSK; QAM16; QAM64; QAM256;
waveparam   = [[100,120,66,'QAM64']]            #ChBW, SubSp, RB
numMeas     = 1
########################################################################
### Code Overhead: Import and create objects
########################################################################
import math
from datetime               import datetime     #pylint: disable=E0611,E0401
from rssd.RCT.NR5G_K        import RCT          #pylint: disable=E0611,E0401
from rssd.VSG.NR5G_K144     import VSG          #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO       #pylint: disable=E0611,E0401
OFile = FileIO().makeFile(__file__)

class vari:
    def __init__(self):
        self.NR_ChBW    = 0
        self.NR_SubSp   = 0
        self.NR_RB      = 0
        self.NR_Mod     = ''
        self.NR_TF      = "off"
NR5G = vari()

########################################################################
### Code Start
########################################################################
CMP = RCT()
SMW = VSG()
CMP.jav_Open(CMP_IP,OFile)
SMW.jav_Open(SMW_IP,OFile)

CMP.query('*IDN?')
CMP.write('ROUT:NRMM:MEAS:SCEN:SAL RF1C,RX1')
CMP.Set_5GNR_Freq(28000)
CMP.Set_5GNR_ExpPwr(0)
CMP.Set_5GNR_UserMargin(11.5)
CMP.Set_5GNR_ExtAttn(0)
CMP.Set_5GNR_MixerOff(0)
CMP.Set_5GNR_BWP_SubSpace(120)
CMP.Set_5GNR_ChannelBW(100)
CMP.Set_5GNR_PhaseComp('OFF',2.8e10)
CMP.Set_5GNR_Periodicity(1)
CMP.write('CONF:NRMM:MEAS:ULDL:PATT S120K,0,0,8,0')
CMP.write('CONF:NRMM:MEAS:PLC 3')
CMP.write('CONF:NRMM:MEAS:BWP BWP0,S120,NORM,MAX,0')
CMP.write('CONF:NRMM:MEAS:BWP:PUSC:DFTP BWP0,OFF')
CMP.write('CONF:NRMM:MEAS:ALL:PUSC A,14,0,66,0,Q64')
CMP.write('CONF:NRMM:MEAS:TAP 3')
CMP.write('CONF:NRMM:MEAS:BWP:PUSC:DMTA BWP0,1,0,1')
CMP.write('CONF:NRMM:MEAS:CC:ALL:PUSC:ADD 1,1,0.0,0')
CMP.write('TRIG:NRMM:MEAS:MEV:SOUR "Free Run (Fast Sync)"')
CMP.write('CONF:NRMM:MEAS:MEV:RES:ALL ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON,ON')
CMP.write('CONF:NRMM:MEAS:MEV:REP SING')
CMP.write('CONF:NRMM:MEAS:MEV:SCON NONE')
CMP.write('CONF:NRMM:MEAS:MEV:MMOD NORM')
CMP.write('CONF:NRMM:MEAS:MEV:MOEX OFF')
CMP.write('CONF:NRMM:MEAS:MEV:SCO:POW 1')
CMP.write('CONF:NRMM:MEAS:MEV:SCO:MOD 1')
CMP.write('CONF:NRMM:MEAS:MEV:SCO:SPEC:SEM 1')
CMP.write('CONF:NRMM:MEAS:MEV:SCO:SPEC:ACLR 1')

##########################################################
### Measure Time
##########################################################
#sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
Header = 'Iter,Model,Freq,EVM,TxPwr,PeakPwr,FreqErr,EVMdB,ChBW,UL-TP,SubSp,Mod,SMWPwr,ExpPwr,UserMargin,ExtAttn,MixerLevel,StepTime'
OFile.write(Header)

for i in range(numMeas):                                            #Loop: Repeatability
    for param in waveparam:                                         #Loop: Waveform Parameters
        NR5G.NR_ChBW    = param[0]
        NR5G.NR_SubSp   = param[1]
        NR5G.NR_RB      = param[2]
        NR5G.NR_Mod     = param[3]
        CMP.Init_5GNR()
        for freq  in FreqArry:                                      #Loop: Frequency
            print(f'Freq:{freq:.0f} RFBW:{NR5G.NR_ChBW} SubC:{NR5G.NR_SubSp} Mod:{NR5G.NR_Mod}')
            SMW.Set_Freq(freq)
            CMP.Set_5GNR_Freq(freq/1e6)
            print(Header)
            for pwr in pwrArry:                                     #Loop: Power
                SMW.Set_RFPwr(pwr)
                CMP.Set_5GNR_ExpPwr(pwr)
                tick = datetime.now()                               #Tick
                evm     = CMP.Get_5GNR_EVM()
                attn    = CMP.Get_AmpSettings()
                try:
                    evmdB   = 20 * math.log10(float(evm[0])/100)
                except:
                    evmdB   = -9999
                s = datetime.now() - tick                          #Total test time
                OutStr = f'{i},{CMP.Model},{freq:.0f},{evm},{evmdB:.3f},{NR5G.NR_ChBW},{NR5G.NR_TF},{NR5G.NR_SubSp},{NR5G.NR_Mod},{pwr:3d},{attn},{s.seconds:3d}.{s.microseconds:06d}'
                OFile.write (OutStr)
            #end PwrLoop
        #end FreqLoop
    #end ParamLoop
#end repeatabilityLoop
CMP.jav_ClrErr()                                                    #Clear Errors
