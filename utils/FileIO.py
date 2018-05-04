#####################################################################
### Rohde & Schwarz Automation for demonstration use.
###
### Title : Common file functions
### Author: Martin C Lim
### Date  : 2018.02.01
#####################################################################
import time

class FileIO():
   def __init__(self):
      self.Outfile = ""
      self.sFName = ""
      self.debug = 1
      pass
      
   def Init(self,sName="Datalog"):
      self.sFName = "%s-%s.csv"%(sName,time.strftime("%y%m%d"))
      self.Outfile = open(self.sFName, 'a')           #Open File
      return self.Outfile
      
   def Write(self,inStr):
      if self.debug: print(inStr)
      self.Outfile = open(self.sFName, 'a')           #Open File
      self.Outfile.write(inStr+'\n')
      self.Outfile.close()

   def WriteDate(self,inStr):
      if self.debug: print(inStr)
      sDate = time.strftime("%y%m%d,%H%M%S")       #Date String
      self.Outfile = open(self.sFName, 'a')           #Open File
      self.Outfile.write('%s,%s\n'%(sDate,inStr))
      self.Outfile.close()
      
#####################################################################
### Run if Main
#####################################################################
if __name__ == "__main__":
   ### this won't be run when imported
   FileIO = FileIO()
   FileIO.Init("Test.py")
   FileIO.Write("Hello World")
   FileIO.WriteDate("Hello Worldd")
