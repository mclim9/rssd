from __future__ import print_function
##########################################################
### Rohde & Schwarz SCPI Driver Software Test
###
### Purpose: Import Libraries.  Catch obvious typos.
###          Tests do not require instrument.
### Author:  mclim
### Date:    2018.06.13
##########################################################
### User Entry
##########################################################

##########################################################
### Code Start
##########################################################
import unittest

class TestGeneral(unittest.TestCase):
   def setUp(self):              #run before each test
      pass
      
   def test_CMW_GPRF(self):
      from rssd.CMW_GPRF import BSE
      self.CMW = BSE()
      self.assertEqual(self.CMW.Model,"CMW-GPRF")
      
   def test_FSW_Common(self):
      from rssd.FSW_Common import VSA
      self.FSW = VSA()
      self.assertEqual(self.FSW.Model,"FSW")
      
   def test_FSW_5GNR(self):
      from rssd.FSW_5GNR_K144 import VSA
      self.FSW = VSA()
      self.assertEqual(self.FSW.Model,"FSW")

   def test_FSW_LTE(self):
      from rssd.FSW_LTE_K100 import VSA
      self.FSW = VSA()
      self.assertEqual(self.FSW.Model,"FSW")
      
   def test_SMW_Common(self):
      from rssd.SMW_Common import VSG
      self.SMW = VSG()      
      self.assertEqual(self.SMW.Model,"SMW")
      
   def test_VSE_Common(self):
      from rssd.VSE_Common import VSE
      self.VSE = VSE()      
      self.assertEqual(self.VSE.Model,"VSE")
      
   def test_VSE_K96(self):
      from rssd.VSE_Common import VSE
      self.VSE = VSE()
      self.assertEqual(self.VSE.Model,"VSE")
      
      
   def tearDown(self):
      pass

if __name__ == '__main__':
   if 0:    #Run w/o test names
      unittest.main()
   else:    #Verbose run
      suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
      unittest.TextTestRunner(verbosity=2).run(suite)
