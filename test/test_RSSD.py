from __future__ import print_function
#coding: future_fstrings
###############################################################################
### Rohde & Schwarz SCPI Driver Software Test
###
### Purpose: Import Library-->Create Object-->Catch obvious typos.
###          Tests do not require instrument.
### Author:  mclim
### Date:    2018.06.13
###############################################################################
### Code Start
###############################################################################
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #Run before each test
        print("",end="")
        pass

    def tearDown(self):                             #Run after each test
        pass

###############################################################################
### <Test>
###############################################################################
    def test_CMW_GPRF(self):
        from rssd.CMW_GPRF import BSE               #pylint:disable=E0611,E0401
        self.CMW = BSE()
        self.assertEqual(self.CMW.Model,"CMW-GPRF")
        
    def test_FileIO(self):
        from rssd.FileIO import FileIO              #pylint:disable=E0611,E0401
        self.FileIO = FileIO()

    def test_FSW_5GNR(self):
        from rssd.FSW_5GNR_K144 import VSA          #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_FSW_ADemod(self):
        from rssd.FSW_ADemod_K7 import VSA          #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_FSW_Common(self):
        from rssd.FSW_Common import VSA             #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_FSW_LTE(self):
        from rssd.FSW_LTE_K100 import VSA           #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_FSW_NoiseFigure(self):
        from rssd.FSW_NoiseFigure_K30 import VSA   #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_FSW_Transient(self):
        from rssd.FSW_Transient_K60 import VSA      #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_FSW_WLAN(self):
        from rssd.FSW_WLAN_K91 import VSA           #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_NRP_Common(self):
        from rssd.NRP_Common import PMr             #pylint:disable=E0611,E0401
        self.NRP = PMr()
        self.assertEqual(self.NRP.Model,"NRP")

    def test_NRQ_Common(self):
        from rssd.NRQ_Common import NRQ             #pylint:disable=E0611,E0401
        self.NRQ = NRQ()
        self.assertEqual(self.NRQ.Model,"NRQ")

    def test_OSP_Common(self):
        from rssd.OSP_Common import OSP             #pylint:disable=E0611,E0401
        self.OSP = OSP()
        self.assertEqual(self.OSP.Model,"OSP1x0")

    def test_SMW_5GNR(self):
        from rssd.SMW_5GNR_K144 import VSG          #pylint:disable=E0611,E0401
        self.SMW = VSG()        
        self.assertEqual(self.SMW.Model,"SMW")

    def test_SMW_Common(self):
        from rssd.SMW_Common import VSG             #pylint:disable=E0611,E0401
        self.SMW = VSG()        
        self.assertEqual(self.SMW.Model,"SMW")

    def test_SMW_LTE_K55(self):
        from rssd.SMW_LTE_K55 import VSG            #pylint:disable=E0611,E0401
        self.SMW = VSG()        
        self.assertEqual(self.SMW.Model,"SMW")

    def test_SMW_WLAN_K54(self):
        from rssd.SMW_WLAN_K54 import VSG           #pylint:disable=E0611,E0401
        self.SMW = VSG()        
        self.assertEqual(self.SMW.Model,"SMW")

    def test_VNA_Common(self):
        from rssd.VNA_Common import VNA             #pylint:disable=E0611,E0401
        self.VNA = VNA()        
        self.assertEqual(self.VNA.Model,"VNA")

    def test_VSE_ADemod(self):
        from rssd.VSE_ADemod import VSE             #pylint:disable=E0611,E0401
        self.VSE = VSE()        
        self.assertEqual(self.VSE.Model,"VSE")

    def test_VSE_Common(self):
        from rssd.VSE_Common import VSE             #pylint:disable=E0611,E0401
        self.VSE = VSE()        
        self.assertEqual(self.VSE.Model,"VSE")

    def test_VSE_K96(self):
        from rssd.VSE_Common import VSE             #pylint:disable=E0611,E0401
        self.VSE = VSE()
        self.assertEqual(self.VSE.Model,"VSE")

    def test_VST_5GNR(self):
        from rssd.VST_5GNR_K144 import VST          #pylint:disable=E0611,E0401
        self.VST = VST()
        self.assertEqual(self.VST.NR_TF,'OFF')

    def test_VST_Common(self):
        from rssd.VST_Common import VST             #pylint:disable=E0611,E0401
        self.VST = VST()
        self.assertEqual(self.VST.Freq,19e9)

    def test_VST_LTE(self):
        from rssd.VST_LTE import VST                #pylint:disable=E0611,E0401
        self.VST = VST()
        self.assertEqual(self.VST.LTE_CC,1)

    def test_VST_WLAN(self):
        from rssd.VST_WLAN import VST               #pylint:disable=E0611,E0401
        self.VST = VST()
        self.assertEqual(self.VST.WLAN_MCS,1)

    def test_yaVISA(self):
        from rssd.yaVISA import jaVisa              #pylint:disable=E0611,E0401
        self.K2 = jaVisa()

    def test_yaVISASocket(self):
        from rssd.yaVISA_socket import jaVisa       #pylint:disable=E0611,E0401
        self.K2 = jaVisa()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    if 0:     #Run w/o test names
        unittest.main()
    else:     #Verbose run
        suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
        unittest.TextTestRunner(verbosity=2).run(suite)
