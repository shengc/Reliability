'''
Created on Jun 8, 2012

@author: shengcer
'''

from __future__ import division
import os
import sys

from main.Util import Util
from main.ObservedDisagreement import ObservedDisagreement
from main.ExpectedDisagreement import ExpectedDisagreement

base_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data")

def main():
    if len(sys.argv) != 2:
        print "python Main %s"
        sys.exit(-1)
    
    data = Util.read_data(os.path.join(base_path, sys.argv[1]))
    
    for c, d in enumerate(data):
        od = ObservedDisagreement(d)
        ock = od.create_ock()
        od_value = od.get_disagreement(ock)
        
        ed = ExpectedDisagreement(od, ock)
        ed_value = ed.get()
    
        alpha = 1 - od_value / ed_value
        print "data[{0}] = {1}".format(c, d)
        print "alpha = {0}".format(alpha)
    
if __name__ == '__main__':
    main()