#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 24 12:02:26 2020

@author: juan
"""

import unittest

from unittest.mock import patch

from cctop.CCTop import getSeqCoords,getFormattedCoords,getPlainOTPosition,addCandidateTargets,findOT,validDinucleotideIUPAC,validOverhang,readMultiFasta
from cctop import CCTop

from cctop.sgRNAbindingSites import sgRNAbindingSites
from cctop.pam import factory
from cctop.bedInterval import BedInterval

from argparse import ArgumentTypeError

class TestCCTop(unittest.TestCase):
    
    def test_getSeqCoords(self):
        CCTop.runBowtie = unittest.mock.Mock(side_effect=[["0\t+\tchr\t1\tseq\talignment\t0\tmm"],
                                                          ["0\t+\tchr\t4\tseq\talignment\t0\tmm"],
                                                          ["0\t+\tchr\t404\tseq\talignment\t0\tmm"]])
        seq = "ACGTACGTACGT"
        output1 = getSeqCoords(seq, "bowtiePath", "indexPath")
        CCTop.runBowtie.assert_called_with(['--quiet'], "bowtiePath", "indexPath", ['-c', seq], None)
        self.assertEqual(output1,['chr', 1, 13, '+'])
        
        seq = "ACGTACGTAC"*50
        output2 = getSeqCoords(seq, "bowtiePath", "indexPath")
        CCTop.runBowtie.assert_called_with(['--quiet'], "bowtiePath", "indexPath", ['-c', seq[0:100]], None)
        CCTop.runBowtie.assert_called_with(['--quiet'], "bowtiePath", "indexPath", ['-c', seq[-100:]], None)
        self.assertEqual(output2,['chr', 4, 504, '+'])
        
    
    def test_getFormattedCoords(self):
        self.assertEqual("chr:start-end",getFormattedCoords(['chr','start','end']))
        
    def test_getPlainOTPosition(self):
        self.assertEqual("Exonic",getPlainOTPosition(0,None))
        self.assertEqual("Intronic",getPlainOTPosition(10,True))
        self.assertEqual("Intergenic",getPlainOTPosition(10,False))

    def test_addCandidateTargets(self):
        candidates = sgRNAbindingSites()
        addCandidateTargets(factory("NGG"), 4, "NN", "NN", "ACGTNGGCCCACGT", "+", candidates, "", "")
        self.assertEqual(1,len(candidates.sites))
        addCandidateTargets(factory("NGG"), 4, "NN", "NN", "ACGTGGGCCNACGT", "-", candidates, "", "")
        self.assertEqual(2,len(candidates.sites))
        self.assertEqual("ACGTNGG", candidates.sites["C1"].sequence)
        self.assertEqual("ACGTGGG", candidates.sites["C2"].sequence)
        
        candidates = sgRNAbindingSites()
        addCandidateTargets(factory("TTTN"), 4, "NN", "NN", "TTTNACGTACGTAAAA", "+", candidates, "", "")
        self.assertEqual(1,len(candidates.sites))
        addCandidateTargets(factory("TTTN"), 4, "NN", "NN", "TTTTACGTACGTNAAA", "-", candidates, "", "")
        self.assertEqual(3,len(candidates.sites))
        self.assertEqual("TTTNACGT", candidates.sites["C1"].sequence)
        self.assertEqual("TTTTACGT", candidates.sites["C2"].sequence)
        self.assertEqual("TTTACGTA", candidates.sites["C3"].sequence)
        
    def test_findOT(self):
        candidates = sgRNAbindingSites()
        candidates.add("ACGTACGT", "ACGTACGTGGG", 8, "+", "fwdP", "revP", 2)
        
        # mocking
        CCTop.runBowtie = unittest.mock.Mock()
    
        mock_o = unittest.mock.mock_open()
        mock_o.side_effect = [unittest.mock.mock_open().return_value,
                              unittest.mock.mock_open(read_data="C1\t+\tchr\t1\tsequence\talignment\t0\t2:N>A\n" +
                                                          "C1\t+\tchr\t4\tsequence\talignment\t0\t2:N>A\n" +
                                                          "C1\t+\tchr\t404\tsequence\talignment\t0\t2:N>G,5:A>T").return_value]
        with patch("builtins.open", mock_o):
            findOT(candidates, factory("NGG"), "outputPath", 2, 12, 4, "bowtiePath", "indexPath", ['chr', 72,96], BedInterval(), BedInterval())
        
        mock_o.assert_called_with('outputPath/bowtieOutput', 'r')
        mock_o.assert_any_call('outputPath/bowtieInput.fasta', 'w')
        self.assertEqual(3, len(candidates.getSite("C1").offTargets))

    def test_valid_dinucleotideIUPAC(self):
        self.assertEqual(validDinucleotideIUPAC("AC"),"AC")
        self.assertEqual(validDinucleotideIUPAC("ac"),"AC")
        with self.assertRaises(ArgumentTypeError):
            validDinucleotideIUPAC("acg") # length different than 2
            validDinucleotideIUPAC("ab") # invalid chars

    def test_valid_overhang(self):
        self.assertEqual(validOverhang("ACGT"),"ACGT")
        self.assertEqual(validOverhang("acgt"),"ACGT")
        with self.assertRaises(ArgumentTypeError):
            validOverhang("acgtac") # longer than 5
            validOverhang("abcd") # invalid chars
            
    def test_readMultiFasta(self):
        mockFile = [">h1","ACGT","TGCA",">h2","CGTC","GGAC"]
        rtn = readMultiFasta(mockFile)
        self.assertEqual("h1",rtn[0][0])
        self.assertEqual("ACGTTGCA",rtn[0][1])
        self.assertEqual("h2",rtn[1][0])
        self.assertEqual("CGTCGGAC",rtn[1][1])
        
        mockFile = [""]
        with self.assertRaises(Exception):
            readMultiFasta(mockFile)
            
        mockFile = [">"]
        with self.assertRaises(Exception):
            readMultiFasta(mockFile)
            
        mockFile = [">$"]
        with self.assertRaises(Exception):
            readMultiFasta(mockFile)
            
        mockFile = [">h1","ABCD"]
        with self.assertRaises(Exception):
            readMultiFasta(mockFile)
        
if __name__ == "__main__":
    unittest.main()
