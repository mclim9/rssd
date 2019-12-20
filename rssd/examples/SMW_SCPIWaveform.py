###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Raw Binary to SMW
### Author : mclim
### Date   : 2018.10.26
###############################################################################
### User Entry
###############################################################################
SMW_IP   = '192.168.1.114'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.VSG.Common    import VSG
from rssd.FileIO        import FileIO

SMW = VSG().jav_Open(SMW_IP)  #Create SMW Object

###############################################################################
### Code Start
###############################################################################
### :MMEM:DATA:UNPR "NVWFM://var//user//<wave.wv>",#<numSize><NumBytes><I0Q0...IxQx>
###     wave.wv : Name of *.wv to be created
###     numSize : Number of bytes in <NumBytes>
###     NumBytes: Number of bytes to follow.
###               Each I (or Q) value is two bytes
###               I(2 bytes) + Q(2bytes) = 4 bytes/IQ pair
###               NumBytes = NumIQPair * 4
###
scpi  = ':MMEM:DATA:UNPR "NVWFM://var//user//wave.wv",#14'      # Ascii Cmd
bits  = b'\x00\x01\x02\x03'                                     # Binary Data
cmd   = bytes(scpi, 'utf-8') + bits                             # Add ASCII + Bin
print(bytes(cmd))
SMW.K2.write_raw(cmd)
SMW.write('SOUR1:BB:ARB:WAV:CLOC "/var/user/wave.wv",1.1E6')    # Set Fs/Clk Rate
SMW.write('BB:ARB:WAV:SEL "/var/user/wave.wv"')                 # Select Arb File
print(SMW.query('SYST:ERR?'))

###############################################################################
### Close Nicely
###############################################################################
SMW.jav_Close()
