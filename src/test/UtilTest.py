'''
Created on Jun 3, 2012

@author: shengcer
'''

import unittest
import os

from main.Util import Util

class UtilTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        cls.filepath = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "music.dat")
    
    def test_util_init(self):
        self.assertRaises(Exception, Util)
        
    def test_prod(self):
        print
        print "{0}testing multiplication of list of numbers{0}".format("*" * 6)
        d = []
        m = Util.prod(d)
        print "prod({{}}) = {0}".format(m)
        self.assertEqual(m, 1, "prod({}) = 1")
        d = [2]
        m = Util.prod(d)
        print "prod({{2}}) = {0}".format(m)
        self.assertEqual(m, 2, "prod({2}) = 2")
        d = [1, 2, 3, 4]
        m = Util.prod(d)
        print "prod({{1,2,3,4}}) = {0}".format(m)
        self.assertEqual(m, 24, "m({{1,2,3,4}}) = 24")
        print "{0}tested multiplication of list of numbers{0}".format("*" * 6)
        print
        
    def test_read_data(self):
        print
        print "{0}testing read data{0}".format("*" * 6) 
        data = Util.read_data(self.filepath)[0]
        print "data = {0}".format(data)
        self.assertEquals(data, [[("Funk", "Rock"), ("Rock",)], [("Funk", "Jazz", "Rock"), ("Funk",), ("Funk", "Rock")], [(), ("Jazz",), ("Jazz",)]], "data should be read as expected")
        flat_data = Util.flat_case_data(data)
        print "flat_data = {0}".format(flat_data)
        self.assertEquals(flat_data, [('Funk', 'Rock'), ('Rock',), ('Funk', 'Jazz', 'Rock'), ('Funk',), (), ('Jazz',)])
        data_items = Util.get_data_item(flat_data)
        print "data_items={0}".format(data_items)
        self.assertTrue(() in data_items, "empty set should be included in unique single items")
        data_combination = Util.get_data_item_combination(data_items)
        print "data_combination = {0}".format(data_combination)
        print "{0}tested read data{0}".format("*" * 6)
        print
    
    def test_coincidence(self):
        print
        print "{0}testing coincidence{0}".format("*" * 6)
        data = [(), ('Jazz',), ('Jazz',)]
        self.assertEquals(Util.list_item_count(data, ('Jazz', )), 2, "Jazz occures for twice")
        self.assertEquals(Util.coincidence(data, (), ('Jazz',)), 1.0, "coincidence of {} and (Jazz,) is 1")
        self.assertEquals(Util.coincidence(data, ('Jazz', ), ('Jazz',)), 1.0, "coincidence of (Jazz,) and (Jazz,) is 1")
        
        data2 = [('Funk', 'Rock', 'Jazz'), ('Funk',), ('Funk', 'Rock')]
        self.assertEquals(Util.coincidence(data2, ('Funk', ), ('Funk', 'Rock')), 0.5, 'coincidence of (Funk,) and (Funk, Rock) is 0.5')
        self.assertEquals(Util.coincidence(data2, ('Funk', ), ('Funk', 'Rock')), Util.coincidence(data2, ('Funk', 'Rock'), ('Funk',)), 'coincidence is symmetric')
        print "{0}tested coincidence{0}".format("*" * 6)
        print
    
    def test_distance(self):
        print
        print "{0}testing distance{0}".format("*" * 6)
        d1 = ()
        print "distance({{}}, {{}}) = {0}".format(Util.distance(d1, d1))
        self.assertEquals(Util.distance(d1, d1), 0, "distance({Empty}, {Empty}) = 0")
        d2 = ("Funk", "Rock")
        print "distance({{Funk}}, {{Rock}}) = {0}".format(Util.distance(d1, d2))
        self.assertEquals(Util.distance(d1, d2), 1.0, "distance({Empty}, {Rock, Funk}) = 1")
        
        d3 = ("Funk", "Rock")
        d4 = ("Funk", "Jazz", "Rock")
        print "distance({{Funk, Rock}}, {{Funk, Rock, Jazz}}) = {0}".format(Util.distance(d3, d4))      
        self.assertAlmostEqual(Util.distance(d3, d4), 0.2, 5, "distance({Funk, Rock}, {Funk, Rock, Jazz}) = 0.2")
        self.assertEquals(Util.distance(d3, d4), Util.distance(d4, d3), "distance is symmetric")
        print "{0}tested distance{0}".format("*" * 6)
        print