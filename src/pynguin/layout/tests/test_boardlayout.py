#! /usr/bin/python
"""
Created on Dec 13, 2010

@author: Niriel
"""

import unittest
from pynguin.layout.size import Size
from pynguin.layout.size import SizeAllocation
from pynguin.layout import boardlayout
from pynguin.layout.cell import Cell
from mock import MockWidget

class TestDocTest(unittest.TestCase):
    """Checks that the module box passes its doctests."""
    def testDocTest(self):
        """Module layout.boardlayout passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=boardlayout)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)


class TestBoard(unittest.TestCase):
    """Test the BoardLayout layout."""
    def testRequestSize(self):
        """BoardLayout.requestSize returns its favorite size."""
        cells = [Cell(MockWidget(20, 10), 'not', 'not'),
                 Cell(MockWidget(40, 10), 'not', 'not'),
                 Cell(MockWidget(30, 15), 'not', 'not')]
        for cell in cells:
            cell.requestSize(True)
        my_board = boardlayout.BoardLayout()
        requested_size = my_board.requestSize(cells)
        self.assertEquals(requested_size, my_board.preferred_size)
        self.assertEquals(cells[0].requested_size, Size(20, 10))
        self.assertEquals(cells[1].requested_size, Size(40, 10))
        self.assertEquals(cells[2].requested_size, Size(30, 15))

    def testAllocateSize(self):
        """BoardLayout.allocateSize gives the cells the size they want."""
        cells = [Cell(MockWidget(20, 10), 'not', 'not'),
                 Cell(MockWidget(40, 10), 'not', 'not'),
                 Cell(MockWidget(30, 15), 'not', 'not')]
        for cell in cells:
            cell.requestSize(True)
        my_board = boardlayout.BoardLayout()
        requested_size = my_board.requestSize(cells)
        allocated_size = SizeAllocation((1, 2), requested_size)
        my_board.allocateSize(allocated_size, requested_size, cells)
        cell_sizes = [cell.allocated_size for cell in cells]
        self.assertEquals(cell_sizes[0], SizeAllocation((0, 0), (20, 10)))
        self.assertEquals(cell_sizes[1], SizeAllocation((0, 0), (40, 10)))
        self.assertEquals(cell_sizes[2], SizeAllocation((0, 0), (30, 15)))

if __name__ == "__main__":
    unittest.main()
