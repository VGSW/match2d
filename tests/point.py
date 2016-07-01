import os
import sys

p0 = __file__             # relative path of this module (python >= 2.3)
p1 = os.path.abspath(p0)  # make path absolute
p2 = os.path.dirname(p1)  # current dir path
pp = os.path.dirname(p2)  # parent path
sys.path.insert(1, pp)    # insert parent directly after this directory

import unittest
from optparse import OptionParser

from match2d import Point

class TestMatch2D (unittest.TestCase):
    # def setUp (self):
    # def tearDown (self):

    def test01 (self):
        p00 = Point (x = 0, y = 0)
        p22 = Point (x = 2, y = 2)
        p55 = Point (x = 5, y = 5)
        p77 = Point (x = 7, y = 7)

        self.assertTrue ( p00.left_of (p22) )
        self.assertTrue ( p77.right_of (p00) )
        self.assertTrue ( p22.above_of (p55) )
        self.assertTrue ( p77.below_of (p22) )

        self.assertFalse ( p22.left_of (p00) )
        self.assertFalse ( p00.right_of (p77) )
        self.assertFalse ( p55.above_of (p22) )
        self.assertFalse ( p22.below_of (p77) )

if __name__ == '__main__':
    unittest.main()
