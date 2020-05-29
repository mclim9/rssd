# -*- coding: future_fstrings -*-
#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title : Common file functions
### Author: Martin C Lim
### Date  : 2018.02.01
#####################################################################
from datetime  import datetime
import os

class FileIO(object):                                       #pylint: disable=R0205
    """ Util File IO Object """
    def __init__(self):
        self.Outfile = ""
        self.sFName = ""
        self.debug = 1

    def makeFile(self,sFilepath):
        BaseDir  = os.path.dirname(os.path.realpath(sFilepath))
        BaseFile = os.path.basename(sFilepath)
        OutFile  = f'{BaseDir}\\{BaseFile}'
        self.Init(OutFile)
        return self

    def Init(self,sName="Datalog"):
        self.sFName = "%s-%s.csv"%(sName,datetime.now().strftime("%y%m%d"))
        return self

    def write(self,inStr):                                  #pylint: disable=R0201,W0613
        pass

    def write_raw(self,inStr):                              #pylint: disable=R0201,W0613
        pass

    def read(self):                                         #pylint: disable=R0201,W0613
        return 'asdkfal;sdf;jkasljk;df;jklasfd;jklasjkl;dfjkasdfljk;as;lkjf'

    def readcsv(self):                                      #pylint: disable=R0201,W0613
        return ['str1','str2','str3','str4','str5']

    def initread(self,sFile):
        self.sFName = sFile
        return self

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    FileIO = FileIO()
    FileIO.Init("FileIO.csv")
    FileIO.write("Hello World")
    FileIO.write_raw("Hello Worldd")
    data = FileIO.readcsv()
    for i, line in enumerate(data):
        print("%d:%s"%(i,",".join(data[i])))
