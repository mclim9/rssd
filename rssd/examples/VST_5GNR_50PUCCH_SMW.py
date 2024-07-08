SMW_IP      = '192.168.58.114'
freqArry    = [28e9]

from rssd.VSG.NR5G_K144     import VSG

SMW = VSG().jav_Open(SMW_IP)                          # Create SMW Object
SMW.debug = 0

###############################################################################
# ## Code Start
###############################################################################
SMW.Set_Freq(3.5e9)
SMW.Set_5GNR_BBState('OFF')
SMW.Set_5GNR_Direction('UL')
# SMW.Set_5GNR_BWP_CellID(1024)
SMW.write(':SOUR1:BB:NR5G:UBWP:USER0:UEID 1024')
SMW.Set_5GNR_FreqRange('LOW')
SMW.Set_5GNR_ChannelBW(100)
SMW.Set_5GNR_BWP_Users(50)

for ch in range(0, 44):
    # Frame Configuration
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:NALL 1')                   # Add User
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:CONT PUCC')           # Select PUCCH
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:FMT F0')              # Format
    # SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:RBN 1')             # Number of RB
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:RBOF {ch}')           # RB Offset
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:SYMN 2')              # Number of Symbol
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:SYM 12')              # Symbol offset
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:REP SLOT')            # Repitition

    # PUCCH Setting
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:ISFH 1')         # Intra Slot Freq Hop
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:HOP {ch * 2}')   # Hop ID
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:SHOP {272-ch}')  # 2nd Hop PBR
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:FS:CYCS 6')   # Initial Cyclic Shift

RBSize = 1
for ch in range(44, 50):
    # Frame Configuration
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:NALL 1')                   # Add User
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:CONT PUCC')           # Select PUCCH
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:FMT F2')              # Format
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:RBN {RBSize}')        # Number of RB
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:RBOF {ch}')           # RB Offset
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:SYMN 2')              # Number of Symbol
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:SYM 0')               # Symbol offset
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:REP SLOT')            # Repitition

    # PUCCH Setting
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:ISFH 1')         # Intra Slot Freq Hop
    # SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:HOP {ch * 2}')   # Hop ID
    SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:SHOP {272-ch}')  # 2nd Hop PBR
    # SMW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:PUCC:FS:CYCS 6')   # Initial Cyclic Shift

SMW.Set_5GNR_BBState('ON')
