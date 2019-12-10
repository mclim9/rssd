###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Title  : 5GNR Measurements
### Creatd : mclim, 2019.12.11
###############################################################################
### User Entry
###############################################################################
instru_ip   = '192.168.1.109'
freq        = 15    #GHz

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.VSA.NR5G_K144     import VSA
from rssd.FileIO            import FileIO
import timeit

OFile = FileIO().makeFile(__file__)
FSW   = VSA().jav_Open(instru_ip,OFile)                     #Create Object

###############################################################################
### Code Start
###############################################################################
OFile.write('EVM,FreqError,ChPwr,Adj-,Adj+,SEM')            #Data Header

FSW.Set_Freq(freq * 1e9)
FSW.Set_SweepCont(0)

###########################
### EVM
###########################
FSW.Init_5GNR_Meas('EVM')
FSW.Set_InitImm()
EVM = FSW.query(':FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?')
EVM = EVM + ',' + FSW.query(':FETC:CC1:ISRC:FRAM:SUMM:FERR:AVER?')

###########################
### ACLR
###########################
FSW.Init_5GNR_Meas('ACLR')
FSW.Set_InitImm()
ACLR = FSW.Get_5GNR_ACLR()

FSW.Init_5GNR_Meas('ESP')
FSW.Set_InitImm()
SEM  = FSW.Get_5GNR_SEM()

"""
:FETC:CC1:ISRC:FRAM:SUMM:EVM:ALL:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:EVM:PCH:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:EVM:PSIG:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:FERR:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:SERR:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:IQOF:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:GIMB:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:QUAD:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:OSTP:AVER?
:FETC:CC1:ISRC:FRAM:SUMM:POW:AVER?
:FETC:CC1:ISRC:SUMM:CRES:AVER?
"""
OFile.write (f'{EVM},{ACLR},{SEM}')

###############################################################################
### Cleanup Automation
###############################################################################
FSW.jav_Close()