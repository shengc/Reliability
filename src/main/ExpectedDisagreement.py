'''
Created on Jun 6, 2012

@author: shengcer
'''

from __future__ import division
from main.Util import Util

class ExpectedDisagreement(object):
    
    def __init__(self, observed_disagreement, ock):
        self.od = observed_disagreement
        self.ock = ock
        self.data_item = Util.get_data_item(self.od.flat_data)
        self.data_combinations = Util.get_data_item_combination(self.data_item)
    
    def get_num_p(self):
        p = {}
        for k in self.od.flat_data:
            numK = len(k)
            if not p.has_key(numK):
                p[numK] = 0
            p[numK] += sum([self.ock[k][k2] for k2 in self.od.flat_data])
        
        ndotdot = sum([v for v in p.itervalues()])
        return dict([(k, v / ndotdot) for k, v in p.iteritems()])
    
    def get_single_item_n(self):
        n = dict([(d, 0) for d in self.data_item])
        for multi_item in [d for case in self.od.data for d in case]:
            if multi_item == () and () in self.data_item:
                n[multi_item] += 1
            else:
                for item in multi_item:
                    if n.has_key(item): n[item] += 1
        return n
    
    def create_eck(self, n):
        """
        @param n: get single data item frequency 
        """
        eck = {}.fromkeys(self.data_combinations)
        for key in self.data_combinations:
            eck[key] = {}
        
        data_combinations2 = self.data_combinations[:]
        for k1 in self.data_combinations:
            for k2 in data_combinations2:
                if k1 == () and k2 == ():
                    eck[k1][k2] = n[()] * (n[()] - 1)
                elif k1 == ():
                    eck[k1][k2] = n[()] * Util.prod([n[x] for x in k2])
                elif k2 == ():
                    eck[k1][k2] = Util.prod([n[x] for x in k1]) * n[()]
                else:
                    eck[k1][k2] = Util.prod([n[x] for x in k1]) *  Util.prod([(n[x] - 1) if x in k1 else n[x] for x in k2])
            data_combinations2.remove(k1)
            for k3 in data_combinations2:
                eck[k3][k1] = eck[k1][k3]
        
        return eck
    
    def get_ways_of_pair(self, eck):
        num_data_combinations = list(set([len(k) for k in self.data_combinations]))
        denominator = dict([(k, {}) for k in num_data_combinations])
        
        num_data_combinations2 = num_data_combinations[:]
        for n1 in num_data_combinations:
            for n2 in num_data_combinations2:
                denominator[n1][n2] = sum(
                                          [sum(
                                               [eck[k1][k2] for k2 in eck.iterkeys() if len(k2) == n2]
                                               ) for k1 in eck.iterkeys() if len(k1) == n1]
                                          )
            num_data_combinations2.remove(n1)
            for n3 in num_data_combinations2:
                denominator[n3][n1] = denominator[n1][n3]
                 
        return denominator
    
    def get_single_case_ed(self, item1, item2, p, n, d):
        """
        @param item1: multi-value item1
        @param item2: multi-value item2
        @param p: output of get_num_p
        @param n: output of get_single_item_n
        @param d: output of get_ways_of_pair
        
        @return: expected disagreement of item1 and item2 (note: this is not symmetric, i.e., get_single_case_ed(item1, item2) != get_single_case_ed(item2, item1)
        """
        def get_complementary_set(t):
            return [x for x in n.iterkeys() if x not in t]
        
        def intersection(t, s):
            return [tt for tt in t if tt in s]
        
        if not p.has_key(len(item1)):
            return 0
        else:
            ratio1 = p[len(item1)]
        
        if not p.has_key(len(item2)):
            return 0
        else:
            ratio2 = p[len(item2)]
            
        if d[len(item1)][len(item2)] == 0:
            denominator = 1
        else:
            denominator = d[len(item1)][len(item2)]
        
        if item1 == () and item2 == ():
            numerator = n[()] * (n[()] - 1)
        elif item1 == ():
            numerator = n[()] * Util.prod([n[x] for x in item2])
        elif item2 == ():
            numerator = Util.prod([n[x] for x in item1]) * n[()]
        else: 
            numerator = Util.prod([n[x] for x in item1]) * Util.prod([n[x] for x in intersection(item2, get_complementary_set(item1))]) * Util.prod([(n[x] - 1) for x in intersection(item1, item2)])
        
        delta = Util.distance(item1, item2)
        
        return ratio1 * ratio2 * numerator * delta / denominator
    
    def get_disagreement(self, p, n, d):
        return sum([
                   sum(
                       [self.get_single_case_ed(item1, item2, p, n, d) for item2 in self.data_combinations]
                       ) for item1 in self.data_combinations
                   ])
    
    def get(self):
        p = self.get_num_p()
        n = self.get_single_item_n()
        eck = self.create_eck(n)
        d = self.get_ways_of_pair(eck)
        
        return self.get_disagreement(p, n, d)