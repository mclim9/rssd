###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Date   : mclim.2020.05.12
###############################################################################
SMW_IP      = '192.168.1.114'
UserDir     = '2020.05.12-CMPEval'
###############################################################################
from rssd.VSG.NR5G_K144     import VSG
# from rssd.FileIO            import FileIO
SMW = VSG().jav_Open(SMW_IP)  #Create SMW Object

###############################################################################
### Code Start
###############################################################################
SMW.Set_OS_Dir(UserDir)
fileList = SMW.Get_OS_DirList()
for file in fileList:
    filename = file[0]
    if filename.find('.savrcltxt') > 0:
        SMW.Set_Setting(f'{UserDir}/{filename}')
        # SMW.Set_Setting(f'{filename}')
        SMW.Set_5GNR_GenerateWv(filename)
