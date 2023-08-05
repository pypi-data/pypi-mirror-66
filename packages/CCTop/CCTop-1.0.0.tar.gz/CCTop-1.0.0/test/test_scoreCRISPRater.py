'''
Created on Mar 26, 2014

@author: juan
'''
import unittest

from cctop.scoreCRISPRater import getScore

class TestScoreCRISPRater(unittest.TestCase):
    def setUp(self):
        pass
    
    def tearDown(self):
        pass

    def test_getScore(self):
        self.assertAlmostEqual(getScore("TTCCCAACTCAGAAAAGGAG"),0.6238839)
        self.assertAlmostEqual(getScore("CTGCCTCTCCTTTTCTGAGT"),0.6027914)
        self.assertAlmostEqual(getScore("ATGCTTTCCCAACTCAGAAA"),0.7056449)
        self.assertAlmostEqual(getScore("TTTTCTGAGTTGGGAAAGCA"),0.4780395)
        self.assertAlmostEqual(getScore("TGCCTCTCCTTTTCTGAGTT"),0.6584332)
        
if __name__ == "__main__":
    unittest.main()
