###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Measure VSA Noise Floor
### Creatd : mclim, 2018.05.24
###############################################################################
### User Entry
###############################################################################
instru_ip  = '192.168.1.108'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.FSW_Common        import VSA
from rssd.FileIO            import FileIO

OFile = FileIO().makeFile(__file__)
FSVA = VSA().jav_Open(instru_ip,OFile)                  #Create Object

###############################################################################
### Code Start
###############################################################################
OFile.write('Freq,LNA,NoiseCorr,MkrFreq,Noise,dBmHz')

FSVA.Set_SweepCont(0)
#FSVA.Set_SweepTime(100e-3)
FSVA.Set_Span(1e6)
FSVA.Set_RefLevel(-100)
FSVA.Set_Trace_Detector('RMS')
FSVA.Set_Trace_Avg('POW')
FSVA.Set_Trace_AvgCount(30)
FSVA.Set_AttnMech(0)
FSVA.Set_ResBW(100)
for freq in (1,3.6,6):
    FSVA.Set_Freq(freq * 1e9)
    for preamp in ('NoPA','LNA'):
        if 'LNA' in preamp:
            FSVA.write(':INP:GAIN:STAT ON')
            FSVA.write(':INP:GAIN:VAL 30')
        else:
            FSVA.write(':INP:GAIN:STAT OFF')
        for NC in ('OFF','ON'):
            FSVA.Set_NoiseCorr(NC)
            FSVA.jav_OPC_Wait('INIT:IMM')
            mkr = FSVA.Get_Mkr_Noise()
            OutStr = f'{freq},{preamp},{NC},{mkr[0]},{mkr[1]}'
            OFile.write (OutStr)

###############################################################################
### Cleanup Automation
###############################################################################
FSVA.jav_Close()
