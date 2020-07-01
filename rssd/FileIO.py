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

    def makeFile(self,sFilepath):
        """"Create file in same directory as sFilepath."""
        BaseDir  = os.path.dirname(os.path.realpath(sFilepath))
        BaseFile = os.path.basename(sFilepath)
        OutFile  = f'{BaseDir}\\{BaseFile}'
        self.init(OutFile)
        return self

    def init(self,sName="Datalog"):
        """Append to sName file"""
        self.sFName = "%s-%s.csv"%(sName,datetime.now().strftime("%y%m%d"))
        self.Outfile = open(self.sFName, 'a')                               #Open File
        return self

    def set_filename(self,sFile):
        self.sFName = sFile
        return self

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

    def readdict(self):
        """Text file split w/ space"""
        d = {}
        # BaseDir  = os.path.dirname(os.path.realpath(__file__))
        # os.chdir(BaseDir)
        # dirpath = os.getcwd()
        with open(self.sFName) as f:
            for line in f:
                # (key, val) = line.split()
                try:
                    (key, val) = line.split()
                except ValueError:
                    key = line.split(' ')[0]
                    val = line.split(' ')[1]
                d[key] = val
        return d

    def write(self,inStr):
        if self.debug: print("FileOut    : %s"%inStr)
        sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
        with open(self.sFName, 'a') as csv_file:
            csv_file.write(f'{sDate},{inStr}\n')

    def write_raw(self,inStr):
        if self.debug: print("FileOut_raw : %s"%inStr)
        with open(self.sFName, 'a') as csv_file:
            csv_file.write(f'{inStr}\n')

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
    ### this won't be run when imported
    FileIO = FileIO()
    FileIO.init("FileIO.csv")
    FileIO.write("Hello World")
    FileIO.write_raw("Hello Worldd")
    data = FileIO.readcsv()
    for i, line in enumerate(data):
        print("%d:%s"%(i,",".join(data[i])))
