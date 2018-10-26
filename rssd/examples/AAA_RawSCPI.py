##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2018.05.24
###
##########################################################
### User Entry
##########################################################
SMW_IP   = '192.168.1.114'
FSW_IP   = '192.168.1.109'
Freq     = 28e9
ChBW     = 100
subCarr  = [60, 120]
modArry  = ['QPSK', 'QAM64'] #QPSK; QAM16; QAM64; QAM256; PITB
numMeas  = 10

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.FSW_Common    import VSA
from rssd.SMW_Common    import VSG
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)
SMW = VSG().jav_Open(SMW_IP,OFile)  #Create SMW Object
FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

##########################################################
### Code Start
##########################################################
SCPI   = 'BB:ARB:WAV:DATA "test.wv",#23'
IQData = b"123456"
msg = SCPI.encode('UTF-8') + IQData
OFile.write(IQData)
SMW.write(msg)
print(SMW.query('SYST:ERR?'))

##########################################################
### Close Nicely
##########################################################
SMW.jav_Close()
