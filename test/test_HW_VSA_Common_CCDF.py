"""rssd.FSW.common_CCDF test
"""
host = '192.168.1.109'                              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        self.FSW = VSA().jav_OpenTest(host)
        self.FSW.Init_CCDF()

    def tearDown(self):                             #Run after each test
        self.assertEqual(self.FSW.jav_Error()[0],'0')
        self.FSW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_FSW_CCDF_Common(self):
        self.FSW.Set_CCDF('ON')
        self.FSW.Set_SweepCont(0)
        self.FSW.Set_CCDF_BW(10e6)
        self.FSW.Set_CCDF_Samples(1e6)
        self.FSW.Set_InitImm()
        getVal = self.FSW.Get_CCDF()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # coverage run -a -m unittest -b -v test_HW_VSA_Common_CCDF
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
