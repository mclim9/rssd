###############################################################################
### Rohde & Schwarz Software Test
###
### Purpose: self.SMW_driver software test
### Author:  mclim
### Date:    2018.06.13
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.114'              #Get local machine name

###############################################################################
### Code Start
###############################################################################
from rssd.SMW_Common import VSG
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                      #run before each test
        self.SMW = VSG()
        try:
            self.SMW.jav_Open(host)
            self.SMW.jav_Reset()
            self.SMW.jav_ClrErr()
            self.SMW.dLastErr = ""
        except:
            self.assertTrue(1)

    def test_SMW_Connect(self):
        self.assertEqual(self.SMW.jav_Error()[0],'0')

    def test_SMW_Common(self):        
        self.SMW.Set_Freq(1e6)
        self.SMW.Set_RFPwr(10)
        self.SMW.Get_Freq()
        self.SMW.Get_PowerRMS()
        self.assertEqual(self.SMW.jav_Error()[0],'0')

###############################################################################
if __name__ == '__main__':
	unittest.main()
