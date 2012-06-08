'''
Created on Jun 3, 2012

@author: shengcer
'''

from __future__ import division
from main.Util import Util

class ObservedDisagreement(object):

    def __init__(self, data):
        '''
        @param data: a list of lists. Each sublist stands for the observations for a particular object
        '''
        
        assert isinstance(data, list) and isinstance(data[0], list) and isinstance(data[0][0], tuple) and isinstance(data[0][0][0], str)
        self.data = data
        self.flat_data = Util.flat_case_data(data)

    def create_ock(self):
        ock = {}.fromkeys(self.flat_data)
        for key in ock.iterkeys():
            ock[key] = {}
        
        flat_data_2 = self.flat_data[:]
        for obs in self.flat_data:
            for obs2 in flat_data_2:
                ock[obs][obs2] = sum([
                                      Util.coincidence(d, obs, obs2) for d in self.data
                                      if obs in d and obs2 in d
                                      ])
            flat_data_2.remove(obs)
            for obs2 in flat_data_2:
                # copy the symmetric items
                ock[obs2][obs] = ock[obs][obs2]
        return ock

    def get_disagreement(self, ock):
        ndotdot = sum([sum([ock[f1][f2] for f2 in self.flat_data]) for f1 in self.flat_data])
        distanced_ock_sum = sum([sum([ock[f1][f2] * Util.distance(f1, f2) for f2 in self.flat_data]) for f1 in self.flat_data])
        
        return distanced_ock_sum / ndotdot
    
    def get(self):
        ock = self.create_ock()
        return self.get_disagreement(ock)

if __name__ == "__main__":
    import os
    
    data = Util.read_data(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "data", "music.dat"))[0]
    od = ObservedDisagreement(data)
    