4##########################################################
### Rohde & Schwarz Software Test
###
### Purpose: self.SMW_driver software test
### Author:  mclim
### Date:    2018.06.13
##########################################################
### User Entry
##########################################################
host = '192.168.1.115'           #Get local machine name
host = '127.0.0.1'               #Get local machine name

##########################################################
### Code Start
##########################################################
from rssd.SMW_Common import VSG
import unittest

class TestGeneral(unittest.TestCase):
   def setUp(self):                 #run before each test
      self.SMW = VSG()
      try:
         self.SMW.VISA_Open(host)
         self.SMW.VISA_Reset()
         self.SMW.VISA_ClrErr()
         self.SMW.dLastErr = ""
      except:
         self.assertTrue(1)

   def test_SMW_Connect(self):
      self.assertEqual(self.SMW.Make,"Rohde&Schwarz")

   def test_SMW_Common(self):      
      self.SMW.Set_Freq(1e6)
      self.SMW.Set_Power(10)
      self.SMW.Get_Freq()
      self.SMW.Get_Level()
      self.assertEqual(self.SMW.dLastErr,"")

if __name__ == '__main__':
	unittest.main()
