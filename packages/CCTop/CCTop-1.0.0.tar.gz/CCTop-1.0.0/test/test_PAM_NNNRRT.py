'''
Created on Jul 23, 2018

@author: juan
'''
import unittest

import cctop.pam as pam
from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.sequenceMethods import reverse_complement

class TestPAM_NNNRRT(unittest.TestCase):


    def setUp(self):
        
        self.candidates = sgRNAbindingSites()
        self.candidates.add('CTTGACATAAATAGATTTTT', 'CTTGACATAAATAGATTTTTGGAAGT', 0, '-', '', '')
        self.candidates.add('CTGAGGGAGGCTGAGATGGA', 'CTGAGGGAGGCTGAGATGGATGAGGT', 0, '+', '', '')
        
        self.NNNRRT_PAM = pam.factory("NNNRRT")


    def tearDown(self):
        pass
    
    def test_getSequencesforBowtie(self):
        sites = self.candidates.getSitesSorted()
        
        seqs = self.NNNRRT_PAM.getSequencesforBowtie(sites)
        seqs = seqs.split('\n')
        
        self.assertEqual(4*len(sites)+1, len(seqs))
        self.assertEqual('>C1', seqs[0])
        self.assertEqual('ACNNNN'+reverse_complement(sites[0].sequence[:-len(self.NNNRRT_PAM.PAM_str)]), seqs[1])
        self.assertEqual('>C1', seqs[2])
        self.assertEqual('ATNNNN'+reverse_complement(sites[0].sequence[:-len(self.NNNRRT_PAM.PAM_str)]), seqs[3])
        self.assertEqual('>C2', seqs[4])
        self.assertEqual('ACNNNN'+reverse_complement(sites[1].sequence[:-len(self.NNNRRT_PAM.PAM_str)]), seqs[5])
        self.assertEqual('>C2', seqs[6])
        self.assertEqual('ATNNNN'+reverse_complement(sites[1].sequence[:-len(self.NNNRRT_PAM.PAM_str)]), seqs[7])

    def test_getBowtieOptions(self):
        bowtieOptions = self.NNNRRT_PAM.getBowtieOptions(2, 12, 4)
        
        self.assertEqual(bowtieOptions[0], "-a")
        self.assertEqual(bowtieOptions[1], "--quiet")
        self.assertEqual(bowtieOptions[2], "-y")
        self.assertEqual(bowtieOptions[3], "-n3")
        self.assertEqual(bowtieOptions[4], "-l5")
        self.assertEqual(bowtieOptions[5], "-e240")
        

    def test_isBowtieHitConsistent(self):
        self.assertTrue(self.NNNRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '3:A>N']))
        self.assertTrue(self.NNNRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '12:?>?']))
        self.assertTrue(self.NNNRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:T>G,2:...']))
        self.assertTrue(self.NNNRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:C>G,2:...']))
        self.assertTrue(self.NNNRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '2:A>G,2:...']))
        self.assertTrue(self.NNNRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '2:G>C,2:...']))
        
        
        
        self.assertFalse(self.NNNRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '2:T>G,...']))
        self.assertFalse(self.NNNRRT_PAM.isBowtieHitConsistent(['', '-', '', '', '', '', '', '2:C>G,2:...']))
        self.assertFalse(self.NNNRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:A>G,2:...']))
        self.assertFalse(self.NNNRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '2:G>C,2:...']))
        
        self.assertFalse(self.NNNRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '1:?>?']))
        self.assertFalse(self.NNNRRT_PAM.isBowtieHitConsistent(['', '+', '', '', '', '', '', '0:?>?']))
        #=======================================================================
        # seqs = self.NNNRRT_PAM.getSequencesforBowtie(self.candidates)
        # seqs = seqs.split('\n')
        # 
        # bowtieOptions1 = self.NNNRRT_PAM.getBowtieOptions(2, 12, 4)
        # bowtieOptions1.insert(0,'/home/juan/software/bowtie-0.12.7/bowtie')
        # bowtieOptions1.append('/data/genomes/oryLat2/oryLat2')
        # bowtieOptions1.append('-c')
        # bowtieOptions2 = list(bowtieOptions1)
        # bowtieOptions1.append(seqs[1])
        # bowtieOptions2.append(seqs[3])
        # bowtieOutput = subprocess.check_output(bowtieOptions1).split('\n')
        # bowtieOutput = bowtieOutput + subprocess.check_output(bowtieOptions2).split('\n')
        # 
        # for line in bowtieOutput:
        #     columns = line.split('\t')
        #     self.assertTrue(self.NNNRRT_PAM.isBowtieHitConsistent(columns), "Hit should be consistent with PAM: [" + ', '.join(columns) + "] ")
        #=======================================================================

if __name__ == "__main__":
    unittest.main()