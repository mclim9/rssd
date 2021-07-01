"""Timing SCPI Commands Example"""
import timeit
from rssd.instrument        import instr
from rssd.yaVISA_socket     import jaVisa

instr = jaVisa().jav_Open('192.168.58.109', port=5025)          # Create Object
instr.K2.settimeout(30)

def timeQuery(SCPI):
    tick = timeit.default_timer()
    rdStr = instr.query(SCPI)
    TotTime = timeit.default_timer() - tick
    outStr = f'{TotTime:.3f},{rdStr}'
    return outStr

data = timeQuery(':INIT:IMM;*OPC?;:FETC:ALL:SUMM:EVM:ALL?')     # MultiCC
capture = instr.query(':SENS:SWE:TIME?')
print(f'{capture},{data}')

instr.jav_Close()
