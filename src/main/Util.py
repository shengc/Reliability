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

from __future__ import division
import re
import logging as log

class Util(object):
    '''
    classdocs
    '''

    def __init__(self):
        raise Exception("cannot be instantialized!")
    
    @staticmethod
    def __import_data_as_list(a):
        # so an object observed by only one observer will be ignored!
        return filter(lambda x: len(x) > 1, 
                      [[tuple(sorted(y.split(",") if y != "" else [])) for y in re.findall("\[(.*?)\]", x)] for x in a.split(";") if x != ''])
    
    @staticmethod
    def read_data(filepath):
        with open(filepath) as fin:
            lines = []
            for line in fin:
                if line.strip().startswith("#"): continue
                if not line.strip(): continue
                lines.append(line.strip())
        
        lines = ''.join(lines)
        log.debug("lines = {0}".format(lines))
        return [Util.__import_data_as_list(x) for x in re.findall('\{(.+?)\}', lines)]
    
    @staticmethod
    def flat_case_data(data):
        """
        This should only be used to flattern a case data
        """
        def uniq_add(aList, item):
            if item not in aList: aList.append(item)
            else: pass
            return aList
        
        return reduce(uniq_add, [[]] + [l for ll in data for l in ll])
    
    @staticmethod
    def get_data_item(flat_data):
        """
        get the list of all unique single data items
        """
        all_items = [x for f in flat_data for x in f]
        seen = set()
        results = []
        for x in all_items:
            if x in seen: continue
            else:
                seen.add(x)
                results.append(x)
        return results if () not in flat_data else [()] + results
    
    @staticmethod
    def get_data_item_combination(data_item):
        """
        calculated all possible combinations of single data items
        """
        starts = [d for d in data_item if d != ()]
        
        def p(S, x):
            return [(x,)] if len(S) == 0 else (S + [(x,)] + [tuple(sorted(y + (x,))) for y in S])
        
        S = []
        for s in starts: S = p(S, s)
        if () in data_item: S.append(())
        return S
    
    @staticmethod
    def list_item_count(l, x):
        """
        @param l: a list
        @param x: an item
        @return: the number of counts that x in l  
        """
        
        return len([y for y in l if y == x])
    
    @staticmethod
    def coincidence(l, x, y):
        """
        @param l: a list
        @param x: an item
        @param y; an item (could be equal to x)
        
        @return: the coincidence of x and y in l  
        """
        
        lminus = l[:]
        lminus.remove(x)
        return Util.list_item_count(l, x) * (Util.list_item_count(lminus, y) / (len(l) - 1))
    
    @staticmethod
    def distance(x, y):
        """
        @param x: a multi-value item in tuple
        @param y: a multi-value item in tuple
        
        @return: distance between these two items 
        """
        def intersection(x, y):
            """
            @return: number of items shared by x and y
            """
            return [xx for xx in x if xx in y]
        
        numerator = len(intersection(x, y))
        denominator = len(x) + len(y)
        
        return (1 - 2 * numerator / denominator) if (numerator != 0 or denominator != 0) else 0
    
    @staticmethod
    def prod(x):
        """
        @param x: a list of numbers 
        """
        return 1 if len(x) == 0 else reduce(lambda a, b: a * b, x) 
