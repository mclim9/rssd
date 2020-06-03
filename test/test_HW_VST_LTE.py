###############################################################################
### Rohde & Schwarz Driver Test
### Purpose: VST.NR5G_K144 test
###              _   ___        __  _____
###             | | | \ \      / / |_   _|__  ___| |_
###             | |_| |\ \ /\ / /    | |/ _ \/ __| __|
###             |  _  | \ V  V /     | |  __/\__ \ |_
###             |_| |_|  \_/\_/      |_|\___||___/\__|
###             Please connect instrument prior 2 test
###############################################################################
### User Entry
###############################################################################
host    = '10.0.0.7'                                    #Get local machine name
SMW_IP  = '192.168.1.114'
FSW_IP  = '192.168.1.109'

###############################################################################
### Code Start
###############################################################################
import unittest
from rssd.VST.LTE import VST                            #pylint: disable=E0611,E0401

class TestGeneral(unittest.TestCase):
    def setUp(self):                                    #run before each test
        self.VST = VST().jav_OpenTest(SMW_IP,FSW_IP)

    def tearDown(self):                                 #Run after each test
        self.assertEqual(self.VST.SMW.jav_Error()[0],'0')
        self.assertEqual(self.VST.FSW.jav_Error()[0],'0')
        self.VST.jav_Close()

###############################################################################
### <Test>
###############################################################################
    def test_VST_Get_LTE_All(self):
        self.VST.Get_LTE_All()

    def test_VST_Get_LTE_All_print(self):
        self.VST.Get_LTE_All_print()

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
