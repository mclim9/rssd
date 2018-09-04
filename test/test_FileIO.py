from __future__ import print_function
##########################################################
### Rohde & Schwarz Software Test
###
### Purpose: Test FileIO.py
### Author:  mclim
### Date:    2018.06.04
##########################################################
### User Entry
##########################################################

##########################################################
### Code Start
##########################################################
import unittest
from rssd.FileIO     import FileIO

class TestGeneral(unittest.TestCase):
   def setUp(self):              #run before each test
      self.FileIO = FileIO()
      self.FileIO.Init("FileIO.csv")
      
   def test_write(self):
      self.FileIO.write("Hello World Test_FileIO.py")
      self.FileIO.write_raw("Hello World Test_FileIO.py Raw")
      
   def test_readcsv(self):
      data = self.FileIO.readcsv()
      for i, line in enumerate(data):
         print("%d:%s"%(i,",".join(data[i])))               
      self.assertEqual("as"+"df","asdf")
   
   def test_read(self):
      data = self.FileIO.read()
      for i, line in enumerate(data):
         print("%d:%s"%(i,",".join(line)))               
         
      self.assertTrue('FOO'.isupper())
      self.assertFalse('Foo'.isupper())
   
   def tearDown(self):
      pass

if __name__ == '__main__':
   if 0:    #Run w/o test names
      unittest.main()
   else:    #Verbose run
      suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
      unittest.TextTestRunner(verbosity=2).run(suite)
