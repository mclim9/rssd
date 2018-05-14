##########################################################
### Rohde & Schwarz Software Test
###
### Purpose: self.FSW_driver software test
### Author:  mclim
### Date:    2018.05.07
##########################################################
### User Entry
##########################################################
host = '192.168.1.109'           #Get local machine name
host = '127.0.0.1'               #Get local machine name
port = 5025                      #Reserve a port for your service.

##########################################################
### Code Start
##########################################################
from rssd.FSW_Common import VSA
import unittest

class TestGeneral(unittest.TestCase):
   def setUp(self):                 #run before each test
      self.FSW = VSA()
      try:
         self.FSW.VISA_Open(host)
         self.FSW.VISA_Reset()
         self.FSW.VISA_ClrErr()
         self.FSW.dLastErr = ""
      except:
         self.assertTrue(1)

   def test_FSW_Connect(self):
      self.assertEqual(self.FSW.Make,"Rohde&Schwarz")

   def test_FSW_Common(self):      
      self.FSW.Set_Freq(1e6)
      self.FSW.Set_RefLevel(10)
      self.FSW.Set_ResBW(1e6)
      self.FSW.Set_VidBW(1e6)
      self.FSW.Set_Span(100e6)
      self.FSW.Get_Attn()
      self.FSW.Get_RefLevel()
      self.assertEqual(self.FSW.dLastErr,"")

   def test_FSW_Marker(self):      
      self.FSW.Set_Mkr_Peak()
      self.FSW.Get_Mkr_Freq()
      self.assertEqual(self.FSW.dLastErr,"")

if __name__ == '__main__':
	unittest.main()
