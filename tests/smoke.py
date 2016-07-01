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

from optparse import OptionParser

class TestMatch2D (unittest.TestCase):
    # def setUp (self):
    # def tearDown (self):

    def test01 (self):
        landscape = Landscape2D (filename = './landscape00.txt')
        bug = Bug2D (filename = './bug01.txt')
        self.assertEquals (
            bug.area(),
            [(0, 0), (1, 0), (2, 0), (0, 1), (1, 1), (2, 1), (3, 1), (0, 2), (1, 2), (2, 2)],
        )

    def test01a (self):
        landscape = Landscape2D (filename = './landscape00.txt')
        bug = Bug2D (filename = './bug01.txt')
        bug.move (x = 5, y = 10)
        self.assertEquals (
            bug.area(),
            [(5, 10), (6, 10), (7, 10), (5, 11), (6, 11), (7, 11), (8, 11), (5, 12), (6, 12), (7, 12)],
        )

    def test02 (self):
        landscape = Landscape2D (filename = './landscape02.txt')
        bug = Bug2D (filename = './bug01.txt')
        self.assertEquals (
            landscape.count_those (thing = bug),
            4,
        )

    def test03 (self):
        landscape = Landscape2D (filename = './landscape02.txt')
        bug = Bug2D (filename = './bug01.txt')
        self.assertEquals (
            landscape.find (thing = bug),
            [(4, 1), (18, 3), (35, 5), (44, 5)],
        )

    def test04 (self):
        bug1 = Bug2D (filename = './bug01.txt')
        bug2 = Bug2D (filename = './bug02.txt')
        self.assertTrue (bug1 in bug2)

    def test05 (self):
        landscape = Landscape2D (filename = './landscape02.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1)
        self.assertEquals (0, landscape.count_overlaps)

    def test06 (self):
        landscape = Landscape2D (filename = './landscape03.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (2, len (landscape.population))
        self.assertEquals (1, landscape.count_overlaps)

    def test07 (self):
        landscape = Landscape2D (filename = './landscape03.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=True)
        self.assertEquals (1, len (landscape.population))
        self.assertEquals (1, landscape.count_overlaps)

    def test08 (self):
        landscape = Landscape2D (filename = './landscape04.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=True)
        self.assertEquals (9, len (landscape.population))
        self.assertEquals (0, landscape.count_overlaps)

    def test09 (self):
        landscape = Landscape2D (filename = './landscape05.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (12, len (landscape.population))
        self.assertEquals (3, landscape.count_overlaps)

    def test10 (self):
        landscape = Landscape2D (filename = './landscape05.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=True)
        self.assertEquals (9, len (landscape.population))
        self.assertEquals (3, landscape.count_overlaps)

    def test11 (self):
        landscape = Landscape2D (filename = './landscape06.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (11, len (landscape.population))
        self.assertEquals (3, landscape.count_overlaps)

    def test12 (self):
        # test bounds
        landscape = Landscape2D (filename = './landscape08.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (2, len (landscape.population))
        self.assertEquals (0, landscape.count_overlaps)

    def test13 (self):
        landscape = Landscape2D (filename = './landscape07.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (1, len (landscape.population))
        self.assertEquals (0, landscape.count_overlaps)

    def test14 (self):
        # test bounds and overlappings

        landscape = Landscape2D (filename = './landscape09.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=True)
        self.assertEquals (2, len (landscape.population))
        self.assertEquals (0, landscape.count_overlaps)

        landscape = Landscape2D (filename = './landscape09a.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=True)
        self.assertEquals (1, len (landscape.population))
        self.assertEquals (1, landscape.count_overlaps)

        landscape = Landscape2D (filename = './landscape09a.txt')
        bug1 = Bug2D (filename = './bug01.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (2, len (landscape.population))
        self.assertEquals (1, landscape.count_overlaps)

    def test100 (self):
        landscape = Landscape2D (filename = './landscape10.txt')
        bug1 = Bug2D (filename = './bug10.txt')
        landscape.populate (thing = bug1, remove_overlaps=False)
        self.assertEquals (1, len (landscape.population))
        self.assertEquals (0, landscape.count_overlaps)

if __name__ == '__main__':
    unittest.main()
