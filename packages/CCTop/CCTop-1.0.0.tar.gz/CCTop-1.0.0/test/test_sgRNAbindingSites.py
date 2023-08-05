'''
Created on Jul 25, 2018

@author: juan
'''
import unittest

from cctop.sgRNAbindingSites import sgRNAbindingSites, sgRNAbindingSite
from cctop.offTarget import Offtarget
from cctop.bedInterval import BedInterval

class Test(unittest.TestCase):


    def test_RankingCandidates(self):
        exons = BedInterval()
        exons.insert( 'chr1', 100, 150, 'gene_id', 'gene_name')
        exons.insert( 'chr2', 200, 250, 'gene_id', 'gene_name')
        exons.insert( 'chr3', 300, 350, 'gene_id', 'gene_name')
        genes = exons
        
        sites = sgRNAbindingSites()
        sites.sites['C1'] = sgRNAbindingSite( 'targetSeqC1', 'sequenceC1', 0, 'strand', 'fwdPrimer', 'revPrimer')
        sites.sites['C1'].label = 'C1'
        ot1 = Offtarget(False, 'chr1', '+', 200, '2:T>N', 'sequence', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        ot1 = Offtarget(False, 'chr2', '+', 50, '2:T>N', 'sequence', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        
        sites.sites['C2'] = sgRNAbindingSite( 'targetSeqC2', 'sequenceC2', 0, 'strand', 'fwdPrimer', 'revPrimer')
        sites.sites['C2'].label = 'C2'
        ot1 = Offtarget(False, 'chr2', '+', 50, '2:T>N', 'sequence', 20, 3, 12)
        sites.sites['C2'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        ot1 = Offtarget(False, 'chr3', '+', 50, '2:T>N', 'sequence', 20, 3, 12)
        sites.sites['C2'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        
        sites.sites['C3'] = sgRNAbindingSite( 'targetSeqC3', 'sequenceC3', 0, 'strand', 'fwdPrimer', 'revPrimer')
        sites.sites['C3'].label = 'C3'
        ot1 = Offtarget(False, 'chr1', '+', 200, '2:N>T', 'sequence', 20, 3, 12)
        sites.sites['C3'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        
        sites.scaleScoreAndRelabel()
        self.assertEqual(sites.getSite('T1').sequence, 'sequenceC3')
        self.assertEqual(sites.getSite('T2').sequence, 'sequenceC1')
        self.assertEqual(sites.getSite('T3').sequence, 'sequenceC2')
        
    def test_scaleScoreAndRelabel(self):
        sites = sgRNAbindingSites()
        sites.sites['C1'] = sgRNAbindingSite( 'targetSeqC1', 'sequenceC1', 0, 'strand', 'fwdPrimer', 'revPrimer')
        sites.sites['C1'].label = 'C1'
        sites.sites['C1'].score = 406
        sites.sites['C2'] = sgRNAbindingSite( 'targetSeqC2', 'sequenceC2', 0, 'strand', 'fwdPrimer', 'revPrimer')
        sites.sites['C2'].label = 'C2'
        sites.sites['C2'].score = 248
        sites.sites['C3'] = sgRNAbindingSite( 'targetSeqC3', 'sequenceC3', 0, 'strand', 'fwdPrimer', 'revPrimer')
        sites.sites['C3'].label = 'C3'
        sites.sites['C3'].score = 724
        
        sites.scaleScoreAndRelabel()
        self.assertEqual(sites.getSite('T1').label, 'T1')
        self.assertEqual(sites.getSite('T1').sequence, 'sequenceC3')
        self.assertEqual(sites.getSite('T1').score, 1000)
        self.assertEqual(sites.getSite('T2').label, 'T2')
        self.assertAlmostEqual(sites.getSite('T2').score, 331.932773,3)
        self.assertEqual(sites.getSite('T2').sequence, 'sequenceC1')
        self.assertEqual(sites.getSite('T3').label, 'T3')
        self.assertEqual(sites.getSite('T3').score, 0)
        self.assertEqual(sites.getSite('T3').sequence, 'sequenceC2')

    def test_sortOffTargets(self):
        exons = BedInterval()
        exons.insert( 'chr1', 100, 150, 'gene_id', 'gene_name')
        exons.insert( 'chr2', 200, 250, 'gene_id', 'gene_name')
        exons.insert( 'chr3', 300, 350, 'gene_id', 'gene_name')
        genes = exons
        
        sites = sgRNAbindingSites()
        sites.sites['C1'] = sgRNAbindingSite( 'targetSeqC1', 'sequenceC1', 0, 'strand', 'fwdPrimer', 'revPrimer')
        sites.sites['C1'].label = 'C1'
        ot1 = Offtarget(False, 'chr2', '+', 400, '3:T>A', 'CCNAAAAAAAAAAAAAAAAAAAA', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        ot1 = Offtarget(False, 'chr3', '+', 50, '4:G>C', 'CCNCCCCCCCCCCCCCCCCCCCC', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        ot1 = Offtarget(False, 'chr2', '+', 1480, '3:C>G', 'CCNGGGGGGGGGGGGGGGGGGGG', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        
        sites.sortOffTargets()
        self.assertLess(sites.sites['C1'].offTargets[0].score, sites.sites['C1'].offTargets[1].score)
        self.assertEqual(sites.sites['C1'].offTargets[1].score, sites.sites['C1'].offTargets[2].score)
        self.assertLess(sites.sites['C1'].offTargets[1].distance, sites.sites['C1'].offTargets[2].distance)
        
        self.assertEqual(sites.sites['C1'].offTargets[0].sequence, 'GGGGGGGGGGGGGGGGGGCGNGG')
        self.assertEqual(sites.sites['C1'].offTargets[1].sequence, 'TTTTTTTTTTTTTTTTTTTANGG')
        self.assertEqual(sites.sites['C1'].offTargets[2].sequence, 'CCCCCCCCCCCCCCCCCCCGNGG')
        
        #Now with gene info, but some with no hits (comparing same score)
        exons = BedInterval()
        exons.insert( 'chr4', 100, 150, 'gene_id', 'gene_name')
        exons.insert( 'chr4', 200, 250, 'gene_id', 'gene_name')
        exons.insert( 'chr4', 300, 350, 'gene_id', 'gene_name')
        genes = exons
        sites = sgRNAbindingSites()
        sites.sites['C1'] = sgRNAbindingSite( 'targetSeqC1', 'sequenceC1', 0, 'strand', 'fwdPrimer', 'revPrimer')
        sites.sites['C1'].label = 'C1'
        ot1 = Offtarget(False, 'chr4', '+', 400, '3:T>A', 'CCNAAAAAAAAAAAAAAAAAAAA', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        ot1 = Offtarget(False, 'chr3', '+', 50, '4:G>C', 'CCNCCCCCCCCCCCCCCCCCCCC', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        ot1 = Offtarget(False, 'chr2', '+', 1480, '3:C>G', 'CCNGGGGGGGGGGGGGGGGGGGG', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        
        sites.sortOffTargets()
        self.assertLess(sites.sites['C1'].offTargets[0].score, sites.sites['C1'].offTargets[1].score)
        self.assertEqual(sites.sites['C1'].offTargets[1].score, sites.sites['C1'].offTargets[2].score)
        
        self.assertEqual(sites.sites['C1'].offTargets[0].sequence, 'GGGGGGGGGGGGGGGGGGCGNGG')
        self.assertEqual(sites.sites['C1'].offTargets[1].sequence, 'CCCCCCCCCCCCCCCCCCCGNGG')
        self.assertEqual(sites.sites['C1'].offTargets[2].sequence, 'TTTTTTTTTTTTTTTTTTTANGG')
        
        #Now without gene info
        exons = BedInterval()
        genes = exons
        sites = sgRNAbindingSites()
        sites.sites['C1'] = sgRNAbindingSite( 'targetSeqC1', 'sequenceC1', 0, 'strand', 'fwdPrimer', 'revPrimer')
        sites.sites['C1'].label = 'C1'
        ot1 = Offtarget(False, 'chr2', '+', 400, '3:T>A', 'CCNAAAAAAAAAAAAAAAAAAAA', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        ot1 = Offtarget(False, 'chr3', '+', 50, '4:G>C', 'CCNCCCCCCCCCCCCCCCCCCCC', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        ot1 = Offtarget(False, 'chr2', '+', 1480, '3:C>G', 'CCNGGGGGGGGGGGGGGGGGGGG', 20, 3, 12)
        sites.sites['C1'].addOffTarget(ot1,['chr1',200,230],exons,genes)
        
        sites.sortOffTargets()
        self.assertLess(sites.sites['C1'].offTargets[0].score, sites.sites['C1'].offTargets[1].score)
        self.assertEqual(sites.sites['C1'].offTargets[1].score, sites.sites['C1'].offTargets[2].score)
        self.assertEqual(sites.sites['C1'].offTargets[1].distance, sites.sites['C1'].offTargets[2].distance)
        
        self.assertEqual(sites.sites['C1'].offTargets[0].sequence, 'GGGGGGGGGGGGGGGGGGCGNGG')
        self.assertEqual(sites.sites['C1'].offTargets[1].sequence, 'TTTTTTTTTTTTTTTTTTTANGG')
        self.assertEqual(sites.sites['C1'].offTargets[2].sequence, 'CCCCCCCCCCCCCCCCCCCGNGG')
        

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.test_scaleScoreAndRelabel']
    unittest.main()
