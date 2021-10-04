import unittest

from lw_pub_statistics import LWdata

class TestPubsInfo(unittest.TestCase):

    def test_modelLWdata(self):
        data = LWdata()
        self.assertAlmostEqual(data.publicationInfo(2012)) # check dataframe 
        with self.assertRaises(AssertionError):       # to trigger and test for intended failure
            data.publicationInfo(200)

if __name__ == '__main__':
    unittest.main()