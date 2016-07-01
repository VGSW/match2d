import os
import sys

p0 = __file__             # relative path of this module (python >= 2.3)
p1 = os.path.abspath(p0)  # make path absolute
p2 = os.path.dirname(p1)  # current dir path
pp = os.path.dirname(p2)  # parent path
sys.path.insert(1, pp)    # insert parent directly after this directory

import unittest

from match2d import Landscape2D
from match2d import Bug2D


fn_name = sys._getframe().f_code.co_name
print "\nWARNING: %s takes ~20 secs on a i3-2310M CPU @ 2.10GHz with 4 cores and uses about 70 %% of 4 gb of ram\n" % fn_name

landscape = Landscape2D (filename = './landscape20.txt')
bug1 = Bug2D (filename = './bug20.txt')
landscape.populate (thing = bug1, remove_overlaps=False)

print 'landscape.population: %s' % landscape.population
print 'landscape.count_overlaps: %s' % landscape.count_overlaps
