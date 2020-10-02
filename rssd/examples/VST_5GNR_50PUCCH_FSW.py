###############################################################################
### Rohde & Schwarz Automation for demonstration use.
#pylint: disable=E0611,E0401
###############################################################################
FSW_IP      = '192.168.58.109'
freqArry    = [28e9]

###############################################################################
### Overhead
###############################################################################
from rssd.VSA.NR5G_K144     import VSA

FSW = VSA().jav_Open(FSW_IP)                          #Create FSW Object
FSW.debug = 0

def NR5G_Rx_Init():
    """Start 5GNR Measurement Channel"""
    FSW.Init_5GNR()
    FSW.Set_5GNR_FrameCount('OFF')

###############################################################################
### Code Start
###############################################################################
FSW.Set_Freq(28e9)
FSW.Set_5GNR_Direction('UL')
FSW.Set_5GNR_CellID(777)
FSW.Set_5GNR_FreqRange('LOW')
FSW.Set_5GNR_ChannelBW(100)
# FSW.Set_5GNR_BWP_Users(50)
FSW.write(f'CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:ALC 0')                               # PUSCH Allocation
FSW.write(f'CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:UCCC 40')                             # PUCCH Allocation

for i in range(0,10):
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC0:FORM 0')                   # Format
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{i}:RBC 1')                  # Number of RB
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{i}:RBOF {i}')               # RB Offset
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{i}:SCO 2')                  # Number of Symbol
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{i}:SOFF 0')                 # Symbol Offset
    # FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:ALL0:REP SLOT')         # Repitition
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC0:DMRS:ICSH  6')             # Initial Cyclic Shift
    
# RBOffset = 50
# RBSize = 14
# for i in range (44-50):
#     FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:NALL 1')
#     FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:ALL0:CONT PUCC')
#     FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:ALL0:FMT F2')           # Format
#     FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:ALL0:RBN {RBSize}')     # Number of RB
#     FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:ALL0:RBOF {RBOffset + i*RBSize}')         # RB Offset
#     # FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:ALL0:SYMN 2')         # Number of Symbol
#     FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:ALL0:SYM 0')            # Symbol offset
#     FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:ALL0:REP SLOT')         # Repitition
#     FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{i}:BWP0:ALL0:PUCC:FS:CYCS 6')   # Initial Cyclic Shift

