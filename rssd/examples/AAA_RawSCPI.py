##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2018.10.26
###
##########################################################
### User Entry
##########################################################
SMW_IP   = '192.168.1.114'
FSW_IP   = '192.168.1.109'
Freq     = 28e9
ChBW     = 100

##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.FSW_Common    import VSA
from rssd.SMW_Common    import VSG
from rssd.FileIO        import FileIO

OFile = FileIO().makeFile(__file__)
SMW = VSG().jav_Open(SMW_IP,OFile)  #Create SMW Object
#FSW = VSA().jav_Open(FSW_IP,OFile)  #Create FSW Object

##########################################################
### Code Start
##########################################################
# parts
#scpi = "MMEM:DATA '/var/user/test.txt',#15hallo"
#scpi = 'BB:ARB:WAV:DATA "test.wv",#14'    #bytes = 2(I)+2(Q)= 4bytes = 1IQ sample
scpi  = ':MMEM:DATA:UNPR "NVWFM://var//user//wave.wv",#212'
bits  = b'\x00\x01\x02\x03\x00\x01\x02\x03\x00\x01\x02\x03'
cmd   = bytes(scpi, 'utf-8') + bits
print(bytes(cmd))
SMW.K2.write_raw(cmd)
SMW.write('SOUR1:BB:ARB:WAV:CLOC "/var/user/wave.wv",1.1E6')
SMW.write(':MMEM:DATA:UNPR "NVMKR:/var/user/wave.wv",#111')
SMW.write('BB:ARB:WAV:SEL "/var/user/wave.wv"')
print(SMW.query('SYST:ERR?'))

##########################################################
### Close Nicely
##########################################################
SMW.jav_Close()
