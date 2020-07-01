##########################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : Timing SCPI Commands Example
### Author : mclim
##########################################################
### User Entry
##########################################################
numMeas = 10


##########################################################
### Code Begin
##########################################################
from datetime               import datetime    #pylint: disable=E0611,E0401
import time

for i in range(numMeas):        #Loop: # of Measurements
    tick = datetime.now()
    time.sleep(1)
    d = datetime.now() - tick
    print(f'{d.seconds:3d}.{d.microseconds:06d}')

