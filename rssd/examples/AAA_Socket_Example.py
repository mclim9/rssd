""" Rohde & Schwarz Automation for demonstration use"""
from rssd.yaVISA_socket     import jaVisa

FSW = jaVisa().jav_Open('192.168.58.109',port=5025)                  #Create Object
SMW = jaVisa().jav_Open('192.168.58.114',port=5025)                  #Create Object
###############################################################################
### Code Start
###############################################################################
idn_fsw = FSW.query('*IDN?;*OPC?')
idn_smw = SMW.query(('*IDN?'))
print(f'{idn_fsw}')
print(f'{idn_smw}')

FSW.jav_Close()
SMW.jav_Close()
