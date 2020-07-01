###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.VSG.NR5G_K144    import VSG

SMW = VSG().jav_Open('10.0.0.10')  #Create SMW Object

###############################################################################
### User Entry
###############################################################################
SlotDir     = 'DDDSU'       #Frame Pattern
Entities    = [1,2,3,4]
RVPatt      = [0,2,3,1]
SlotNum     = 8             #Num of Slots per Subframe
SubFNum     = 10            #Num of SubFrame per Frame
currSlot    = 0
RVIi        = 0
FrameInfo   = []
numAlloc    = [0]*SubFNum   #Num Alloc per SubFrame

for SubF in range(SubFNum):                             # Loop through all slots in Frame individually 
    numAlloc[SubF] = 0                                  # Start Each Frame w/ 0 allocations
    FrameInfo.append([])                                # Blank Slot Definition
    for Slot in range(SlotNum):
        UDdir = currSlot % len(SlotDir)                 # Retrieve Uplink/Downlink Direction from UDdir
        if 'U' in SlotDir[UDdir]:                       # If this slot is U
            numAlloc[SubF] += 1                         #   - Add Allocation
            RVI = RVPatt[RVIi%len(RVPatt)]              #   - Identify next RVI in RVPatt
            FrameInfo[SubF].append([SubF,Slot,RVI])     #   - Add SubFrame; Slot# and RVI into our Frame Definition
            print(f'SubF:{SubF} Slot:{Slot} RVI:{RVI}') #   - Print for verification.
            RVIi += 1
        currSlot += 1

for ent in Entities:
    SMW.write(f'ENT{ent}:SOUR1:BB:NR5G:STAT 0')         # Baseband off
    for SubF in range(SubFNum):
        SMW.write(f':ENT{ent}:SOUR1:BB:NR5G:SCH:CELL0:SUBF{SubF}:USER0:BWP0:NALL {numAlloc[SubF]}')
        for alloc in range(numAlloc[SubF]):
            RVI = FrameInfo[SubF][alloc][2]
            SMW.write(f':ENT{ent}:SOUR1:BB:NR5G:SCH:CELL0:SUBF{SubF}:USER0:BWP0:ALL{alloc}:SLOT {FrameInfo[SubF][alloc][1]}')
            SMW.write(f':ENT{ent}:SOUR1:BB:NR5G:SCH:CELL0:SUBF{SubF}:USER0:BWP0:ALL{alloc}:REP OFF')
            SMW.write(f':ENT{ent}:SOUR1:BB:NR5G:SCH:CELL0:SUBF{SubF}:USER0:BWP0:ALL{alloc}:PUSCh:CCOD:RVIN {RVI}')
    SMW.jav_Wait(f'ENT{ent}:SOUR1:BB:NR5G:STAT 1')      # Baseband On & Calculate
