'''
Created on Jul 23, 2018

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.sequenceMethods import reverse_complement

class TestPAM_NNNNRYAC(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('CCATCTTCCAGTTGCTGCTT', 'CCATCTTCCAGTTGCTGCTTTTGCACAC', 0, '-', '', '')
        self.candidates.add('TGCTGCCATCTCTGTCTTCG', 'TGCTGCCATCTCTGTCTTCGCTTCACAC', 0, '+', '', '')

        self.NNNNRYAC_PAM = pam.factory("NNNNRYAC")

    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        
        sites = self.candidates.getSitesSorted()
        
        seqs = self.NNNNRYAC_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        
        self.assertEqual(2*len(sites)+1, len(seqs))
        self.assertEqual('>' + sites[0].label, seqs[0])
        self.assertEqual('GTNNNNNN' + reverse_complement(sites[0].sequence[:-len(self.NNNNRYAC_PAM.PAM_str)]), seqs[1])
        self.assertEqual('>' + sites[1].label, seqs[2])
        self.assertEqual('GTNNNNNN' + reverse_complement(sites[1].sequence[:-len(self.NNNNRYAC_PAM.PAM_str)]), seqs[3])
        
    def test_getBowtieOptions(self):
        
        bowtieOptions = self.NNNNRYAC_PAM.getBowtieOptions('NA', 'NA', 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e300")
        

    def test_isBowtieHitConsistent(self):
        
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '4:?>N']))
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '12:C>G']))
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:G>N,3:C>N']))
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:G>N,3:T>N']))
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:A>N,3:C>N']))
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:A>N,3:T>N']))
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '2:C>N,3:G>N']))
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '2:C>N,3:A>N']))
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '2:T>N,3:G>N']))
        self.assertTrue(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '2:T>N,3:A>N']))
        
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:G>N,2:G>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:G>N,2:A>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:A>N,2:G>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:A>N,2:A>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:C>N,2:C>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:T>N,2:C>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:C>N,2:T>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:T>N,2:T>N']))
        
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:G>N,2:T>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:G>N,2:C>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:A>N,2:T>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:A>N,2:C>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:C>N,2:G>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:T>N,2:A>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:C>N,2:G>N']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:T>N,2:A>N']))
        
        
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:?>C']))
        self.assertFalse(self.NNNNRYAC_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '3:?>C']))

if __name__ == "__main__":
    unittest.main()