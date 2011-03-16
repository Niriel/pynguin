#! /usr/bin/python
"""
Created on Dec 13, 2010

@author: Niriel
"""

import unittest
from pynguin.layout.size import Size, SizeAllocation
from pynguin.layout.cell import Cell
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
        """WindowLayout.requestSize requests the size of its cell."""
        my_layout = windowlayout.WindowLayout()
        cell = Cell(MockWidget(10, 20), 'padded', 'padded')
        cell.requestSize(True)
        requested_size = my_layout.requestSize([cell])
        self.assertEquals(requested_size, Size(10, 20))

    def testAllocateSize(self):
        """WindowLayout.allocateSize sets the children position to (0, 0)."""
        my_layout = windowlayout.WindowLayout()
        cell = Cell(MockWidget(10, 20), 'padded', 'padded')
        cell.requestSize(True)
        requested_size = my_layout.requestSize([cell])
        allocated_size = SizeAllocation((10, 20), (30, 40))
        my_layout.allocateSize(allocated_size, requested_size, [cell])
        cell_size = cell.allocated_size
        self.assertEquals(cell_size, SizeAllocation((0, 0), (30, 40)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
