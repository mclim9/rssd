###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Creatd : mclim, 2018.05.24
###############################################################################
### User Entry
###############################################################################
instru_ip  = '192.168.1.108'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.yaVISA_socket     import jaVisa
from rssd.FileIO            import FileIO
import timeit

instr = jaVisa().jav_Open(instru_ip,port=5025)                  #Create Object

###############################################################################
### Code Start
###############################################################################
# instr.write("INST:DEL 'Spectrum'")
instr.write(":TRIG:SEQ:SOUR IMM")               # Trigger Immediate
instr.write(":SENS:LTE:FRAM:SSUB ON")
instr.write(":SENS:SWE:TIME 0.00251")

instr.write(":SYST:PASS '894129'")              # Service Mode Password
instr.query("DIAG:SERV:SFUN? '2.0.46.5.1'")     # Service Mode to activate
#instr.query("DIAG:SERV:SFUN? '2.0.46.33'")     # Clear lookup table
#2.0.46.3.Mode.Reserve_cdB.InputLevel_Preamp15_RF.InputLevel_Preamp30_RF.MaxMixLevel_Gain0_RF.MaxMixLevel_Gain15_RF.MaxMixLevel_Gain30_RF
instr.query("DIAG:SERV:SFUN? '2.0.46.3.1.2.-10.-31.0.-20.-35'")

tick = timeit.default_timer()
rdStr = instr.query('INIT:IMM;*OPC?')
TotTime = timeit.default_timer() - tick
print( f'{TotTime:.6f},{rdStr}')

###############################################################################
### Cleanup Automation
###############################################################################
instr.jav_Close()
