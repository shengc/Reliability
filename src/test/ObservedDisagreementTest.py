'''
   Copyright [2012] [Mianwo]

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at

       http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
'''

import unittest
import os

from main.ObservedDisagreement import ObservedDisagreement
from main.Util import Util

class ObservedDisagreementTest(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        data = Util.read_data(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "music.dat"))[0]
        cls.od = ObservedDisagreement(data)
        cls.ock = cls.od.create_ock()
    
    def test_ock(self):
        print
        print "{0}testing observed coincidence matrix{0}".format("*" * 6)
        print "\t\t\t".join(["Header"] + ["{" + ",".join(dd) + "}" for dd in self.od.flat_data])
        for k1 in self.od.flat_data:
            print "{0}\t\t\t".format(k1),
            for k2 in self.od.flat_data:
                print "{0}\t\t\t".format(self.ock[k1][k2]),
            print
        
        self.assertEqual(self.ock[()][('Jazz',)], 1.0, "ock[{}][{Jazz}] = 1")
        self.assertEqual(self.ock[('Funk', 'Rock')][('Funk', 'Jazz', 'Rock')], 0.5, "ock[(Rock, Funk)][(Rock, Funk, Jazz)] = 0.5")
        self.assertEqual(self.ock[('Funk', 'Rock')][('Funk', 'Jazz', 'Rock')], self.ock[('Funk', 'Jazz', 'Rock')][('Funk', 'Rock')], "ock matrix is symmetric")
        print "{0}tested observed coincidence matrix{0}".format("*" * 6)
        print
    
    def test_disagreement(self):
        print
        print "{0}testing observed disagreement{0}".format("*" * 6)
        print "observed disagreement = {0}".format(self.od.get_disagreement(self.ock))
        self.assertAlmostEqual(self.od.get_disagreement(self.ock), 0.4625, 4, "observed disagreement of music = 0.4625")
        print "{0}tested observed disagreement{0}".format("*" * 6)
        print
