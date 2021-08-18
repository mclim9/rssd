"""Timing SCPI Commands Example"""
import timeit
from rssd.instrument        import instr

# K2SO = instr().open('192.168.58.114')
K2SO = instr().open('192.168.58.109', type='hislip')
K2SO.timeout(1)

def timeQuery(SCPI):
    tick = timeit.default_timer()
    rdStr = K2SO.query(SCPI)
    TotTime = timeit.default_timer() - tick
    outStr = f'{TotTime:.3f},{rdStr}'
    return outStr

print(timeQuery('*IDN?'))
print(timeQuery(':SENS:FREQ:CENT 24e9;*OPC?'))
# print(timeQuery(':INIT:IMM;*OPC?'))

K2SO.close()
