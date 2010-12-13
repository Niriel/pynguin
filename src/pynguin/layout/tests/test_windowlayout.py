#! /usr/bin/python
"""
Created on Dec 13, 2010

@author: delforge
"""

import unittest
from pynguin.layout.size import SizeAllocation
from pynguin.layout.cell import Cell
from pynguin.layout import windowlayout
from mock import MockWidget

class TestWindowLayout(unittest.TestCase):
    """Test the WindowLayout layout."""
    
    def testRequestSize(self):
        """WindowLayout.requestSize returns the requested size of its cell."""
        my_win = windowlayout.WindowLayout()
        cells = [Cell(MockWidget(10, 20), 'not', 'not')]
        requested_size = my_win.requestSize(cells)
        self.assertEquals(requested_size.asTuple(), (10, 20))

    def testAllocateSize(self):
        """WindowLayout.allocateSize sets the children position to (0, 0)."""
        my_win = windowlayout.WindowLayout()
        cells = [Cell(MockWidget(10, 20), 'padded', 'padded')]
        requested_size = my_win.requestSize(cells)
        allocated_size = SizeAllocation((10, 20), (30, 40))
        my_win.allocateSize(allocated_size, requested_size, cells)
        cell_size = cells[0].allocated_size
        self.assertEquals(cell_size, SizeAllocation((0, 0), (30, 40)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()