"""VSA Save 5GNR Test Mode Setting"""
###############################################################################
### User Entry
###############################################################################
#pylint: disable=E0611,E0401
FSW_IP   = '192.168.1.109'

###############################################################################
### Code Overhead: Import and create objects
###############################################################################
from rssd.VSA.NR5G_K144     import VSA
from rssd.VSG.NR5G_K144     import VSG
# from rssd.FileIO            import FileIO

FSW = VSA().jav_Open(FSW_IP)                        #Create FSW Object
SMW = VSG().jav_Open('192.168.1.114')               #Create SMW Object

###############################################################################
### Code Start
###############################################################################
FSW.Set_5GNR_Direction('DL')
cat = SMW.Get_5GNR_TM_Cat()
print(len(cat))

FSW.Set_SweepCont(0)
for file in cat:
    print(file)
    FSW.Set_5GNR_TM(file)
    FSW.Set_5GNR_savesetting(file)
    # FSW.query(f'MMEM:STOR:DEM:CC1 "TM\{file}.allocation";*OPC?')

###############################################################################
### Close Nicely
###############################################################################
FSW.jav_Close()
