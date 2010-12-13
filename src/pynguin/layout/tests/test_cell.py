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

class TestDocTest(unittest.TestCase):
    def testDocTest(self):
        """module size passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=cell_module)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)

class TestCell(unittest.TestCase):
    class Mockpadded(object):
        """A pseudo padded implementing only what I need for this test."""
        def requestSize(self):
            self.requested_size = size.Size(10, 20)
        def allocateSize(self, allocated_size):
            self.allocated_size = allocated_size

    def testInitPadded(self):
        """Cell.__init__ properly assigns the padded."""
        padded = TestCell.Mockpadded()
        p = Cell(padded, Cell.EXPAND_NOT, Cell.EXPAND_NOT)
        self.assertTrue(p.padded is padded)

    def testInitPadding(self):
        """Cell.__init__ assigns the proper padding values."""
        #
        p = Cell(None, Cell.EXPAND_NOT, Cell.EXPAND_NOT)
        self.assertEquals(p.padding, Padding())
        #
        p = Cell(None, Cell.EXPAND_NOT, Cell.EXPAND_NOT, 42)
        self.assertEquals(p.padding, Padding(42))
        #
        p = Cell(None, Cell.EXPAND_NOT, Cell.EXPAND_NOT, 42, 666)
        self.assertEquals(p.padding, Padding(42, 666))
        #
        p = Cell(None, Cell.EXPAND_NOT, Cell.EXPAND_NOT, 1, 2, 3, 4)
        self.assertEquals(p.padding, Padding(1, 2, 3, 4))
        # When a Padding object is used as a parameter, then the padding
        # attribute of the Cell object is not a copy but is the Padding
        # object itself.
        padding = Padding(1, 2, 3, 4)
        p = Cell(None, Cell.EXPAND_NOT, Cell.EXPAND_NOT, padding)
        self.assertTrue(p.padding is padding)

    def testRequestSize(self):
        """Cell.requestSize adds padding size to padded size."""
        padded = TestCell.Mockpadded()
        cell = Cell(padded, Cell.EXPAND_NOT, Cell.EXPAND_NOT, 1, 2, 4, 8)
        cell.requestSize()
        rs = cell.requested_size
        self.assertEquals(rs, size.Size(13, 32))
        self.assertTrue(isinstance(rs, size.Size))

    def testAllocateSizeEqual(self):
        """Cell.allocateSize gives the padded what it wants when ideal.

        We give a cell exactly the size it requests.  Therefore its padded
        should also have the size it requests.  We also check that the
        coordinates of the padded are properly set.

        """
        padded = TestCell.Mockpadded()
        cell = Cell(padded, Cell.EXPAND_NOT, Cell.EXPAND_NOT, 1, 2, 4, 8)
        cell.requestSize()
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
        padded = TestCell.Mockpadded()
        cell = Cell(padded, Cell.EXPAND_NOT, Cell.EXPAND_NOT, 1, 2, 4, 8)
        cell.requestSize()
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
        padded = TestCell.Mockpadded()
        cell = Cell(padded, Cell.EXPAND_NOT, Cell.EXPAND_NOT, 1, 2, 4, 8)
        cell.requestSize()
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
        padded = TestCell.Mockpadded()
        cell = Cell(padded, Cell.EXPAND_NOT, Cell.EXPAND_NOT, 1, 2, 4, 8)
        cell.requestSize()
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
        # the top padding.s
        self.assertEquals(padded_size.top, 204 - 2)

    def testAllocateSizeInflateNoExpand(self):
        """Cell.allocateSize breaks if too large and expand=EXPAND_NOT."""
        padded = TestCell.Mockpadded()
        cell = Cell(padded, Cell.EXPAND_NOT, Cell.EXPAND_NOT, 1, 2, 4, 8)
        cell.requestSize()
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation((0, 0), requested_size.copy())
        allocated_size.height = 50
        self.assertRaises(CellError, cell.allocateSize, allocated_size)

    def testAllocatedSizeInflateNoFill(self):
        """Cell.allocatedSize inflates the padding when needed."""
        padded = TestCell.Mockpadded()
        cell = Cell(padded, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING, 1, 2, 4, 8)
        cell.requestSize()
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation((100, 200), requested_size)
        allocated_size.height += 50
        cell.allocateSize(allocated_size)
        padded_size = padded.allocated_size
        self.assertEquals(padded_size.width, 10)
        self.assertEquals(padded_size.height, 20)
        self.assertEquals(padded_size.left, 101)
        # We add 50 to the padding.  The ratio top/bottom is 4/(4+8).
        # 50*4/12=16. 16 is added to the top padding.
        self.assertEquals(padded_size.top, 204 + 16)

    def testAllocatedSizeInflateFill(self):
        """Cell.allocatedSize inflates the padded when needed."""
        padded = TestCell.Mockpadded()
        cell = Cell(padded, Cell.EXPAND_PADDED, Cell.EXPAND_PADDED, 1, 2, 4, 8)
        cell.requestSize()
        requested_size = cell.requested_size
        allocated_size = size.SizeAllocation(size.Pos(100, 200), requested_size)
        allocated_size.height += 50
        cell.allocateSize(allocated_size)
        padded_size = padded.allocated_size
        self.assertEquals(padded_size.width, 10)
        self.assertEquals(padded_size.height, 20 + 50)
        self.assertEquals(padded_size.left, 101)
        self.assertEquals(padded_size.top, 204)
