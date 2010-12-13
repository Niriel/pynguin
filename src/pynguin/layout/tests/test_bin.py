#! /usr/bin/python
"""
Created on Nov 17, 2010

@author: Niriel
"""

import unittest
from pynguin.layout import bin

class TestBin(unittest.TestCase):
    def testDocTest(self):
        """Module passes its doctests."""
        import doctest
        failures, unused = doctest.testmod(m=bin)#, verbose=True)
        self.assertEquals(failures, 0)

if __name__ == "__main__":
    unittest.main()
