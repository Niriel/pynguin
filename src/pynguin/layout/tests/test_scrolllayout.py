#! /usr/bin/python
"""
Created on Dec 13, 2010

@author: delforge
"""

import unittest
from pynguin.layout.size import SizeAllocation
from pynguin.layout.cell import Cell
from pynguin.layout import scrolllayout
from mock import MockWidget

class TestScrollLayout(unittest.TestCase):
    """Test ScrollLayout."""

    def testAllocateSize(self):
        """ScrollLayout.allocateSize sets the children position to (0, 0)."""
        my_scroll = scrolllayout.ScrollLayout()
        cells = [Cell(MockWidget(10, 100), 'padded', 'padded')]
        requested_size = my_scroll.requestSize(cells)
        allocated_size = SizeAllocation((10, 20), (30, 40))
        my_scroll.allocateSize(allocated_size, requested_size, cells)
        cell_size = cells[0].allocated_size
        self.assertEquals(cell_size, SizeAllocation((0, 0), (30, 100)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()