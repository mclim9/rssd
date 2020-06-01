# # -*- coding: future_fstrings -*-
# ###############################################################################
### Purpose: rssd.FSW.common_CCDF test
###              _   ___        __  _____         _
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '192.168.1.109'                              #Get local machine name

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSA.Common        import VSA              #pylint: disable=E0611,E0401
from rssd.test.yaVISA       import jaVISA_mock      #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                #run before each test
        print("",end="")
        self.FSW = VSA()
        self.FSW.debug      = 0
        self.FSW.jav_Open(host)
        self.connected      = 1
        if self.FSW.K2 == 'NoVISA':
            mock = jaVISA_mock()
            self.FSW.jav_Open   = mock.jav_Open
            self.FSW.write      = mock.write
            self.FSW.query      = mock.query
            self.FSW.jav_Error  = mock.jav_Error
            self.connected      = 0
        self.FSW.jav_ClrErr()
        self.FSW.dLastErr = ""
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
        getVal = self.FSW.Get_CCDF()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
