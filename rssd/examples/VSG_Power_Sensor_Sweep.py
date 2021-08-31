###############################################################################
### Rohde & Schwarz Automation for demonstration use.
###############################################################################
SMW_IP      = '192.168.1.114'
SMW_IP      = '10.0.0.10'
FreqArry    = [24e9, 28e9, 39e9]
PwrArry     = range(-50, 0, 2)

###############################################################################
from rssd.VSG.Common        import VSG
from rssd.FileIO            import FileIO

FIL = FileIO().makeFile(__file__)
SMW = VSG().jav_Open(SMW_IP, FIL)  #Create SMW Object

###############################################################################
### Code Start
###############################################################################
SMW.Set_IQMod('OFF')
for frq in FreqArry:
    SMW.Set_Freq(frq)
    # SMW.Set_NRP_Freq(frq)
    for pwr in PwrArry:
        SMW.Set_RFPwr(pwr)
        SMW.Set_RFState(1)
        rdStr = SMW.Get_NRPPower()
        FIL.write(f'{frq},{pwr},{rdStr}')
