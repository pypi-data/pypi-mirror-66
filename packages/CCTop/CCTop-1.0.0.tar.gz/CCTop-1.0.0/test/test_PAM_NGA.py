'''
Created on Jul 23, 2018

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.sequenceMethods import reverse_complement

class TestPAM_NGA(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('TACCTTCATACATGGCAAGG', 'TACCTTCATACATGGCAAGGTGA', 0, '-', '', '')
        self.candidates.add('TATGAAGGTAAATCCCTCAG', 'TATGAAGGTAAATCCCTCAGGGA', 0, '+', '', '')

        self.NGA_PAM = pam.factory("NGA")

    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        
        sites = self.candidates.getSitesSorted()
        
        seqs = self.NGA_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        
        self.assertEqual(2*len(sites)+1, len(seqs))
        self.assertEqual('>' + sites[0].label, seqs[0])
        self.assertEqual('TCN' + reverse_complement(sites[0].sequence[:-len(self.NGA_PAM.PAM_str)]), seqs[1])
        self.assertEqual('>' + sites[1].label, seqs[2])
        self.assertEqual('TCN' + reverse_complement(sites[1].sequence[:-len(self.NGA_PAM.PAM_str)]), seqs[3])
        
    def test_getBowtieOptions(self):
        bowtieOptions = self.NGA_PAM.getBowtieOptions(2, 12, 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l15")
        self.assertEqual(bowtieOptions[5], "-e150")
        
        bowtieOptions = self.NGA_PAM.getBowtieOptions('NA', 'NA', 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e150")
        

    def test_isBowtieHitConsistent(self):
        
        self.assertTrue(self.NGA_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:?>N']))
        self.assertTrue(self.NGA_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '12:C>G']))
        self.assertFalse(self.NGA_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '1:?>G,2:G>N,15:A>G,18:C>G,21:A>T']))
        self.assertFalse(self.NGA_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:?>C']))

if __name__ == "__main__":
    unittest.main()