#! /usr/bin/python
"""
Created on Dec 13, 2010

@author: Niriel
"""

import unittest
from pynguin.layout.size import Size, SizeAllocation
from pynguin.layout import windowlayout
from mock import MockWidget

class TestWindowLayout(unittest.TestCase):
    """Test the WindowLayout layout."""

    def testDocTest(self):
        """Module layout.windowlayout passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=windowlayout)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)

    def testRequestSize(self):
        """WindowLayout.requestSize requests the size of its child."""
        my_layout = windowlayout.WindowLayout()
        child = MockWidget(10, 20)
        child.requestSize(True)
        requested_size = my_layout.requestSize([child])
        self.assertEquals(requested_size, Size(10, 20))

    def testAllocateSize(self):
        """WindowLayout.allocateSize sets the children position to (0, 0)."""
        my_layout = windowlayout.WindowLayout()
        child = MockWidget(10, 20)
        child.requestSize(True)
        requested_size = my_layout.requestSize([child])
        allocated_size = SizeAllocation((10, 20), (30, 40))
        my_layout.allocateSize(allocated_size, requested_size, [child])
        cell_size = child.allocated_size
        self.assertEquals(cell_size, SizeAllocation((0, 0), (30, 40)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
