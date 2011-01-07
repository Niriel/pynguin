#! /usr/bin/python
"""
Created on Jan 7, 2011

@author: Niriel
"""

import unittest
from pynguin.layout.size import Size, SizeAllocation
from pynguin.layout.cell import Cell
from pynguin.layout import binlayout
from mock import MockWidget

class TestBinLayout(unittest.TestCase):
    """Test the binlayout module."""
    def testRequestSize(self):
        """BinLayout.requestSize return the size requested by the cell."""
        cell = Cell(MockWidget(10, 20), 'not', 'not')
        layout = binlayout.BinLayout()
        requested_size = layout.requestSize(cell)
        self.assertEquals(requested_size, Size(10, 20))
    
    def testAllocateSize(self):
        """BinLayout.allocateSize allocates the size of the cell."""
        cell = Cell(MockWidget(10, 20), 'padding', 'padding')
        layout = binlayout.BinLayout()
        requested_size = layout.requestSize(cell)
        allocated_size = SizeAllocation((100, 200), (25, 50))
        layout.allocateSize(allocated_size, requested_size, cell)
        self.assertEquals(cell.allocated_size, allocated_size)

if __name__ == "__main__":
    unittest.main()
