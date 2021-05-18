"""Timing SCPI Commands Example"""
instru_ip  = '192.168.58.109'

import timeit
from rssd.yaVISA_socket     import jaVisa                       #pylint: disable=E0611,E0401

instr = jaVisa().jav_Open(instru_ip,port=5025)                  #Create Object
instr.K2.settimeout(30)

def timeCommand(SCPI):
    tick = timeit.default_timer()
    rdStr = instr.query(SCPI)
    TotTime = timeit.default_timer() - tick
    outStr = f'{TotTime:.3f},{rdStr}'
    return outStr

###############################################################################
### Code Start
###############################################################################

data = timeCommand(':INIT:IMM;*OPC?;:FETC:ALL:SUMM:EVM:ALL?')     # MultiCC
# data = timeCommand(':INIT:IMM;*OPC?;FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?') # Single CC
capture = instr.query(':SENS:SWE:TIME?')
# ccMode  = instr.query(':CONF:NR5G:CSC?')
# numcc   = instr.query(':CONF:NR5G:NOCC?')
# print(f'{ccMode},{numcc},{capture},{data}')
print(f'{capture},{data}')

instr.jav_Close()
