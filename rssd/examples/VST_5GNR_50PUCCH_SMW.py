###############################################################################
### Rohde & Schwarz Automation for demonstration use.
#pylint: disable=E0611,E0401
###############################################################################
SMW_IP      = '192.168.58.114'
freqArry    = [28e9]

###############################################################################
### Overhead
###############################################################################
from rssd.VSG.NR5G_K144     import VSG
# from rssd.VSA.NR5G_K144     import VSA
# from rssd.FileIO            import FileIO
# from rssd.RSI.time          import timer

# OFile = FileIO().makeFile(__file__)
# TMR = timer()
SMW = VSG().jav_Open(SMW_IP)                          #Create SMW Object
SMW.debug = 0
# FSW = VSA().jav_Open(FSW_IP)                          #Create FSW Object
# FSW.debug = 0

# def NR5G_Rx_Init():
#     """Start 5GNR Measurement Channel"""
#     FSW.Init_5GNR()
#     FSW.Set_5GNR_FrameCount('OFF')

###############################################################################
### Code Start
###############################################################################
SMW.Set_Freq(28e9)
SMW.Set_5GNR_BBState('OFF')
SMW.Set_5GNR_Direction('UL')
SMW.Set_5GNR_BWP_CellID(777)
SMW.Set_5GNR_FreqRange('LOW')
SMW.Set_5GNR_ChannelBW(100)
SMW.Set_5GNR_BWP_Users(10)

for ch in range(0,10):
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:NALL 1')
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:CONT PUCC')
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:FMT F0')           # Format
    # SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:RBN 1')          # Number of RB
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:RBOF {ch}')         # RB Offset
    # SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:SYMN 2')         # Number of Symbol
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:SYM 0')            # Symbol offset
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:REP SLOT')         # Repitition
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:FS:CYCS 6')   # Initial Cyclic Shift

# RBOffset = 50
# RBSize = 16
# for i in range(6):
#     ch = i + 44
#     SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:NALL 1')
#     SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:CONT PUCC')
#     SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:FMT F2')           # Format
#     SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:RBN {RBSize}')     # Number of RB
#     SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:RBOF {RBOffset + i*RBSize}')         # RB Offset
#     #MMM Causes Crash
#     # SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:SYMN 2')         # Number of Symbol
#     SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:SYM 0')            # Symbol offset
#     SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:REP SLOT')         # Repitition
#     SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:FS:CYCS 6')   # Initial Cyclic Shift


# :SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER2:BWP0:ALL0:PUCCh:GRPHopping ENA
# :SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER2:BWP0:ALL0:PUCCh:GRPHopping N
# :SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER2:BWP0:ALL0:PUCCh:ISFHopping 1
# :SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER2:BWP0:ALL0:PUCCh:SHOPping 8

SMW.Set_5GNR_BBState('ON')
