#!/usr/bin/env python2

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

class TestMatch2D (unittest.TestCase):
    # def setUp (self):
    # def tearDown (self):

    def test200 (self):
        # fn_name = sys._getframe().f_code.co_name
        # print "\nWARNING: %s takes ~20 secs on a i3-2310M CPU @ 2.10GHz with 4 cores and uses about 70 %% of 4 gb of ram\n" % fn_name
        # good news everybody: this is by far not as expensive any more as it used to be
        # using bounding boxes when checking overlapping really helped!

        landscape = Landscape2D (filename = './landscape20.txt')
        bug1 = Bug2D (filename = './bug20.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (2, len (landscape.population))
        self.assertEquals (0, landscape.count_overlaps)

if __name__ == '__main__':
    unittest.main()
