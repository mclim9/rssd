###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Measure VSA Noise Floor
### Creatd : mclim, 2019.06.11
###############################################################################
### User Entry
###############################################################################
instru_ip   = '192.168.1.109'
freq        = 1.950    #GHz
###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.VSA.Common        import VSA
from rssd.FileIO            import FileIO

OFile = FileIO().makeFile(__file__)
FSW   = VSA().jav_Open(instru_ip,OFile)                  #Create Object

###############################################################################
### Code Start
###############################################################################
OFile.write('Freq,ChPwr-dBm,2nd-dbc,3rd-dbc')

FSW.Init_Harm()
FSW.Set_Freq(freq * 1e9)
FSW.Set_Harm_num(3)
FSW.Set_Trace_Detector('RMS')
FSW.Set_Harm_adjust()
    # FSW.Set_RefLevel(-100)
    # FSW.Set_ResBW(100)
data = FSW.Get_Harm()
OutStr = f'{freq},{data[0]},{data[1]},{data[2]}'
OFile.write (OutStr)

###############################################################################
### Cleanup Automation
###############################################################################
FSW.jav_Close()
