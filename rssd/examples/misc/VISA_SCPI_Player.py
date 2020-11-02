"""Rohde & Schwarz Automation for demonstration use. """
#pylint: disable=invalid-name, unused-import
import os
import logging
import pyvisa
host = '10.0.0.16'                                  #Instrument IP address

###############################################################################
### Code Begin
###############################################################################
def readSCPI():
    '''read SCPI array from file'''
    SCPIFile = os.path.splitext(__file__)[0] + '.txt'
    SCPIOut = []
    with open(SCPIFile, 'r') as csv_file:
        fileData = csv_file.readlines()
        for line in fileData:
            if line[0] != "#":                          # Remove Comments
                SCPIOut.append(line)
    return SCPIOut

def sendSCPI(SCPIarry):
    '''send SCPI array.  Check error after each cmd'''
    for cmd in SCPIarry:
        try:
            if '?' in cmd:
                instr.query(cmd)
            else:
                instr.write(cmd)
            error = instr.query('SYST:ERR?')
            outStr = f'{error.strip()} {cmd.strip()}'
            logging.info(outStr)
        except pyvisa.VisaIOError:
            error = 'SCPI TIMEOUT' + instr.query('SYST:ERR?')
            outStr = f'{error.strip()} {cmd.strip()}'
            logging.error(outStr)

###############################################################################
### Main Code
###############################################################################
rm = pyvisa.ResourceManager()                           #Create Resource Manager
instr = rm.open_resource(f'TCPIP0::{host}::hislip0::INSTR')                      #Create Visa Obj
instr.timeout = 5000                                    #Timeout, millisec
# logger = logging.getLogger(__name__)
# logger.setLevel(logging.DEBUG)
# file_handler = logging.FileHandler(os.path.splitext(__file__)[0] + '.log')
# formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)
logging.basicConfig(level=logging.DEBUG, \
    filename=os.path.splitext(__file__)[0] + '.log', filemode='w', \
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
arry = readSCPI()
sendSCPI(arry)
# getSysInfo()
