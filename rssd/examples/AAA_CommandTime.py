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
from rssd.yaVISA_socket import jaVisa
from rssd.FileIO        import FileIO
from datetime           import datetime

OFile = FileIO().makeFile(__file__)                     # Create File
instr = jaVisa().jav_Open(instru_ip,OFile)              # Instrument Object

###############################################################################
### Code Start
###############################################################################
sDate = datetime.now().strftime("%y%m%d-%H:%M:%S")      #Date String
OFile.write('Date,Iter,CmdTime,Response')

ALTime = []
for i in range(10):
    tick = datetime.now()
    ### <\thing we are timing>
    rdStr = instr.query('INIT:IMM;*OPC?')
    ### <\thing we are timing>
    tock = datetime.now()
    a = tock - tick
    ALTime.append(a.seconds + (a.microseconds/1e6))
    OutStr = f'{sDate},{i},{ALTime[i]:.6f},{rdStr}'
    OFile.write (OutStr)

print(f'Avg time: {sum(ALTime) / float(len(ALTime))} secs')

###############################################################################
### Cleanup Automation
###############################################################################
instr.jav_Close()
