'''
Created on Jul 23, 2018

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.sequenceMethods import reverse_complement

class TestPAM_NAAAAT(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('AAAAATTCAAAGTGAACGAG', 'AAAAATTCAAAGTGAACGAGAAAAAC', 0, '-', '', '')
        self.candidates.add('CATAGATCATGGAACTAGTA', 'CATAGATCATGGAACTAGTACAAAAC', 0, '+', '', '')

        self.NAAAAC_PAM = pam.factory("NAAAAC")

    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        
        sites = self.candidates.getSitesSorted()
        
        seqs = self.NAAAAC_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        
        self.assertEqual(2*len(sites)+1, len(seqs))
        self.assertEqual('>' + sites[0].label, seqs[0])
        self.assertEqual('GTTTTN' + reverse_complement(sites[0].sequence[:-len(self.NAAAAC_PAM.PAM_str)]), seqs[1])
        self.assertEqual('>' + sites[1].label, seqs[2])
        self.assertEqual('GTTTTN' + reverse_complement(sites[1].sequence[:-len(self.NAAAAC_PAM.PAM_str)]), seqs[3])
        
    def test_getBowtieOptions(self):
        
        bowtieOptions = self.NAAAAC_PAM.getBowtieOptions('NA', 'NA', 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n0")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e150")
        

    def test_isBowtieHitConsistent(self):
        
        self.assertTrue(self.NAAAAC_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '5:?>N']))
        self.assertTrue(self.NAAAAC_PAM.isBowtieHitConsistent(['', '', '', '', '', '', '', '12:C>G']))

if __name__ == "__main__":
    unittest.main()