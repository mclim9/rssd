from rssd.VST.NR5G_K144 import VST           # pylint: disable=E0611,E0401

SMW_IP   = '192.168.58.114'                    # IP Address
FSW_IP   = '192.168.58.109'                    # IP Address

if __name__ == "__main__":
    NR5G = VST().jav_Open(SMW_IP, FSW_IP)
    NR5G.NR_CC = 1
    NR5G.Get_5GNR_All_print()
    NR5G.jav_Clear()
    NR5G.jav_Close()
