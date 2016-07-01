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

    def test30 (self):
        landscape = Landscape2D (filename = './landscape30.txt')
        bug1 = Bug2D (filename = './bug30.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (3, len (landscape.population))
        self.assertEquals (0, landscape.count_overlaps)

    def test31 (self):
        landscape = Landscape2D (filename = './landscape31.txt')
        bug1 = Bug2D (filename = './bug30.txt')
        landscape.populate (thing = bug1, remove_overlaps=True)
        self.assertEquals (3, len (landscape.population))
        self.assertEquals (1, landscape.count_overlaps)

    def test32 (self):
        landscape = Landscape2D (filename = './landscape31.txt')
        bug1 = Bug2D (filename = './bug30.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (4, len (landscape.population))
        self.assertEquals (1, landscape.count_overlaps)

    def test33 (self):
        landscape = Landscape2D (filename = './landscape33.txt')
        bug1 = Bug2D (filename = './bug33.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (2, len (landscape.population))
        self.assertEquals (1, landscape.count_overlaps)

        landscape = Landscape2D (filename = './landscape33.txt')
        bug1 = Bug2D (filename = './bug33.txt')
        landscape.populate (thing = bug1, remove_overlaps=True)
        self.assertEquals (1, len (landscape.population))
        self.assertEquals (1, landscape.count_overlaps)

    def test34 (self):
        landscape = Landscape2D (filename = './landscape34.txt')
        bug1 = Bug2D (filename = './bug33.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (4, len (landscape.population))
        self.assertEquals (2, landscape.count_overlaps)

        landscape = Landscape2D (filename = './landscape34.txt')
        bug1 = Bug2D (filename = './bug33.txt')
        landscape.populate (thing = bug1, remove_overlaps=True)
        self.assertEquals (2, len (landscape.population))
        self.assertEquals (2, landscape.count_overlaps)

    def test35 (self):
        landscape = Landscape2D (filename = './landscape35.txt')
        bug1 = Bug2D (filename = './bug33.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (2, len (landscape.population))
        self.assertEquals (0, landscape.count_overlaps)

    def test40 (self):
        landscape = Landscape2D (filename = './landscape40.txt')
        bug1 = Bug2D (filename = './bug40.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (2, len (landscape.population))
        self.assertEquals (0, landscape.count_overlaps)

if __name__ == '__main__':
    unittest.main()
