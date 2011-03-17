#! /usr/bin/python
"""
Created on Dec 13, 2010

@author: Niriel
"""

import unittest
from pynguin.layout.size import SizeAllocation
from pynguin.layout import scrolllayout
from mock import MockWidget

class TestScrollLayout(unittest.TestCase):
    """Test ScrollLayout."""

    def testDocTest(self):
        """Module layout.scrolllayout its doctests."""
        import doctest
        failures, unused = doctest.testmod(m=scrolllayout)#, verbose=True)
        self.assertEquals(failures, 0)

    def testAllocateSize(self):
        """ScrollLayout.allocateSize sets the children position to (0, 0)."""
        my_scroll = scrolllayout.ScrollLayout()
        child = MockWidget(10, 100)
        child.requestSize(True)
        requested_size = my_scroll.requestSize([child])
        allocated_size = SizeAllocation((10, 20), (30, 40))
        my_scroll.allocateSize(allocated_size, requested_size, [child])
        child_size = child.allocated_size
        self.assertEquals(child_size, SizeAllocation((0, 0), (30, 100)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
