#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title : Common file functions
### Author: Martin C Lim
### Date  : 2018.02.01
#####################################################################
from datetime  import datetime

class FileIO(object):
   def __init__(self):
      self.Outfile = ""
      self.sFName = ""
      self.debug = 1
      pass
      
   def Init(self,sName="Datalog"):
      self.sFName = "%s-%s.csv"%(sName,datetime.now().strftime("%y%m%d"))
      self.Outfile = open(self.sFName, 'a')           #Open File
      return self.Outfile
      
   def write(self,inStr):
      if self.debug: print("FileOut     : %s"%inStr)
      sDate = datetime.now().strftime("%y%m%d-%H:%M:%S.%f") #Date String
      self.Outfile = open(self.sFName, 'a')           #Open File
      self.Outfile.write('%s,%s\n'%(sDate,inStr))
      self.Outfile.close()

   def write_raw(self,inStr):
      if self.debug: print("FileOut_raw : %s"%inStr)
      self.Outfile = open(self.sFName, 'a')           #Open File
      self.Outfile.write('%s\n'%(inStr))
      self.Outfile.close()
   
   def read(self):
      self.Outfile = open(self.sFName, 'r')
      fileData = self.Outfile.readlines()
      return fileData
      
   def readcsv(self):
      dataOut = []
      self.Outfile = open(self.sFName, 'r')
      fileData = self.Outfile.readlines()
      for line in fileData:
         dataOut.append(line.split(','))
      return dataOut
      

#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FileIO = FileIO()
   FileIO.Init("FileIO.csv")
   FileIO.write("Hello World")
   FileIO.write_raw("Hello Worldd")
   data = FileIO.read()
   for line in data:
      #print(i)
      print(line)
