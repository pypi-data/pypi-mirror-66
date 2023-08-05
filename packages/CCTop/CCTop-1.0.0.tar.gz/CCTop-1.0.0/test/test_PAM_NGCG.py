'''
Created on Jul 23, 2018

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.sequenceMethods import reverse_complement

class TestPAM_NGCG(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('CTGGCAGGGAAAACGTGTGA', 'CTGGCAGGGAAAACGTGTGAAGCG', 0, '-', '', '')
        self.candidates.add('CTGAAGCAGGTGTGCTGACC', 'CTGAAGCAGGTGTGCTGACCAGCG', 0, '+', '', '')

        self.NGCG_PAM = pam.factory("NGCG")

    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        
        sites = self.candidates.getSitesSorted()
        
        seqs = self.NGCG_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        
        self.assertEqual(2*len(sites)+1, len(seqs))
        self.assertEqual('>' + sites[0].label, seqs[0])
        self.assertEqual('CGCN' + reverse_complement(sites[0].sequence[:-len(self.NGCG_PAM.PAM_str)]), seqs[1])
        self.assertEqual('>' + sites[1].label, seqs[2])
        self.assertEqual('CGCN' + reverse_complement(sites[1].sequence[:-len(self.NGCG_PAM.PAM_str)]), seqs[3])
        
    def test_getBowtieOptions(self):
        bowtieOptions = self.NGCG_PAM.getBowtieOptions(2, 12, 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l16")
        self.assertEqual(bowtieOptions[5], "-e150")
        
        bowtieOptions = self.NGCG_PAM.getBowtieOptions(0, 12, 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n1")
        self.assertEqual(bowtieOptions[4], "-l16")
        self.assertEqual(bowtieOptions[5], "-e150")
        
        bowtieOptions = self.NGCG_PAM.getBowtieOptions('NA', 'NA', 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n2")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e150")
        

    def test_isBowtieHitConsistent(self):
        
        self.assertTrue(self.NGCG_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '3:?>N']))
        self.assertTrue(self.NGCG_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '12:C>G']))
        self.assertFalse(self.NGCG_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '1:?>G,2:G>N,15:A>G,18:C>G,21:A>T']))
        self.assertFalse(self.NGCG_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:?>C']))
        self.assertFalse(self.NGCG_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '2:?>C']))

if __name__ == "__main__":
    unittest.main()