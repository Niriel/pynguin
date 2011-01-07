#! /usr/bin/python
"""
Created on Dec 13, 2010

@author: Niriel
"""

import unittest
from pynguin.layout.size import SizeAllocation
from pynguin.layout.cell import Cell
from pynguin.layout import windowlayout
from mock import MockWidget

class TestWindowLayout(unittest.TestCase):
    """Test the WindowLayout layout."""
    def testAllocateSize(self):
        """WindowLayout.allocateSize sets the children position to (0, 0)."""
        my_win = windowlayout.WindowLayout()
        cell = Cell(MockWidget(10, 20), 'padded', 'padded')
        requested_size = my_win.requestSize(cell)
        allocated_size = SizeAllocation((10, 20), (30, 40))
        my_win.allocateSize(allocated_size, requested_size, cell)
        cell_size = cell.allocated_size
        self.assertEquals(cell_size, SizeAllocation((0, 0), (30, 40)))

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
