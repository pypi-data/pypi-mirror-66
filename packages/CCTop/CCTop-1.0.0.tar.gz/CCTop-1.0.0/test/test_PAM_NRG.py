'''
Created on Jul 23, 2018

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.sequenceMethods import reverse_complement

class TestPAM_NRG(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('TGACATAAATAGATTTTT', 'TGACATAAATAGATTTTTGGAAG', 0, '-', '', '')
        self.candidates.add('GAGGGAGGCTGAGATGGA', 'GAGGGAGGCTGAGATGGATGAGG', 0, '+', '', '')
        
        self.NRG_PAM = pam.factory("NRG")


    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        sites = self.candidates.getSitesSorted()
        
        seqs = self.NRG_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        self.assertEqual(4*len(self.candidates.sites)+1, len(seqs))
        self.assertEqual('>'+sites[0].label, seqs[0])
        self.assertEqual('CCN'+reverse_complement(sites[0].sequence[:-len(self.NRG_PAM.PAM_str)]), seqs[1])
        self.assertEqual('>'+sites[0].label, seqs[2])
        self.assertEqual('CTN'+reverse_complement(sites[0].sequence[:-len(self.NRG_PAM.PAM_str)]), seqs[3])
        self.assertEqual('>'+sites[1].label, seqs[4])
        self.assertEqual('CCN'+reverse_complement(sites[1].sequence[:-len(self.NRG_PAM.PAM_str)]), seqs[5])
        self.assertEqual('>'+sites[1].label, seqs[6])
        self.assertEqual('CTN'+reverse_complement(sites[1].sequence[:-len(self.NRG_PAM.PAM_str)]), seqs[7])

    def test_getBowtieOptions(self):
        bowtieOptions = self.NRG_PAM.getBowtieOptions(2, 12, 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l15")
        self.assertEqual(bowtieOptions[5], "-e150")
                

    def test_isBowtieHitConsistent(self):
        self.assertTrue(self.NRG_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '2:A>N']))
        self.assertTrue(self.NRG_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '12:?>?']))
        self.assertFalse(self.NRG_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:?>?,2:...']))
        self.assertFalse(self.NRG_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '0:?>?']))

if __name__ == "__main__":
    unittest.main()