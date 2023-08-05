'''
Created on Jul 23, 2018

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.sequenceMethods import reverse_complement

class TestPAM_NNGRRT(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('GCTGGTCAGCACACCTGCTT', 'GCTGGTCAGCACACCTGCTTCAGGGT', 0, '-', '', '')
        self.candidates.add('GGTAGCTGAGGGAGGCTGAG', 'GGTAGCTGAGGGAGGCTGAGATGGAT', 0, '+', '', '')

        self.NNGRRT_PAM = pam.factory("NNGRRT")

    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        
        sites = self.candidates.getSitesSorted()
        
        seqs = self.NNGRRT_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        
        self.assertEqual(2*len(sites)+1, len(seqs))
        self.assertEqual('>' + sites[0].label, seqs[0])
        self.assertEqual('ANNCNN' + reverse_complement(sites[0].sequence[:-len(self.NNGRRT_PAM.PAM_str)]), seqs[1])
        self.assertEqual('>' + sites[1].label, seqs[2])
        self.assertEqual('ANNCNN' + reverse_complement(sites[1].sequence[:-len(self.NNGRRT_PAM.PAM_str)]), seqs[3])
        
    def test_getBowtieOptions(self):
        
        bowtieOptions = self.NNGRRT_PAM.getBowtieOptions('NA', 'NA', 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e240")
        

    def test_isBowtieHitConsistent(self):
        
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '4:?>N']))
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '12:C>G']))
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:G>N,2:G>N']))
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:G>N,2:A>N']))
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:A>N,2:G>N']))
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:A>N,2:A>N']))
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:C>N,2:C>N']))
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:T>N,2:C>N']))
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:C>N,2:T>N']))
        self.assertTrue(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:T>N,2:T>N']))
        
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:G>N,2:G>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:G>N,2:A>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:A>N,2:G>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:A>N,2:A>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:C>N,2:C>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:T>N,2:C>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:C>N,2:T>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:T>N,2:T>N']))
        
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:G>N,2:T>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:G>N,2:C>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:A>N,2:T>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:A>N,2:C>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:C>N,2:G>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:T>N,2:A>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:C>N,2:G>N']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '1:T>N,2:A>N']))
        
        
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:?>C']))
        self.assertFalse(self.NNGRRT_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '3:?>C']))

if __name__ == "__main__":
    unittest.main()