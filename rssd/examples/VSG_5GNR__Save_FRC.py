##########################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title  : SCPI Commands Example
### Author : mclim
### Date   : 2018.10.26
###
#               50MHz   100MHz  200MHz  400MHz
#     60kHz     66      132     264     NaN
#     120kHz    32      66      132     264

#               5MHz   10MHz    15MHz   20MHz   25MHz   30MHz   40MHz   50MHz   60MHz   80MHz   90MHz   100MHz
#     15kHz     25     52       79      106     133     160     216     270     NaN     NaN     NaN      NaN
#     30kHz     11     24       38      51      65      78      06      133     162     217     245      273
#     60kHz     NaN    11       18      24      31      38      51      65      79      107     121      135
##########################################################
### User Entry
##########################################################
SMW_IP      = '192.168.1.114'
cat_FR1     = {'FR1A11','FR1A12','FR1A13','FR1A14','FR1A15','FR1A16','FR1A17','FR1A18','FR1A19','FR1A21','FR1A22','FR1A23','FR1A24','FR1A25','FR1A26','FR1A31','FR1A310','FR1A311','FR1A312','FR1A313','FR1A314','FR1A315','FR1A316','FR1A317','FR1A318','FR1A319','FR1A32','FR1A320','FR1A321','FR1A322','FR1A323','FR1A324','FR1A325','FR1A326','FR1A327','FR1A328','FR1A329','FR1A33','FR1A330','FR1A331','FR1A332','FR1A34','FR1A35','FR1A36','FR1A37','FR1A38','FR1A39','FR1A41','FR1A410','FR1A411','FR1A412','FR1A413','FR1A414','FR1A415','FR1A416','FR1A417','FR1A418','FR1A419','FR1A42','FR1A420','FR1A421','FR1A422','FR1A423','FR1A424','FR1A425','FR1A426','FR1A427','FR1A428','FR1A43','FR1A44','FR1A45','FR1A46','FR1A47','FR1A48','FR1A49','FR1A51','FR1A510','FR1A511','FR1A512','FR1A513','FR1A514','FR1A52','FR1A53','FR1A54','FR1A55','FR1A56','FR1A57','FR1A58','FR1A59'}
cat_FR2_120 = {'FR2A12','FR2A13','FR2A15','FR2A310','FR2A312','FR2A33','FR2A34','FR2A35','FR2A38','FR2A39','FR2A410','FR2A43','FR2A44','FR2A45','FR2A48','FR2A49','FR2A53','FR2A54','FR2A55'}
cat_FR2_60  = {'FR2A11','FR2A14','FR2A31','FR2A311','FR2A32','FR2A36','FR2A37','FR2A41','FR2A42','FR2A46','FR2A47','FR2A51','FR2A52'}
# cat = cat_FR2
##########################################################
### Code Overhead: Import and create objects
##########################################################
from rssd.VSG.NR5G_K144     import VSG
# from rssd.FileIO            import FileIO

SMW = VSG().jav_Open(SMW_IP)  #Create SMW Object

##########################################################
### Code Start
##########################################################
SMW.Set_5GNR_Direction('UP')
SMW.write('SOUR1:BB:NR5G:UBWP:USER0:USCH:CCOD:STAT 1')
SMW.Set_5GNR_FRC_State('ON')
SMW.Set_5GNR_BBState('OFF')

SMW.Set_5GNR_FreqRange(2)
SMW.Set_5GNR_ChannelBW(400)
SMW.Set_5GNR_BWP_SubSpace(120)
SMW.Set_5GNR_BWP_ResBlock(264)
for file in cat_FR2_120:
    SMW.write(f'SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:TYPE {file}')
    Fil = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:TYPE?')
    if Fil == file:
        SCS = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:SCS?')     #Sub CarSpacing
        NRB = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:ALRB?')    #Num RB
        MOD = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:MOD?')     #Modulation
        PAS = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:PAS?')     #Payload Size
        SMW.write(f'SOUR1:BB:NR5G:SETT:STOR "/var/user/FRC/{file}-{SCS}-{NRB}-{MOD}-{PAS}"')

SMW.Set_5GNR_FreqRange(2)
SMW.Set_5GNR_ChannelBW(200)
SMW.Set_5GNR_BWP_SubSpace(60)
SMW.Set_5GNR_BWP_ResBlock(264)
for file in cat_FR2_60:
    SMW.write(f'SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:TYPE {file}')
    Fil = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:TYPE?')
    if Fil == file:
        SCS = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:SCS?')     #Sub CarSpacing
        NRB = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:ALRB?')    #Num RB
        MOD = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:MOD?')     #Modulation
        PAS = SMW.query('SOUR1:BB:NR5G:UBWP:USER0:CELL0:UL:BWP0:FRC:PAS?')     #Payload Size
        SMW.write(f'SOUR1:BB:NR5G:SETT:STOR "/var/user/FRC/{file}-{SCS}-{NRB}-{MOD}-{PAS}"')

##########################################################
### Close Nicely
##########################################################
SMW.jav_Close()
