"""5G NR Carrier Aggregation FSW/SMW Example"""
###############################################################################
### User Entry
###############################################################################
SMW_IP      = '192.168.58.114'
FSW_IP      = '192.168.58.109'
NR_Dir      = 'UL'
VSG_ON      = 0
NumCC       = 8

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
import os
import logging
from rssd.VSG.NR5G_K144     import VSG
from rssd.VSA.NR5G_K144     import VSA

logging.basicConfig(level=logging.INFO, \
                    filename=os.path.splitext(__file__)[0] + '.csv', filemode='w', \
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
###############################################################################
### Code Start
###############################################################################
pwr = 100
if VSG_ON: 
    SMW = VSG().jav_Open(SMW_IP)                        # Create SMW Object
    SMW.Set_5GNR_Direction(NR_Dir)

FSW = VSA().jav_Open(FSW_IP)                            # Create FSW Object
FSW.Set_5GNR_Direction(NR_Dir)

###############################################################################
### Measure Time
###############################################################################
LoopParam   = f'Model,CurrFreq,pwr,CC,NumCC'
header      = f'{LoopParam},{FSW.Get_Params_Amp(1)},{FSW.Get_5GNR_Params_EVM(1)}'
logging.info(header)
evm_arry    = []
FSW.Set_InitImm()
for CC in range(NumCC):                                 # LOOP: CC
    FSW.cc = CC+1
    CurrFreq    = FSW.Get_5GNR_CC_Freq()
    LoopParam   = f'{FSW.Model},{CurrFreq/1e9:9.6f},{pwr:3d},{FSW.cc},{NumCC}'
    AttnParam   = FSW.Get_Params_Amp()
    EVM         = FSW.Get_5GNR_Params_EVM()
    evm_arry.append(float(EVM.split(',')[3]))
    OutStr      = f'{LoopParam},{AttnParam},{EVM}'
    logging.info(OutStr)

print(f'Delta:{max(evm_arry)-min(evm_arry):.3f}  Max:{max(evm_arry)} Min:{min(evm_arry)}')
if VSG_ON: SMW.jav_Close()                              # Close SMW Object
FSW.jav_Close()                                         # Close FSW Object
