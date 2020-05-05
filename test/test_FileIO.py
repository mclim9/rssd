# -*- coding: future_fstrings -*-
###############################################################################
### Rohde & Schwarz Software Test
###
### Purpose:Test FileIO.py
### Author: mclim
### Date:   2018.06.04
###############################################################################
### Code Start
###############################################################################
from rssd.FileIO      import FileIO             # pylint: disable=E0611,E0401
import unittest

class TestGeneral(unittest.TestCase):
    def setUp(self):                            #Run before each test
        self.FileIO = FileIO()
        self.FileIO.Init("FileIO.csv")
        self.FileIO.debug = 0

    def tearDown(self):                         #Run after each test
        self.FileIO.Outfile.close()

###############################################################################
### </Test>
###############################################################################
    def test_makeFile(self):
        newName = 'makeFile'
        self.FileIO.makeFile(newName)           #Append Date
        self.assertNotEqual(self.FileIO.sFName.find(newName),-1)

    def test_readcsv(self):
        self.FileIO.write('testreadcsv,spam,ham,eggs')
        data = self.FileIO.readcsv()            #Read as 2D Table
        size = len(data)
        self.assertEqual(data[size-1][3],'ham')

    def test_read(self):
        self.FileIO.write_raw('testread,spam,ham,eggs')
        data = self.FileIO.read()               #Read entire file
        size = len(data)
        self.assertEqual(data[size-1].strip(),'testread,spam,ham,eggs')
        # self.assertTrue('FOO'.isupper())
        # self.assertFalse('Foo'.isupper())

    def test_write(self):
        self.FileIO.write("test_write,write")           #Append Date
        self.FileIO.write_raw("test_write,write_raw")   #No Date
        # self.assertTrue(1)                  #FAIL

###############################################################################
### </Test>
###############################################################################
if __name__ == '__main__':
    # unittest.main()     #Run w/o test names
    suite = unittest.TestLoader().loadTestsFromTestCase(TestGeneral)
    unittest.TextTestRunner(verbosity=2).run(suite)
