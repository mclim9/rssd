"""Instrument IDN String"""
from rssd.instrument import instr

for IPAddr in ['192.168.58.109','192.168.58.114','127.0.0.1']:
    kyber = instr().open(IPAddr)
    print(kyber.query('*IDN?'))
    kyber.close()
