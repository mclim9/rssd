###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Creatd : mclim, 2018.05.24
###############################################################################
### User Entry
###############################################################################
instru_ip  = '127.0.0.1'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.yaVISA_socket     import jaVisa                       #pylint: disable=E0611,E0401
from rssd.FileIO            import FileIO                       #pylint: disable=E0611,E0401
import timeit

instr = jaVisa().jav_Open(instru_ip,port=5025)                  #Create Object

###############################################################################
### Code Start
###############################################################################
tick = timeit.default_timer()
rdStr = instr.query('*IDN?;*OPC?')
TotTime = timeit.default_timer() - tick
print( f'{TotTime:.6f},{rdStr}')

###############################################################################
### Cleanup Automation
###############################################################################
instr.jav_Close()
