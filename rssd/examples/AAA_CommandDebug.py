"""Timing SCPI Commands Example"""
import timeit
from rssd.instrument        import instr

# K2SO = instr().open('192.168.58.114')
K2SO = instr().open('192.168.58.114', type='hislip')
K2SO.timeout(1)

def timeQuery(SCPI):
    tick = timeit.default_timer()
    rdStr = K2SO.query(SCPI)
    TotTime = timeit.default_timer() - tick
    outStr = f'{TotTime:.3f},{rdStr}'
    return outStr

# data = timeQuery(':INIT:IMM;*OPC?')
data = timeQuery(':CAL1:IQM:LOC?')
# capture = K2SO.query(':SENS:SWE:TIME?')
print(f'{data}')

K2SO.close()
