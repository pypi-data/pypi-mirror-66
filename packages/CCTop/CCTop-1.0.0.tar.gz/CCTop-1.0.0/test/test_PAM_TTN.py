'''
Created on Mar 3, 2019

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites

class TestPAM_TTN(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('GTTATGGCTCCCTGAGGGAT', 'TTTTGTTATGGCTCCCTGAGGGAT', 0, '-', '', '')
        self.candidates.add('GTAAATGACTGACATCCaag', 'TTTCGTAAATGACTGACATCCaag', 0, '+', '', '')

        self.TTN_PAM = pam.factory("TTN")

    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        
        sites = self.candidates.getSitesSorted()
        
        seqs = self.TTN_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        
        self.assertEqual(2*len(sites)+1, len(seqs))
        self.assertEqual('>' + sites[0].label, seqs[0])
        self.assertEqual('TTN' + sites[0].sequence[len(self.TTN_PAM.PAM_str):], seqs[1])
        
        self.assertEqual('>' + sites[1].label, seqs[2])
        self.assertEqual('TTN' + sites[1].sequence[len(self.TTN_PAM.PAM_str):], seqs[3])
        
        
    def test_getBowtieOptions(self):
           
        bowtieOptions = self.TTN_PAM.getBowtieOptions('NA', 'NA', 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e150")
        

    def test_isBowtieHitConsistent(self):
        
        self.assertTrue(self.TTN_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:?>N']))
        self.assertTrue(self.TTN_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '12:C>G']))
        self.assertFalse(self.TTN_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '1:?>G,2:G>N,15:A>G,18:C>G,21:A>T']))
        self.assertFalse(self.TTN_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:?>C']))

if __name__ == "__main__":
    unittest.main()
