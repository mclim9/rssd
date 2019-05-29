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

class FileIO(object):
    """ Util File IO Object """
    def __init__(self):
        self.Outfile = ""
        self.sFName = ""
        self.debug = 1
        pass

    def makeFile(self,sFilepath):
        BaseDir  = os.path.dirname(os.path.realpath(sFilepath))
        BaseFile = os.path.basename(sFilepath)
        OutFile  = f'{BaseDir}\\{BaseFile}'
        self.Init(OutFile)
        return self

    def Init(self,sName="Datalog"):
        self.sFName = "%s-%s.csv"%(sName,datetime.now().strftime("%y%m%d"))
        self.Outfile = open(self.sFName, 'a')              #Open File
        return self

    def write(self,inStr):
        if self.debug: print("FileOut    : %s"%inStr)
        sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
        with open(self.sFName, 'a') as csv_file:
            csv_file.write(f'{sDate},{inStr}\n')

    def write_raw(self,inStr):
        if self.debug: print("FileOut_raw : %s"%inStr)
        with open(self.sFName, 'a') as csv_file:
            csv_file.write(f'{inStr}\n')

    def read(self):
        with open(self.sFName, 'r') as csv_file:
            fileData = csv_file.readlines()
        return fileData

    def readcsv(self):
        dataOut = []
        with open(self.sFName, 'r') as csv_file:
            fileData = csv_file.readlines()
            for line in fileData:
                dataOut.append(line.strip().split(','))
        return dataOut

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
