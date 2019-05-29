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
        self.Outfile = open(self.sFName, 'a')              #Open File
        self.Outfile.write('%s,%s\n'%(sDate,inStr))
        self.Outfile.close()

    def write_raw(self,inStr):
        if self.debug: print("FileOut_raw : %s"%inStr)
        self.Outfile = open(self.sFName, 'a')              #Open File
        self.Outfile.write('%s\n'%(inStr))
        self.Outfile.close()

    def read(self):
        self.Outfile = open(self.sFName, 'r')
        fileData = self.Outfile.readlines()
        self.Outfile.close()
        return fileData
        
    def readcsv(self):
        dataOut = []
        self.Outfile = open(self.sFName, 'r')
        fileData = self.Outfile.readlines()
        for line in fileData:
            dataOut.append(line.strip().split(','))
        self.Outfile.close()
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
