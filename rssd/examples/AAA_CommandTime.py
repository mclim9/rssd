""" Timing SCPI Commands Example"""
import  timeit
from rssd.yaVISA_socket     import jaVisa
from rssd.FileIO            import FileIO

OFile = FileIO().makeFile(__file__)
instr = jaVisa().jav_Open('192.168.58.109', OFile)                 #Create Object
instr.K2.settimeout(30)

###############################################################################
### Code Start
###############################################################################
OFile.write('Iter,CmdTime,Response')

ALTime = []
for i in range(1):
    rdStr = ''
    tick = timeit.default_timer()

    ### <\thing we are timing>
    instr.query('INIT:IMM;*OPC?')
    rdStr = instr.query('FETC:SUMM:EVM:ALL?')
    ### <\thing we are timing>

    ALTime.append(timeit.default_timer() - tick)
    OutStr = f'{i},{ALTime[i]:.6f},{rdStr}'
    OFile.write(OutStr)

print(f'Avg time  : {sum(ALTime) / float(len(ALTime))} secs')

instr.jav_Close()
