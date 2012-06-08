'''
Created on Jun 6, 2012

@author: shengcer
'''

import unittest
import os

from main.Util import Util
from main.ObservedDisagreement import ObservedDisagreement
from main.ExpectedDisagreement import ExpectedDisagreement

class ExpectedDisagreementTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        data = Util.read_data(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "music.dat"))[0]
        od = ObservedDisagreement(data)
        ock = od.create_ock()
        cls.ed = ExpectedDisagreement(od, ock)
    
    def test_num_p(self):
        print
        print "{0}testing probability for the number of values contained in multi-value item{0}".format("*" * 6)
        p = self.ed.get_num_p()
        print p
        self.assertAlmostEqual(p[0], 0.125, 3, "p[0] = 0.125")
        self.assertAlmostEqual(p[1], 0.5, 1, "p[1] = 0.5")
        self.assertAlmostEqual(p[2], 0.25, 2, "p[2] = 0.25")
        self.assertAlmostEqual(p[3], 0.125, 3, "p[3] = 0.125")
        print "{0}tested probability for the number of values contained in multi-value item{0}".format("*" * 6)
        print
    
    def test_single_item_n(self):
        print
        print "{0}testing frequency of single items{0}".format("*" * 6)
        n = self.ed.get_single_item_n()
        print n
        self.assertDictEqual(n, {(): 1, 'Jazz': 3, 'Funk': 4, 'Rock': 4}, "n = {{}:1, Jazz:2, Funk:4, Rock:4}")
        print "{0}tested frequency of single items{0}".format("*" * 6)
        print
    
    def test_eck(self):
        print
        print "{0}testing expected frequency matrix{0}".format("*" * 6)
        n = self.ed.get_single_item_n()
        eck = self.ed.create_eck(n)
        print "\t\t".join(["header"] + ["(%s)" % (",".join(x)) for x in self.ed.data_combinations])
        for k in self.ed.data_combinations:
            print "\t\t".join(["(%s)" % (",".join(k))] + [str(eck[k][x]) for x in self.ed.data_combinations]) 
        
        self.assertDictEqual(eck[()], {(): 0, ('Funk',):4, 
                                       ("Rock",):4, ('Funk', 'Rock'):16, 
                                       ('Jazz',):3, ('Funk', 'Jazz'):12, 
                                       ('Jazz', 'Rock'):12, ('Funk', 'Jazz', 'Rock'):48}, "eck(()) should be right")
        self.assertDictEqual(eck[('Funk', 'Rock')], {('Funk',):48, ('Rock',):48,
                                                     ('Funk', 'Rock'):144, ('Jazz',):48, 
                                                     ('Funk', 'Jazz'):144, ('Jazz', 'Rock'):144,
                                                     ('Funk', 'Jazz', 'Rock'):432, (): 16}, "eck({Rock, Funk}) should be right")
        self.assertEquals(eck[('Rock',)][('Funk',)], eck[('Rock',)][('Funk',)], "eck should be symmetric")
        self.assertEquals(eck[('Funk', 'Jazz')][('Funk', 'Jazz', 'Rock')], eck[('Funk', 'Jazz', 'Rock')][('Funk', 'Jazz')], "eck should still be symmetric")
        
        print "{0}testing number of ways of pairing two labels{0}".format("*" * 6)
        denominator_matrix = self.ed.get_ways_of_pair(eck)
        denominator_keys = sorted(denominator_matrix.keys())
        print "\t\t".join(['header'] + [str(n) for n in denominator_keys])
        for d_key in denominator_keys:
            print "\t\t".join([str(d_key)] + [str(denominator_matrix[d_key][x]) for x in denominator_matrix[d_key]])
        
        print "{0}tested number of ways of pairing two labels{0}".format("*" * 6)
        print "{0}tested expected frequency matrix{0}".format("*" * 6)
        print  
    
    def test_ed(self):
        p = self.ed.get_num_p()
        n = self.ed.get_single_item_n()
        eck = self.ed.create_eck(n)
        d = self.ed.get_ways_of_pair(eck)
        
        print self.ed.get_single_case_ed(('Funk', 'Jazz'), ('Funk', 'Jazz', 'Rock'), p, n, d)
        print self.ed.get_disagreement(p, n, d)