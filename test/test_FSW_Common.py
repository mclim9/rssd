##########################################################
### Rohde & Schwarz Software Test
###
### Purpose: FSW_driver software test
### Author:  mclim
### Date:    2018.05.07
##########################################################
### User Entry
##########################################################
host = '192.168.1.109'           #Get local machine name
port = 5025                      #Reserve a port for your service.

##########################################################
### Code Start
##########################################################
from rssd.FSW_Common import VSA
import unittest

class TestGeneral(unittest.TestCase):
   def setUp(self):                 #run before each test
      FSW = VSA()
      FSW.VISA_Open(host)
      FSW.VISA_Reset()
      FSW.VISA_ClrErr()
      FSW.dLastErr = ""

   def test_FSW_Connect(self):
      self.assertEqual(FSW.Make,"Rohde&Schwarz")

   def test_FSW_Common(self):      
      FSW.Set_Freq(1e6)
      FSW.Set_RefLevel(10)
      FSW.Set_ResBW(1e6)
      FSW.Set_VidBW(1e6)
      FSW.Set_Span(100e6)
      FSW.Get_Attn()
      FSW.Get_RefLevel()
      self.assertEqual(FSW.dLastErr,"")

   def test_FSW_Marker(self):      
      FSW.Set_Mkr_Peak()
      FSW.Get_Mkr_Freq()
      self.assertEqual(FSW.dLastErr,"")
      

if __name__ == '__main__':
	unittest.main()
