###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: rssd.VSG.Fading test
###              _   ___        __  _____         _
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host = '10.0.0.7'                                       #Get local machine name
host = '192.168.1.114'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VSG.Fading    import VSG
from rssd.test.yaVISA   import jaVISA_mock              #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                    #run before each test
        self.SMW = VSG()
        self.SMW.debug      = 0
        self.SMW.jav_Open(host)
        self.connected      = 1
        if self.SMW.K2 == 'NoVISA':
            mock = jaVISA_mock()
            self.SMW.jav_Open   = mock.jav_Open
            self.SMW.write      = mock.write
            self.SMW.query      = mock.query
            self.SMW.jav_Error  = mock.jav_Error
            self.connected      = 0
        self.SMW.jav_ClrErr()
        self.SMW.dLastErr = ""

    def tearDown(self):                                 #Run after each test
        self.assertEqual(self.SMW.jav_Error()[0],'0')
        self.SMW.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_SMW_Fading(self):
        getVal = self.SMW.Get_Fade_Standard()
        getVal = self.SMW.Get_Fade_State()

    def test_SMW_Fading_State(self):
        if self.connected: 
            self.SMW.Set_Fade_State('ON')
            # getVal = self.SMW.Get_Fade_State()
            # self.assertEqual(getVal,1)
            self.SMW.Set_Fade_State('OFF')
            # getVal = self.SMW.Get_Fade_State()
        else:
            pass

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
