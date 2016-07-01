# match2d
find ascii-patterns in ascii-landscapes

## usage from commandline
cd match2d ; python2 match2d.py --landscape-filename=tests/bug01.txt --bug-filename=tests/bug01.txt

## running tests
cd match2d/tests/ ; python2 smoke.py      # basic functionality
cd match2d/tests/ ; python2 shapes.py     # some more or less odd shapes
cd match2d/tests/ ; python2 expensive.py  # previously expensive test; meanwhile optimised :)
cd match2d/tests/ ; python2 point.py      # test helpers
