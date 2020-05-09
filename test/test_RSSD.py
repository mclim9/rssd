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
    def test_FileIO(self):
        from rssd.FileIO import FileIO              #pylint:disable=E0611,E0401
        self.FileIO = FileIO()

    def test_NRP_Common(self):
        from rssd.NRP.Common import PMr             #pylint:disable=E0611,E0401
        self.NRP = PMr()
        self.assertEqual(self.NRP.Model,"NRP")

    def test_NRQ_Common(self):
        from rssd.NRQ.Common import NRQ             #pylint:disable=E0611,E0401
        self.NRQ = NRQ()
        self.assertEqual(self.NRQ.Model,"NRQ")

    def test_OSP_Common(self):
        from rssd.OSP.Common import OSP             #pylint:disable=E0611,E0401
        self.OSP = OSP()
        self.assertEqual(self.OSP.Model,"OSP1x0")

    def test_OTA_Common(self):
        from rssd.OTA.Common import OTA             #pylint:disable=E0611,E0401
        self.OTA = OTA()
        self.assertEqual(self.OTA.Model,"OTA")

    def test_OTA_ATS1000(self):
        from rssd.OTA.ATS1000 import OTA            #pylint:disable=E0611,E0401
        self.OTA = OTA()
        self.assertEqual(self.OTA.Model,"ATS1000")

    def test_OTA_ATS1800(self):
        from rssd.OTA.ATS1800 import OTA            #pylint:disable=E0611,E0401
        self.OTA = OTA()
        self.assertEqual(self.OTA.Model,"ATS1800")

    def test_PNA_Common(self):
        from rssd.PNA.Common import PNA             #pylint:disable=E0611,E0401
        self.PNA = PNA()
        self.assertEqual(self.PNA.Model,"FSWP")

    def test_RCT_Common(self):
        from rssd.RCT.Common import RCT             #pylint:disable=E0611,E0401
        self.CMW = RCT()
        self.assertEqual(self.CMW.Model,"CMW-GPRF")

    def test_RCT_GPRF(self):
        from rssd.RCT.GPRF import RCT               #pylint:disable=E0611,E0401
        self.CMW = RCT()
        self.assertEqual(self.CMW.Model,"CMW-GPRF")

    def test_VNA_Common(self):
        from rssd.VNA.Common import VNA             #pylint:disable=E0611,E0401
        self.VNA = VNA()        
        self.assertEqual(self.VNA.Model,"VNA")

    def test_VSA_ADemod(self):
        from rssd.VSA.ADemod_K7 import VSA          #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_VSA_Common(self):
        from rssd.VSA.Common import VSA             #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_VSA_LTE(self):
        from rssd.VSA.LTE_K100 import VSA           #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_VSA_NoiseFigure(self):
        from rssd.VSA.NoiseFigure_K30 import VSA    #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_VSA_5GNR(self):
        from rssd.VSA.NR5G_K144 import VSA          #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_VSA_Transient(self):
        from rssd.VSA.Transient_K60 import VSA      #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_VSA_VectorDemod(self):
        from rssd.VSA.VSA_K70 import VSA            #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_VSA_WLAN(self):
        from rssd.VSA.WLAN_K91 import VSA           #pylint:disable=E0611,E0401
        self.FSW = VSA()
        self.assertEqual(self.FSW.Model,"FSW")

    def test_VSE_ADemod(self):
        from rssd.VSE.ADemod import VSE             #pylint:disable=E0611,E0401
        self.VSE = VSE()        
        self.assertEqual(self.VSE.Model,"VSE")

    def test_VSE_Common(self):
        from rssd.VSE.Common import VSE             #pylint:disable=E0611,E0401
        self.VSE = VSE()        
        self.assertEqual(self.VSE.Model,"VSE")

    def test_VSE_K96(self):
        from rssd.VSE.K96 import VSE                #pylint:disable=E0611,E0401
        self.VSE = VSE()
        self.assertEqual(self.VSE.Model,"VSE")

    def test_VSG_Common(self):
        from rssd.VSG.Common import VSG             #pylint:disable=E0611,E0401
        self.SMW = VSG()        
        self.assertEqual(self.SMW.Model,"SMW")

    def test_VSG_CDM(self):
        from rssd.VSG.CustomDigMod import VSG       #pylint:disable=E0611,E0401
        self.SMW = VSG()        
        self.assertEqual(self.SMW.Model,"SMW")

    def test_VSG_Fading(self):
        from rssd.VSG.Fading import VSG             #pylint:disable=E0611,E0401
        self.SMW = VSG()        
        self.assertEqual(self.SMW.Model,"SMW")

    def test_VSG_LTE_K55(self):
        from rssd.VSG.LTE_K55 import VSG            #pylint:disable=E0611,E0401
        self.SMW = VSG()        
        self.assertEqual(self.SMW.Model,"SMW")

    def test_VSG_5GNR(self):
        from rssd.VSG.NR5G_K144 import VSG          #pylint:disable=E0611,E0401
        self.SMW = VSG()
        self.assertEqual(self.SMW.Model,"SMW")

    def test_VSG_WLAN_K54(self):
        from rssd.VSG.WLAN_K54 import VSG           #pylint:disable=E0611,E0401
        self.SMW = VSG()        
        self.assertEqual(self.SMW.Model,"SMW")

    def test_VST_Common(self):
        from rssd.VST.Common import VST             #pylint:disable=E0611,E0401
        self.VST = VST()
        self.assertEqual(self.VST.Freq,19e9)

    def test_VST_LTE(self):
        from rssd.VST.LTE import VST                #pylint:disable=E0611,E0401
        self.VST = VST()
        self.assertEqual(self.VST.LTE_CC,1)

    def test_VST_NR5G(self):
        from rssd.VST.NR5G_K144 import VST          #pylint:disable=E0611,E0401
        self.VST = VST()
        self.assertEqual(self.VST.NR_TF,'OFF')

    def test_VST_WLAN(self):
        from rssd.VST.WLAN import VST               #pylint:disable=E0611,E0401
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
if __name__ == '__main__':                          # pragma: no cover
    # unittest.main()     #Run w/o test names
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)

