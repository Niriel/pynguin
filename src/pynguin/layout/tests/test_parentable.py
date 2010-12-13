#! /usr/bin/python
"""
Created on Nov 29, 2010

@author: Niriel
"""

import unittest
from pynguin.layout import parentable

class ParentableTest(unittest.TestCase):
    class MockParent(object):
        pass
    
    def testDocTest(self):
        """Module passes its doctests."""
        import doctest
        failures, unused = doctest.testmod(m=parentable)#, verbose=True)
        self.assertEquals(failures, 0)

    def testParent(self):
        """Parentable.parent sets and gets properly."""
        thing = parentable.Parentable()
        thing.parent = None
        self.assertTrue(thing.parent is None)
        obj1 = self.MockParent()
        obj2 = self.MockParent()
        thing.parent = obj1
        self.assertTrue(thing.parent is obj1)
        thing.parent = obj2
        self.assertTrue(thing.parent is obj2)
        thing.parent = None
        self.assertTrue(thing.parent is None)



if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
