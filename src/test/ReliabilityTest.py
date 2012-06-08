'''
Created on Jun 8, 2012

@author: shengcer
'''

from __future__ import division
from unittest import TestCase
import os

from main.Util import Util
from main.ObservedDisagreement import ObservedDisagreement
from main.ExpectedDisagreement import ExpectedDisagreement

class ReliabilityTest(TestCase):
    
    @classmethod
    def setUpClass(cls):
        base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")
        cls.data = Util.read_data(os.path.join(base_path, "comments.dat"))
        
        print
        print "{0}data{0}".format("*" * 6)
        for c, d in enumerate(cls.data):
            print "data{0}:{1}".format(c, d)
        print "{0}data{0}".format("*" * 6)
        print
    
    def testReliability(self):
        
        print
        print "{0}testing reliability{0}".format("*" * 6)
        for c, d in enumerate(self.data):
            od = ObservedDisagreement(d)
            ock = od.create_ock()
            od_value = od.get()
            ed = ExpectedDisagreement(od, ock)
            ed_value = ed.get()
                        
            reliability = 1 - od_value / ed_value
            print "data{0} reliability = {1}".format(c, reliability)
            
            if c == 0: self.assertAlmostEqual(reliability, 0.947, 3, "reliability[data{0}]={1}".format(c, 0.947))
            elif c == 1: self.assertAlmostEqual(reliability, 0.923, 3, "reliability[data{0}]={1}".format(c, 0.923))
            elif c == 2: self.assertAlmostEqual(reliability, 0.895, 3, "reliability[data{0}]={1}".format(c, 0.895))
            elif c == 3: self.assertAlmostEqual(reliability, 0.716, 3, "reliability[data{0}]={1}".format(c, 0.716))
            elif c == 4: self.assertAlmostEqual(reliability, 0.554, 3, "reliability[data{0}]={1}".format(c, 0.554))
        
        print "{0}tested reliability{0}".format("*" * 6)
        print

