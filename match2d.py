#!/usr/bin/env python2

from optparse import OptionParser
import copy
import sys

#
# TODO
# use Point everywhere

#
def find_all (**kwa):
    """ find sub in string multiple times including overlaps
        returns a list of indices
    """

    string = kwa.get ('string')
    sub    = kwa.get ('sub')
    res    = []

    index = -1
    while index < (len (string) - len(sub)):
        try:
            index = string.index (sub, index+1)
            res.append (index)
        except ValueError:
            break

    return res

class ViewPort (object):
    """ get a cut of a file while moving through it with every call to lines()

        params for init:
            cut_size:  size of the cut (in lines)
            step_size: how many new lines every step. new lines will be appended
                       at the end, the same amount of old lines will be dropped
    """

    def __init__ (self, **kwa):
        self.cut_size  = kwa.get ('cut_size')
        self.step_size = kwa.get ('step_size')
        self.infile    = open (kwa.get ('filename'), 'r')
        self.index     = -1 * self.step_size
        self._lines    = []

        # is there a nice, efficient way for this ?
        self.length = sum ([1 for line in self.infile])
        self.infile.seek (0)

    def lines (self):
        while self.index < self.length:
            i = 0

            if self._lines:
                self._lines = self._lines[self.step_size:]
                i = self.cut_size - self.step_size

            while i < self.cut_size:
                line = self.infile.readline().rstrip()
                self._lines.append (line)
                i += 1

            self.index += self.step_size

            yield self._lines

    def __del__ (self):
        self.infile.close()

class Point (object):
    def __init__ (self, **kwa):
        self.x = kwa.get ('x')
        self.y = kwa.get ('y')

    def left_of (self, other):
        if self.x < other.x:
            return True

    def right_of (self, other):
        if self.x > other.x:
            return True

    def above_of (self, other):
        if self.y < other.y:
            return True

    def below_of (self, other):
        if self.y > other.y:
            return True

    def left_of_eq (self, other):
        if self.x <= other.x:
            return True

    def right_of_eq (self, other):
        if self.x >= other.x:
            return True

    def above_of_eq (self, other):
        if self.y <= other.y:
            return True

    def below_of_eq (self, other):
        if self.y >= other.y:
            return True

    def __str__ (self):
        return "(x: %s, y: %s)" % (self.x, self.y)

class Bug2D (object):
    """ representation of a bug as read from kwa.filename

        warning: the file will be read into memory as whole
        whitespace on the right of a line is omitted
        whitespace on the left is considered significant
    """

    def __init__ (self, **kwa):
        self.filename = kwa.get ('filename')
        self.pattern  = []
        self._area    = []
        self.offset_x = 0
        self.offset_y = 0

        self._bounds  = dict()

        if not self.filename:
            raise UserWarning, 'missing params'

        for line in open (self.filename, 'r'):
            self.pattern.append (line.rstrip())

        self.max_width = max ([ len (p) for p in self.pattern ])
        self.height    = len (self.pattern)

    def area (self):
        """ based on self.pattern create a list of all points occupied by this bug
            also its bounds
        """

        if not self.pattern:
            raise UserWarning, 'pattern not yet set'

        lu = Point (x = sys.maxint, y = sys.maxint)  # min, min
        ru = Point (x = 0,          y = sys.maxint)  # max, min
        ll = Point (x = sys.maxint, y = 0)           # min, max
        rl = Point (x = 0,          y = 0)           # max, max

        if not self._area:
            area = []

            for y in range (len (self.pattern)):
                for x in range (len (self.pattern[y])):
                    current_x = x + self.offset_x
                    current_y = y + self.offset_y
                    current   = Point (x = current_x, y = current_y)
                    area.append ((current.x, current.y))

                    # print 'point: %s' % current

                    # use FOO_eq methods to catch points that excel
                    # the current maximum only in one dimension
                    #
                    if current.left_of_eq (lu) and current.above_of_eq (lu):
                        lu = Point (x = current.x, y = current.y)
                        # print 'new lu: %s' % lu
                    if current.right_of_eq (ru) and current.above_of_eq (ru):
                        ru = Point (x = current.x, y = current.y)
                        # print 'new ru: %s' % ru
                    if current.left_of_eq (ll) and current.below_of_eq (ll):
                        ll = Point (x = current.x, y = current.y)
                        # print 'new ll: %s' % ll
                    if current.right_of_eq (rl) and current.below_of_eq (rl):
                        rl = Point (x = current.x, y = current.y)
                        # print 'new rl: %s' % rl

            self._bounds4 = (dict (lu = lu, ru = ru, ll = ll, rl = rl))

            # naive search for mins/maxs for a left upper and right lower bounding box
            #
            self._bounds2 = (dict (
                lu = Point (
                    x = min ( lu.x, ru.x, ll.x, rl.x ),
                    y = min ( lu.y, ru.y, ll.y, rl.y ),
                ),
                rl = Point (
                    x = max ( lu.x, ru.x, ll.x, rl.x ),
                    y = max ( lu.y, ru.y, ll.y, rl.y ),
                ),
            ))

            # print 'lu: %s' % lu
            # print 'ru: %s' % ru
            # print 'll: %s' % ll
            # print 'rl: %s' % rl

            # print 'LU: %s' % self._bounds2.get ('lu')
            # print 'RL: %s' % self._bounds2.get ('rl')

            self._area = area

        return self._area

    def bounds (self):
        if not self._area or not self._bounds:
            self.area()

        return self._bounds2

    def move (self, **kwa):
        """ set an offset that will be taken into account when doing calculations (eg area())
        """

        self.offset_x = kwa.get ('x')
        self.offset_y = kwa.get ('y')
        self._area     = []

    def __eq__ (self, other):
        # should both be sorted

        for pair in zip (self.area(), other.area()):
            if  (pair[0][0] != pair[1][0]
            or   pair[0][1] != pair[1][1]):
                return False

        return True

    def __ne__ (self, other):
        return not self.__eq__ (other)

    def __contains__ (self, other):
        """ overlap is confirmed if the bounds overlap or if that is
            not the case if any field of self matches any field of other
        """

#        print 'other lu: %s' % other.bounds().get('lu')
#        print 'other rl: %s' % other.bounds().get('rl')
#        print 'self lu:  %s' % self.bounds().get('lu')
#        print 'self rl:  %s' % self.bounds().get('rl')

        contains = True

        # check if not even the bounds overlap
        #
        if ( other.bounds().get('lu').right_of (self.bounds().get('rl'))     # right of
          or other.bounds().get('rl').left_of  (self.bounds().get('lu'))     # left of
          or other.bounds().get('rl').above_of (self.bounds().get('lu'))     # above of
          or other.bounds().get('lu').below_of (self.bounds().get('rl')) ):  # below of
            # print 'bounds do not match'
            return False

        contains = None  # not used anymore

        # for probably oddly shaped things check every point
        #
        for pair in [(o,s) for o in other.area() for s in self.area()]:
            if  (pair[0][0] == pair[1][0]
            and  pair[0][1] == pair[1][1]):
                return True

        return False

class Landscape2D (object):
    """ representation of a landscape given in a textfile
        file is read via ViewPort
    """

    def __init__ (self, **kwa):
        self.filename   = kwa.get ('filename')
        self.bugs       = []
        self.population = []

        if not self.filename:
            raise UserWarning, 'missing params'

    def find (self, **kwa):
        """ find given bug in landscape
            return list of tuples representing upper left coners of found things
        """

        # TODO some sanity checks. if thing even fits into landsacpe ?

        thing   = kwa.get ('thing')
        origins = []

        if not thing:
            raise UserWarning, 'missing params'

        vp = ViewPort (
            cut_size  = thing.height,
            step_size = 1,
            filename  = self.filename,
        )

        # (1) check if the first line of thing matches in landscape's first line
        # (2) if it does check (for every match in (1)) if the remaining lines macht too
        # (3) matches are counted and must in the end equal the height of the thing's pattern

        for cut in vp.lines():
            #print 'cut: %s' % cut
            #print 'cut[0]: %s' % cut[0]
            #print 'thing.pattern[0]: %s' % thing.pattern[0]

            for index in find_all (string = cut[0], sub = thing.pattern[0]):
                #print 'index: %s' % index
                matched_lines = 1

                for line in range (1, thing.height):
                    #print 'line: %s' % line
                    #print 'cut[%s]: %s' % (line, cut[line])
                    #print 'thing.pattern[%s]: %s' % (line, thing.pattern[line])
                    if index in find_all (string = cut[line], sub = thing.pattern[line]):
                        matched_lines += 1
                        #print 'matched_lines: %s' % matched_lines

                if matched_lines == len (thing.pattern):
                    origins.append ((index, vp.index))

        return origins

    def populate (self, **kwa):
        """ based on origins (calculated with self.find())
            and set self.population with Bug2D objects (clones of the supplied kwa.thing)
            finds overlaps too. with set kwa.remove_overlaps those will be removed
        """

        if self.population:
            raise UserWarning, 'population already set, this might not what you want!'

        origins = self.find (**kwa)
        thing = kwa.get ('thing')
        remove_overlaps = kwa.get ('remove_overlaps')

        for t in origins:
            thing.move (x=t[0], y=t[1])
            self.population.append (copy.deepcopy (thing))

        self.find_overlaps (remove_overlaps = remove_overlaps)

        # reset, just in case
        thing.move (x=0, y=1)

    def find_overlaps (self, **kwa):
        """ search for overlaps in an already set self.population
            with kwa.remove_overlaps == True re-sets self.population without the overlapping things
            sets self.count_overlaps
        """

        remove_overlaps = kwa.get ('remove_overlaps')

        if not self.population:
            raise UserWarning, 'must call populate() before overlaps()'

        overlaps = 0
        clean_population = []

        for (i, p) in enumerate (self.population):
            overlap = False
            for (j, q) in enumerate (self.population[i+1:]):
                if p in q:
                    overlaps += 1
                    overlap = True

            if not overlap:
                clean_population.append (p)

        if remove_overlaps:
            self.population = clean_population

        self.count_overlaps = overlaps

    def count_those (self, **kwa):
        return len (self.find (**kwa))

def parse_args():
    usage = "usage: %prog [options] arg1 arg2"
    parser = OptionParser ()
    parser.add_option (
        '--landscape-filename',
        dest = 'landscape_filename',
        help = 'File containing the landscape',
    )
    parser.add_option (
        '--bug-filename',
        dest = 'bug_filename',
        help = 'File containing the bug',
    )
    parser.add_option (
        '--debug',
        action = 'store_true',
        dest   = 'debug',
        help   = 'The program isn\'t debugged until the last user is dead.',
    )

    return parser.parse_args()

if __name__ == '__main__':

    (options, args) = parse_args ()
    DEBUG = options.debug
    if not options.bug_filename or not options.landscape_filename:
        raise UserWarning, 'missing params'

    ### main

    landscape = Landscape2D (filename = options.landscape_filename)
    bug = Bug2D (filename = options.bug_filename)

    landscape.populate (thing = bug, remove_overlaps=False)
    print 'population:     %s' % len (landscape.population)
    print 'count_overlaps: %s' % landscape.count_overlaps

    if options.debug:
        for thing in landscape.population:
            print 'area: %s' % thing.area()
            print 'rl: %s' % thing.bounds().get ('rl')
            print 'lu: %s' % thing.bounds().get ('lu')
