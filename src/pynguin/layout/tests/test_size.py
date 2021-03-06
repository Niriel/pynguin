#! /usr/bin/python
"""
Created on Nov 4, 2010

@author: Niriel
"""

import unittest
from pynguin.layout import size

class TestDocTest(unittest.TestCase):
    def testDocTest(self):
        """Module layout.size passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=size)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)

if __name__ == "__main__":
    unittest.main()
