'''
Created on Jul 23, 2018

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.sequenceMethods import reverse_complement

class TestPAM_NGG(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('GTGTGAAGCGAAGACAGAGA', 'GTGTGAAGCGAAGACAGAGATGG', 0, '-', '', '')
        self.candidates.add('TAGTGTGCAAAAGCAGCAAC', 'TAGTGTGCAAAAGCAGCAACTGG', 0, '+', '', '')
        
        self.NGG_PAM = pam.factory("NGG")

    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        
        sites = self.candidates.getSitesSorted()
        
        seqs = self.NGG_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        
        self.assertEqual(2*len(sites)+1, len(seqs))
        self.assertEqual('>' + sites[0].label, seqs[0])
        self.assertEqual('CCN' + reverse_complement(sites[0].sequence[:-len(self.NGG_PAM.PAM_str)]), seqs[1])
        self.assertEqual('>' + sites[1].label, seqs[2])
        self.assertEqual('CCN' + reverse_complement(sites[1].sequence[:-len(self.NGG_PAM.PAM_str)]), seqs[3])
        
    def test_getBowtieOptions(self):
        bowtieOptions = self.NGG_PAM.getBowtieOptions(2, 12, 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l15")
        self.assertEqual(bowtieOptions[5], "-e150")
        
        bowtieOptions = self.NGG_PAM.getBowtieOptions('NA', 'NA', 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e150")
        

    def test_isBowtieHitConsistent(self):
        
        self.assertTrue(self.NGG_PAM.isBowtieHitConsistent(['0', '+', 'scaffold8133', '258', 'CCNTCTCTGTCTTCGCTTCACAC', 'IIIIIIIIIIIIIIIIIIIIIII', '0', '2:A>N']))
        self.assertTrue(self.NGG_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '12:C>G']))
        self.assertFalse(self.NGG_PAM.isBowtieHitConsistent(['0', '-', 'chr17', '22534746', 'GTGTGAAGCGAAGACAGAGANGG', 'IIIIIIIIIIIIIIIIIIIIIII', '0', '1:A>G,2:G>N,15:A>G,18:C>G,21:A>T']))
        self.assertFalse(self.NGG_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '0:T>C']))

if __name__ == "__main__":
    unittest.main()