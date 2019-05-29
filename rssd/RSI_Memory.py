# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Automation for demonstration use.
### Purpose: Rohde & Scharz Instrument Functions
### Author : Martin C Lim
### Date   : 2019.05.10
###  _____  _____   ____ _______ ____ _________     _______  ______ 
### |  __ \|  __ \ / __ \__   __/ __ \__   __\ \   / /  __ \|  ____|
### | |__) | |__) | |  | | | | | |  | | | |   \ \_/ /| |__) | |__    
### |  ___/|  _  /| |  | | | | | |  | | | |    \   / |  ___/|  __|  
### | |    | | \ \| |__| | | | | |__| | | |     | |  | |    | |____ 
### |_|    |_|  \_\\____/  |_|  \____/  |_|     |_|  |_|    |______|
###                         _            _           _ 
###                        | |          | |         | |
###             _   _ _ __ | |_ ___  ___| |_ ___  __| |
###            | | | | '_ \| __/ _ \/ __| __/ _ \/ _` |
###            | |_| | | | | ||  __/\__ \ ||  __/ (_| |
###             \__,_|_| |_|\__\___||___/\__\___|\__,_|
###
###############################################################################
from rssd.yaVISA import jaVisa

class RSI(jaVisa):
    """ Rohde & Schwarz Instrument Memory Object """
    def __init__(self):
        super(RSI, self).__init__()
        self.Model = "AAA"

    #####################################################################
    ### AAA Get Functions
    #####################################################################
    def Get_dirInfo(self):
        # FSW/FSVA uses ':MMEM:CAT:LONG?'
        # SMW/ZVA  uses ':MMEM:CAT?'
        dirInfo = self.query(':MMEM:CAT:LONG?')
        if '<notRead>' in dirInfo:
            dirInfo = self.query(':MMEM:CAT?')
        dirInfo = dirInfo.strip().replace('"','').split(',')
        print(dirInfo,'\n')
        if len(dirInfo) > 2:
            self.usedSpace = dirInfo.pop(0)
            self.freeSpace = dirInfo.pop(0)
            self.dir       = []
            self.files     = {}
            for i in range(0, len(dirInfo), 3):
                if dirInfo[i+1] == 'DIR':
                    self.dir.append(dirInfo[i])                             #Add directories to self.dir
                else:
                    self.files[dirInfo[i]]= int(dirInfo[i+2])               #Add file to self.files
        return dirInfo

    def Get_File(self,filename):
        self.Get_dirInfo()
        self.write(f':MMEM:DATA? {filename}')
        size = self.files[filename]
        rdStr = self.K2.read_raw(self.files[filename])
        return rdStr

    #####################################################################
    ### AAA Get Functions
    #####################################################################
    def Set_Copy(self,fromLoc, toLoc):
        self.write(f'MMEM:COPY {fromLoc},{toLoc}')

    def Set_Dir(self,dir):
        self.write(f'MMEM:CDIR {dir}')

    def Set_Filename(self,filename):
        self.write(f'MMEM:NAME {filename}')

    def Set_Move(self,fromLoc, toLoc):
        self.write(f'MMEM:MOVE {fromLoc},{toLoc}')


###############################################################################
### Debug Main.  Won't run when imported
###############################################################################
if __name__ == "__main__":
    RSI = RSI().jav_Open("192.168.1.108")
    asdf = RSI.Get_File('autolog.txt')
    RSI.jav_ClrErr()