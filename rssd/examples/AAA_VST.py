"""RSSD Frequency Sweep VSA & VSG"""
from rssd.VSA           import VSA
from rssd.VSG           import VSG
from rssd.FileIO        import FileIO

freqOffset = 60e6
smwPwr      = -10
OFile = FileIO().makeFile(__file__)                 # Create Output File
SMW = VSG().jav_Open('169.254.58.114',OFile)        # Create Generator Object
FSW = VSA().jav_Open('169.254.58.109',OFile)        # Create Analyzer Object

OFile.write('SMWFreq,FreqOffset,SMWPwr,MkrBand,MkrCenter,MkrOffset,MkrDelta,SMWOff')
Freqs = range(int(36e9), int(50e9), int(100e6))     # Frequency List
SMW.Set_RFPwr(smwPwr)
SMW.Set_IQMod(1)
FSW.Set_Span(200e6)
FSW.Set_SweepTime(0.500)
FSW.Set_Trace_Detector('RMS')
FSW.Set_Mkr_Band(100e6)
for frq in Freqs:
    SMW.Set_RFState(1)
    SMW.Set_Freq(frq)
    FSW.Set_SweepCont(0)
    FSW.Set_Freq(frq)
    ## SMW on Power
    FSW.Set_Autolevel()
    FSW.Set_InitImm()
    FSW.Set_Mkr_Freq(frq)
    MkrCenter = FSW.Get_Mkr_Y()
    MkrBandPr = FSW.Get_Mkr_Band()
    FSW.Set_Mkr_Freq(frq + freqOffset)
    MkrOffset = FSW.Get_Mkr_Y()
    ## SMW off Power
    SMW.Set_RFState(0)
    FSW.Set_InitImm()
    MkrOff = FSW.Get_Mkr_Y()

    OFile.write(f'{frq},{freqOffset},{smwPwr},{MkrBandPr[1]},{MkrCenter},{MkrOffset},{MkrCenter-MkrOffset},{MkrOff}')

SMW.jav_Close()
FSW.jav_Close()
