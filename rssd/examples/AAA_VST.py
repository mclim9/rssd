"""RSSD Demo VSA & VSG"""
from rssd.VSA           import VSA
from rssd.VSG           import VSG
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)                 #Create Output File
SMW = VSG().jav_Open('192.168.1.114',OFile)         #Create Generator Object
FSW = VSA().jav_Open('192.168.1.109',OFile)         #Create Analyzer Object

OFile.write('Iter,CmdTime,Response')                #Data header
Freqs = [1e9, 2e9, 3e9, 4e9, 5e9]                   #Frequency List
for frq in Freqs:
    SMW.Set_Freq(frq)
    FSW.Set_Freq(frq)
    OFile.write(f'{frq}')

SMW.jav_Close()
FSW.jav_Close()
