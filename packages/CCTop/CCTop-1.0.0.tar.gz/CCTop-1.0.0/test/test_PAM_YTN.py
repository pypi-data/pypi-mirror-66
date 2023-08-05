'''
Created on Mar 3, 2019

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
#from sequenceMethods import reverse_complement

class TestPAM_YTN(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('GTTATGGCTCCCTGAGGGAT', 'TTTTGTTATGGCTCCCTGAGGGAT', 0, '-', '', '')
        self.candidates.add('GTAAATGACTGACATCCaag', 'TTTCGTAAATGACTGACATCCaag', 0, '+', '', '')

        self.YTN_PAM = pam.factory("YTN")

    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        
        sites = self.candidates.getSitesSorted()
        
        seqs = self.YTN_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        
        self.assertEqual(4*len(sites)+1, len(seqs))
        self.assertEqual('>' + sites[0].label, seqs[0])
        self.assertEqual('TTN' + sites[0].sequence[len(self.YTN_PAM.PAM_str):], seqs[1])
        self.assertEqual('>' + sites[0].label, seqs[2])
        self.assertEqual('CTN' + sites[0].sequence[len(self.YTN_PAM.PAM_str):], seqs[3])
        
        self.assertEqual('>' + sites[1].label, seqs[4])
        self.assertEqual('TTN' + sites[1].sequence[len(self.YTN_PAM.PAM_str):], seqs[5])
        self.assertEqual('>' + sites[1].label, seqs[6])
        self.assertEqual('CTN' + sites[1].sequence[len(self.YTN_PAM.PAM_str):], seqs[7])
        
    def test_getBowtieOptions(self):
           
        bowtieOptions = self.YTN_PAM.getBowtieOptions('NA', 'NA', 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e150")
        

    def test_isBowtieHitConsistent(self):
        
        self.assertTrue(self.YTN_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:?>N']))
        self.assertTrue(self.YTN_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '12:C>G']))
        self.assertFalse(self.YTN_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '1:?>G,2:G>N,15:A>G,18:C>G,21:A>T']))
        self.assertFalse(self.YTN_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:?>C']))

if __name__ == "__main__":
    unittest.main()
