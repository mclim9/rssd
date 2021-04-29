"""IQ --> SCPI --> SMW"""
SMW_IP   = '192.168.1.114'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
import numpy            as np
from rssd.VSG.Common    import VSG
SMW = VSG().jav_Open(SMW_IP)  #Create SMW Object

###############################################################################
### Code Start
###############################################################################
### :MMEM:DATA:UNPR "NVWFM://var//user//<wave.wv>",#<numSize><NumBytes><I0Q0...IxQx>
###     wave.wv : Name of *.wv to be created
###     numSize : Number of bytes in <NumBytes> string
###     NumBytes: Number of bytes to follow
###               Each I (or Q) value is two bytes
###               I(2 bytes) + Q(2bytes) = 4 bytes/IQ pair
###               NumBytes = NumIQPair * 4
###
IData = [0.1,0.2,0.3]
QData = [0.4,0.5,0.6]

### ASCII
scpi  = ':MMEM:DATA:UNPR "NVWFM://var//user//test.wv",#'        # Define file & number of bytes
iqsize= str(len(IData)*4)                                       # Calculate bytes of IQ data
scpi  = scpi + str(len(iqsize)) + iqsize                        # Calculate length of iqsize string

### Binary: IQ data --> Binary format
iqdata= np.vstack((IData,QData)).reshape((-1,),order='F')       # Combine I&Q Data
bits  = np.array(iqdata*32767, dtype='>i2')                     # Convert to big-endian 2byte int

### ASCII + Binary
cmd   = bytes(scpi, 'utf-8') + bits.tostring()                  # Add ASCII + Bin
SMW.K2.write_raw(cmd)
SMW.write('SOUR1:BB:ARB:WAV:CLOC "/var/user/test.wv",1.234E6')  # Set Fs/Clk Rate
SMW.write('BB:ARB:WAV:SEL "/var/user/test.wv"')                 # Select Arb File
print(SMW.query('SYST:ERR?'))

###############################################################################
### Close Nicely
###############################################################################
SMW.jav_Close()
