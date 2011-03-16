#! /usr/bin/python
"""
Created on Nov 25, 2010

@author: Niriel
"""

import unittest
from pynguin.layout import size
from pynguin.layout.cell import Cell, CellError
from pynguin.layout import cell as cell_module
from pynguin.layout.padding import Padding
from mock import MockWidget

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

class TestCell(unittest.TestCase):
    """Test the layout.cell module."""
    def testDocTest(self):
        """Module layout.cell passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=cell_module)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)

    def testInitPadded(self):
        """Cell.__init__ properly assigns the padded."""
        padded = MockWidget(10, 20)
        cell = Cell(padded, 'not', 'not')
        self.assertTrue(cell.padded is padded)

    def testInitPadding(self):
        """Cell.__init__ assigns the proper padding values."""
        #
        cell = Cell(None, 'not', 'not')
        self.assertEquals(cell.padding, Padding())
        #
        cell = Cell(None, 'not', 'not', 42)
        self.assertEquals(cell.padding, Padding(42))
        #
        cell = Cell(None, 'not', 'not', 42, 666)
        self.assertEquals(cell.padding, Padding(42, 666))
        #
        cell = Cell(None, 'not', 'not', 1, 2, 3, 4)
        self.assertEquals(cell.padding, Padding(1, 2, 3, 4))
        # When a Padding object is used as a parameter, then the padding
        # attribute of the Cell object is not a copy but is the Padding
        # object itself.
        padding = Padding(1, 2, 3, 4)
        cell = Cell(None, 'not', 'not', padding)
        self.assertTrue(cell.padding is padding)

    def testRequestSize(self):
        """Cell.requestSize(True) adds padding size to padded size."""
        padded = MockWidget(10, 20)
        cell = Cell(padded, 'not', 'not', 1, 2, 4, 8)
        cell.requestSize(True)
        requested_size = cell.requested_size
        self.assertEquals(requested_size, size.Size(13, 32))
        self.assertTrue(isinstance(requested_size, size.Size))
        #
        padded.width = 100
        cell.requestSize(False)
        requested_size = cell.requested_size
        self.assertEquals(requested_size, size.Size(13, 32))
        #
        cell.requestSize(True)
        requested_size = cell.requested_size
        self.assertEquals(requested_size, size.Size(103, 32))


    def testAllocateSizeEqual(self):
        """Cell.allocateSize gives the padded what it wants when ideal.

        We give a cell exactly the size it requests.  Therefore its padded
        should also have the size it requests.  We also check that the
        coordinates of the padded are properly set.

        """
        padded = MockWidget(10, 20)
        cell = Cell(padded, 'not', 'not', 1, 2, 4, 8)
        cell.requestSize(True)
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation((100, 200), requested_size)
        cell.allocateSize(allocated_size)
        padded_size = padded.allocated_size
        self.assertEquals(padded_size.width, 10)
        self.assertEquals(padded_size.height, 20)
        self.assertEquals(padded_size.left, 101)
        self.assertEquals(padded_size.top, 204)

    def testAllocateSizeShrinkABit(self):
        """Cell.allocateSize shrinks the padded when needed."""
        padded = MockWidget(10, 20)
        cell = Cell(padded, 'not', 'not', 1, 2, 4, 8)
        cell.requestSize(True)
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation((100, 200), requested_size)
        allocated_size.height -= 15 # padded height is 20, remove 15 leaves 5.
        cell.allocateSize(allocated_size)
        padded_size = padded.allocated_size
        self.assertEquals(padded_size.width, 10)
        self.assertEquals(padded_size.height, 5) # Only difference with ideal.
        self.assertEquals(padded_size.left, 101)
        self.assertEquals(padded_size.top, 204)

    def testAllocateSizeShrinkpaddedAtMax(self):
        """Cell.allocateSize shrinks the padded down to 0."""
        padded = MockWidget(10, 20)
        cell = Cell(padded, 'not', 'not', 1, 2, 4, 8)
        cell.requestSize(True)
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation(size.Pos(100, 200), requested_size)
        allocated_size.height -= 20 # padded height is 20, remove 20 leaves 0.
        cell.allocateSize(allocated_size)
        padded_size = padded.allocated_size
        self.assertEquals(padded_size.width, 10)
        self.assertEquals(padded_size.height, 0) # Only difference with ideal.
        self.assertEquals(padded_size.left, 101)
        self.assertEquals(padded_size.top, 204)

    def testAllocateSizeShrinkALot(self):
        """Cell.allocateSize shrinks the padded and padding when needed."""
        padded = MockWidget(10, 20)
        cell = Cell(padded, 'not', 'not', 1, 2, 4, 8)
        cell.requestSize(True)
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation((100, 200), requested_size)
        allocated_size.height = 7 # Instead of 4+8=12.
        cell.allocateSize(allocated_size)
        padded_size = padded.allocated_size
        self.assertEquals(padded_size.width, 10)
        self.assertEquals(padded_size.height, 0)
        self.assertEquals(padded_size.left, 101)
        # The padding is 7 instead of 12.  That's a difference of -5. The ratio
        # top/height = 4/(4+8). -5 * 4/(4+8) = -2. 2 pixels are removed from
        # the tocell.padding.s
        self.assertEquals(padded_size.top, 204 - 2)

    def testAllocateSizeInflateNoExpand(self):
        """Cell.allocateSize breaks if too large and expand=EXPAND_NOT."""
        padded = MockWidget(10, 20)
        cell = Cell(padded, 'not', 'not', 1, 2, 4, 8)
        cell.requestSize(True)
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation((0, 0), requested_size.copy())
        allocated_size.height = 50
        self.assertRaises(CellError, cell.allocateSize, allocated_size)

    def testAllocatedSizeInflateNoFill(self):
        """Cell.allocatedSize inflates the padding when needed."""
        padded = MockWidget(10, 20)
        cell = Cell(padded, 'padding', 'padding', 1, 2, 4, 8)
        cell.requestSize(True)
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation((100, 200), requested_size)
        allocated_size.height += 50
        cell.allocateSize(allocated_size)
        padded_size = padded.allocated_size
        self.assertEquals(padded_size.width, 10)
        self.assertEquals(padded_size.height, 20)
        self.assertEquals(padded_size.left, 101)
        # We add 50 to the padding.  The ratio top/bottom is 4/(4+8).
        # 50*4/12=16. 16 is added to the top.
        self.assertEquals(padded_size.top, 204 + 16)

    def testAllocatedSizeInflateFill(self):
        """Cell.allocatedSize inflates the padded when needed."""
        padded = MockWidget(10, 20)
        cell = Cell(padded, 'padded', 'padded', 1, 2, 4, 8)
        cell.requestSize(True)
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation(size.Pos(100, 200),
                                             requested_size)
        allocated_size.height += 50
        cell.allocateSize(allocated_size)
        padded_size = padded.allocated_size
        self.assertEquals(padded_size.width, 10)
        self.assertEquals(padded_size.height, 20 + 50)
        self.assertEquals(padded_size.left, 101)
        self.assertEquals(padded_size.top, 204)
