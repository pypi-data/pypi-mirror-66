'''
Created on Jul 23, 2018

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.sequenceMethods import reverse_complement

class TestPAM_NNAGAAW(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('AGGCTGGCGGTGCTGCTCTT', 'AGGCTGGCGGTGCTGCTCTTTGAGAAT', 0, '-', '', '')
        self.candidates.add('AGAGCATTGCTCTGGTAAGG', 'AGAGCATTGCTCTGGTAAGGGCAGAAT', 0, '+', '', '')

        self.NNAGAAW_PAM = pam.factory("NNAGAAW")

    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        
        sites = self.candidates.getSitesSorted()
        
        seqs = self.NNAGAAW_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        
        self.assertEqual(2*len(sites)+1, len(seqs))
        self.assertEqual('>' + sites[0].label, seqs[0])
        self.assertEqual('NTTCTNN' + reverse_complement(sites[0].sequence[:-len(self.NNAGAAW_PAM.PAM_str)]), seqs[1])
        self.assertEqual('>' + sites[1].label, seqs[2])
        self.assertEqual('NTTCTNN' + reverse_complement(sites[1].sequence[:-len(self.NNAGAAW_PAM.PAM_str)]), seqs[3])
        
    def test_getBowtieOptions(self):
        
        bowtieOptions = self.NNAGAAW_PAM.getBowtieOptions('NA', 'NA', 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n1")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e210")
        

    def test_isBowtieHitConsistent(self):
        
        self.assertTrue(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '5:?>N']))
        self.assertTrue(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '12:C>G']))
        self.assertTrue(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:A>N']))
        self.assertTrue(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:T>N']))
        
        self.assertFalse(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:G>N']))
        self.assertFalse(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:C>N']))        
        
        self.assertFalse(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '1:?>C']))
        self.assertFalse(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '2:?>C']))
        self.assertFalse(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '3:?>C']))
        self.assertFalse(self.NNAGAAW_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '4:?>C']))

if __name__ == "__main__":
    unittest.main()