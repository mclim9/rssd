###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Creatd : mclim, 2018.05.24
###############################################################################
### User Entry
###############################################################################
instru_ip  = '192.168.1.107'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
import  timeit
from rssd.yaVISA_socket     import jaVisa
from rssd.FileIO            import FileIO

OFile = FileIO().makeFile(__file__)
instr = jaVisa().jav_Open(instru_ip,OFile)                  #Create Object

###############################################################################
### Code Start
###############################################################################
OFile.write('Iter,CmdTime,Response')

ALTime = []
for i in range(10):
    rdStr = ''
    tick = timeit.default_timer()
    ### <\thing we are timing>
    if 1:
        instr.query('INIT:IMM;*OPC?')
    # instr.write(':INST:COUP:RLEV ON')
    # rdStr = instr.query('FETC:SUMM:EVM:ALL?')
    ### <\thing we are timing>
    ALTime.append(timeit.default_timer() - tick)
    OutStr = f'{i},{ALTime[i]:.6f},{rdStr}'
    OFile.write (OutStr)

print(f'Avg time  : {sum(ALTime) / float(len(ALTime))} secs')

###############################################################################
### Cleanup Automation
###############################################################################
instr.jav_Close()
