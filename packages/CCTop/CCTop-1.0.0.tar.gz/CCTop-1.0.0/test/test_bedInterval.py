'''
Created on Mar 26, 2014

@author: juan
'''
import unittest
from unittest.mock import patch
from unittest.mock import mock_open

from cctop.bedInterval import BedInterval

class TestBedInterval(unittest.TestCase):
    def setUp(self):
        self.exons = BedInterval()
        #bed format indexes
        #it is safe to unordered input
        self.exons.insert('1',30,35,'id1','name1')
        self.exons.insert('1',20,22,'id2','name2')
        self.exons.insert('1',8,15,'id3','name3')
        self.exons.insert('1',47,58,'id4','name4')

    def tearDown(self):
        pass

    def test_closest(self):
        closest = self.exons.closest('1',14,17)
        self.assertEqual(closest,['id3','name3',0])
        closest = self.exons.closest('1',24,26)
        self.assertEqual(closest,['id2','name2',3])
        closest = self.exons.closest('1',41,43)
        self.assertEqual(closest,['id4','name4',5])
        closest = self.exons.closest('2',41,43)
        self.assertEqual(closest,['NA','NA','NA'])

    def test_overlaps(self):
        self.assertTrue(self.exons.overlaps('1',19,21))
        self.assertTrue(self.exons.overlaps('1',13,16))
        self.assertFalse(self.exons.overlaps('2',13,26))
        self.assertFalse(self.exons.overlaps('1',22,27))
        
        
    def test_loadFile(self):
        self.exons = BedInterval()
        with patch('cctop.bedInterval.open', mock_open(read_data='1\t30\t35\tid1\tname1\n1\t20\t22\tid2\tname2\n1\t8\t15\tid3\tname3\n1\t47\t58\tid4\tname4\n')) as m:
            self.exons.loadFile('foo.bed')
            self.test_closest()
            self.test_overlaps()

    #without id nor name
    def test_loadFile2(self):
        self.exons = BedInterval()
        with patch('cctop.bedInterval.open', mock_open(read_data='1\t30\t35\n1\t20\t22\n1\t8\t15\n1\t47\t58\n')) as m:
            self.exons.loadFile('foo.bed')
            with self.assertRaises(TypeError):
                self.test_closest()
            self.test_overlaps()
        
if __name__ == "__main__":
    unittest.main()
