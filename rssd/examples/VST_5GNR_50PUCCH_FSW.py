FSW_IP      = '192.168.58.109'

from rssd.VSA.NR5G_K144     import VSA

FSW = VSA().jav_Open(FSW_IP)                          # Create FSW Object
FSW.debug = 0

FSW.Set_Freq(3.5e9)
FSW.Init_5GNR()
FSW.Set_5GNR_FrameCount('OFF')
FSW.Set_5GNR_Direction('UL')
# FSW.Set_5GNR_CellID(1024)
FSW.Set_5GNR_FreqRange('LOW')
FSW.Set_5GNR_ChannelBW(100)
FSW.write(f'CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:ALC 0')                               # PUSCH Allocations
FSW.write(f'CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:UCCC 50')                             # PUCCH Allocation
FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:CSL 1')                                    # User configurable slots, rest copy

for ch in range(0, 44):
    # Frame Configuration
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:FORM 0')                # Format
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:RBC 1')                 # Number of RB
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:RBOF {ch}')             # RB Offset
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:SCO 2')                 # Number of Symbol
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:SOFF 12')               # Symbol Offset
    # FSW.write(f':SOUR1:BB:NR5G:SCH:CELL0:SUBF0:USER{ch}:BWP0:ALL0:REP SLOT')      # Repitition

    # PUCCH Setting
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:ISFH ON')          # Intra Slot Freq Hop
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:HID NID')          # Hop ID type
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:NID {ch * 2}')     # Hop ID num
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:SHPR {272-ch}')    # 2nd Hop PBR
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:ICSH 6')           # Initial Cyclic Shift

for ch in range(44, 50):
    # Frame Configuration
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:FORM 2')                # Format
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:RBC 1')                 # Number of RB
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:RBOF {ch}')             # RB Offset
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:SCO 2')                 # Number of Symbol
    FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:SOFF 0')                # Symbol Offset

    # PUCCH Setting
    # FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:ISFH OFF')          # Intra Slot Freq Hop
    # FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:HID NID')          # Hop ID type
    # FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:NID {ch * 2}')     # Hop ID num
    # FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:SHPR {272-ch}')    # 2nd Hop PBR
    # FSW.write(f':CONF:NR5G:UL:CC1:FRAM1:BWP0:SLOT0:PUCC{ch}:DMRS:ICSH 6')           # Initial Cyclic Shift
