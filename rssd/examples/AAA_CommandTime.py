###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Creatd : mclim, 2018.05.24
###############################################################################
### User Entry
###############################################################################
instru_ip  = '192.168.1.109'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.yaVISA_socket     import jaVisa
from rssd.FileIO            import FileIO
from datetime               import datetime
import timeit

OFile = FileIO().makeFile(__file__)
instr = jaVisa().jav_Open(instru_ip,OFile)                #Create Object

###############################################################################
### Code Start
###############################################################################
sDate = datetime.now().strftime("%y%m%d-%H:%M:%S")     #Date String
OFile.write('Iter,CmdTime,Response')

ALTime = []
for i in range(10):
    tick = timeit.default_timer()
    ### <\thing we are timing>
    # rdStr = instr.query(':SENS:ADJ:LEV;*OPC?')
    instr.write('INIT:IMM;*WAI')
    rdStr = instr.query('FETC:SUMM:EVM:ALL?')
    ### <\thing we are timing>
    tock = timeit.default_timer()
    a = tock - tick
    ALTime.append(a)
    OutStr = f'{sDate},{i},{ALTime[i]:.6f},{rdStr}'
    OFile.write (OutStr)

print(f'Avg time: {sum(ALTime) / float(len(ALTime))} secs')

###############################################################################
### Cleanup Automation
###############################################################################
instr.jav_Close()
