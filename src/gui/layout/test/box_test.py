'''
Created on Nov 9, 2010

@author: Niriel
'''

import unittest
from gui.layout import size
from gui.layout import box
from gui.layout.padding import Padding
from gui.layout.parentable import Parentable
from gui.layout.cell import Cell


class TestDocTest(unittest.TestCase):
    def testDocTest(self):
        """module box passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=box)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)


class TestHomothecy(unittest.TestCase):
    def testNoChange(self):
        """Homothecy returns unchanged values if dest_length = ori_length."""
        ori_lengths = [50, 100, 33]
        dest_length = sum(ori_lengths)
        dest_lengths = box.Homothecy(ori_lengths, dest_length)
        self.assertEquals(dest_lengths, ori_lengths)
    def testZoomInTwice(self):
        """Homothecy doubles the lengths properly."""
        ori_lengths = [50, 100, 33]
        dest_length = sum(ori_lengths) * 2
        dest_lengths = box.Homothecy(ori_lengths, dest_length)
        self.assertEquals(dest_lengths, [100, 200, 66])
    def testZoomOutTwice(self):
        """Homothecy halves the lengths properly.

        This is a good way of spotting integer division errors.

        """
        ori_lengths = [50, 100, 33]
        dest_length = sum(ori_lengths) / 2
        dest_lengths = box.Homothecy(ori_lengths, dest_length)
        self.assertEquals(dest_lengths, [25, 50, 16])
    def testAlwaysWork(self):
        """Homothecy always return a result with the proper length."""
        ori_lengths = [50, 100, 33]
        for dest_length in range(sum(ori_lengths) * 2):
            dest_lengths = box.Homothecy(ori_lengths, dest_length)
            self.assertEquals(sum(dest_lengths), dest_length,
                              "sum(%r) == %i != %i" % (dest_lengths,
                                                       sum(dest_lengths),
                                                       dest_length)
                              )


class TestBox(unittest.TestCase):
    class MockWidget(Parentable):
        """A pseudo padded implementing only what I need for this test."""
        def __init__(self, width, height):
            Parentable.__init__(self)
            self.width = width
            self.height = height
        def requestSize(self):
            self.requested_size = size.Size(self.width, self.height)
        def allocateSize(self, allocated_size):
            self.allocated_size = allocated_size

    def testInitSpacing(self):
        """Box.__init__ stores the spacing parameter properly."""
        my_box = box.Box(42, False)
        self.assertEquals(my_box.spacing, 42)

    def testInitHomogeneous(self):
        """Box.__init__ stores the homogeneous parameter properly."""
        my_box = box.Box(0, False)
        self.assertFalse(my_box.homogeneous)
        my_box = box.Box(0, True)
        self.assertTrue(my_box.homogeneous)

    def testAddChild(self):
        """Box.addChild does its job."""
        child = TestBox.MockWidget(0, 0)
        # Non-homogeneous.
        my_box = box.Box(0, False)
        my_box.addChild(child, Cell.EXPAND_NOT, Cell.EXPAND_PADDING)
        my_box = box.Box(0, False)
        my_box.addChild(child, Cell.EXPAND_PADDING, Cell.EXPAND_NOT)
        my_box = box.Box(0, False)
        my_box.addChild(child, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
        # Homogeneous.
        my_box = box.Box(0, True)
        my_box.addChild(child, Cell.EXPAND_NOT, Cell.EXPAND_PADDING)
        my_box = box.Box(0, True)
        my_box.addChild(child, Cell.EXPAND_PADDING, Cell.EXPAND_NOT)
        my_box = box.Box(0, True)
        my_box.addChild(child, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
        #
        my_box = box.Box(0, True)
        my_box.addChild(child, Cell.EXPAND_PADDING, Cell.EXPAND_PADDED, 1, 2, 4, 8)
        cell = my_box.cells[0]
        self.assertTrue(cell.padded is child)
        self.assertEquals(cell.padding, Padding(1, 2, 4, 8))

    def testRequestSizeHomogeneous(self):
        """Box.requestSize is correct in the homogeneous case."""
        w1 = TestBox.MockWidget(20, 10)
        w2 = TestBox.MockWidget(40, 10)
        w3 = TestBox.MockWidget(30, 15)
        # The widest padded is 40 pixels wide.  All will get 40 in length.
        # 3 * 40 = 120
        # The max height is 15, we should retreive that.
        b = box.Box(7, True)
        # Add two times 7: 120+2*7=134.
        b.PRIMARY_LENGTH = 'width'
        b.SECONDARY_LENGTH = 'height'
        b.addChild(w1, Cell.EXPAND_PADDED, Cell.EXPAND_PADDED)
        b.addChild(w2, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
        b.addChild(w3, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
        # No padding.
        b.requestSize()
        self.assertEquals(b.requested_size, size.Size(134, 15))

    def testRequestSizeHeterogeneous(self):
        """Box.requestSize is correct in the heterogeneous case."""
        w1 = TestBox.MockWidget(20, 10)
        w2 = TestBox.MockWidget(40, 10)
        w3 = TestBox.MockWidget(30, 15)
        # 20 + 40 + 30 = 90.
        # The max height is 15, we should retrieve that.
        b = box.Box(7, False)
        # Add two times 7: 90 + 2 * 7 = 104.
        b.PRIMARY_LENGTH = 'width'
        b.SECONDARY_LENGTH = 'height'
        b.addChild(w1, Cell.EXPAND_PADDED, Cell.EXPAND_PADDED)
        b.addChild(w2, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
        b.addChild(w3, Cell.EXPAND_PADDING, Cell.EXPAND_PADDING)
        # No padding.
        b.requestSize()
        self.assertEquals(b.requested_size, size.Size(104, 15))

    def testAllocateSizeShrinkABit(self):
        """Box.allocateSize shrinks and leaves space to cells."""
        w1 = TestBox.MockWidget(20, 10)
        w2 = TestBox.MockWidget(40, 10)
        w3 = TestBox.MockWidget(30, 15)
        # 20 + 40 + 30 = 90 for the widgets.
        b = box.Box(7, False)
        # Add two times 7 = 14 for the total spacing.
        # Total width: 90 + 14 = 104.
        b.PRIMARY_LENGTH = 'width'
        b.SECONDARY_LENGTH = 'height'
        b.addChild(w1, Cell.EXPAND_NOT, Cell.EXPAND_PADDING)
        b.addChild(w2, Cell.EXPAND_NOT, Cell.EXPAND_PADDED)
        b.addChild(w3, Cell.EXPAND_NOT, Cell.EXPAND_PADDING)
        # No padding.
        b.requestSize() # Always do that, even if you don't use.
        self.assertEquals(b.requested_size, size.Size(104, 15))
        allocated_size = size.SizeAllocation(size.Pos(100, 200),
                                             size.Size(70, 12))
        b.allocateSize(allocated_size)
        # First, check that the allocated size was stored.
        self.assertTrue(b.allocated_size is allocated_size)
        # All cells must measure 12 in height.
        self.assertEquals(b.cells[0].allocated_size.height, 12)
        self.assertEquals(b.cells[1].allocated_size.height, 12)
        self.assertEquals(b.cells[2].allocated_size.height, 12)
        # All widgets must have their original height except the one that
        # was too big: they were not allowed to fill.
        self.assertEquals(w1.allocated_size.height, 10)
        self.assertEquals(w2.allocated_size.height, 12)
        self.assertEquals(w3.allocated_size.height, 12)
        # Width.  We asked 70.  Remove 14 for the spacing, rest 56.  The
        # widgets wanted 90.  56/90 = 0.62222.
        # 20 * 0.62222 = 12.4444 = 12
        # 40 * 0.62222 = 24.8888 = 25
        # 30 * 0.62222 = 16.6666 = 17
        # But the last is just given the rest:
        # 56 - 12 - 25 = 19.
        self.assertEquals(b.cells[0].allocated_size.width, 12)
        self.assertEquals(b.cells[1].allocated_size.width, 25)
        self.assertEquals(b.cells[2].allocated_size.width, 19)
        self.assertEquals(w1.allocated_size.width, 12)
        self.assertEquals(w2.allocated_size.width, 25)
        self.assertEquals(w3.allocated_size.width, 19)
        
    def testAllocateSizeInflateButWidgetsDontExpand(self):
        """TextBox.allocateSize breaks if inflate with no expand child.
        
        It is forbidden to inflate a Box if none of its child has the expand
        property set to True in the direction in which the box tries to expand.
        
        In such a case, size.SizeAllocationError is raised.

        """
        w1 = TestBox.MockWidget(20, 10)
        w2 = TestBox.MockWidget(40, 10)
        w3 = TestBox.MockWidget(30, 15)
        # 20 + 40 + 30 = 90 for the widgets.
        b = box.Box(7, False)
        # Add two times 7 = 14 for the total spacing.
        # Total width: 90 + 14 = 104.
        b.PRIMARY_LENGTH = 'width'
        b.SECONDARY_LENGTH = 'height'
        b.PRIMARY_COORD = 'left'
        b.SECONDARY_COORD = 'top'
        b.addChild(w1, Cell.EXPAND_NOT, Cell.EXPAND_PADDING)
        b.addChild(w2, Cell.EXPAND_NOT, Cell.EXPAND_PADDED)
        b.addChild(w3, Cell.EXPAND_NOT, Cell.EXPAND_PADDING)
        # No padding.
        b.requestSize() # Always do that, even if you don't use.
        self.assertEquals(b.requested_size, size.Size(104, 15))
        allocated_size = size.SizeAllocation(size.Pos(100, 200),
                                             size.Size(120, 20))
        self.assertRaises(size.SizeAllocationError,
                          b.allocateSize, allocated_size)

    def testAllocateSizeInflate(self):
        """TextBox.allocateSize inflates properly."""
        w1 = TestBox.MockWidget(20, 10)
        w2 = TestBox.MockWidget(40, 10)
        w3 = TestBox.MockWidget(30, 15)
        # 20 + 40 + 30 = 90 for the widgets.
        b = box.Box(7, False)
        # Add two times 7 = 14 for the total spacing.
        # Total width: 90 + 14 = 104.
        b.PRIMARY_LENGTH = 'width'
        b.SECONDARY_LENGTH = 'height'
        b.PRIMARY_COORD = 'left'
        b.SECONDARY_COORD = 'top'
        b.addChild(w1, Cell.EXPAND_NOT, Cell.EXPAND_PADDING)
        b.addChild(w2, Cell.EXPAND_PADDING, Cell.EXPAND_PADDED)
        b.addChild(w3, Cell.EXPAND_PADDED, Cell.EXPAND_PADDING)
        # No padding.
        b.requestSize() # Always do that, even if you don't use.
        self.assertEquals(b.requested_size, size.Size(104, 15))
        allocated_size = size.SizeAllocation(size.Pos(100, 200),
                                             size.Size(120, 17))
        b.allocateSize(allocated_size)
        #
        self.assertTrue(b.allocated_size is allocated_size)
        #
        # The first child does not expand so it keeps its width of 20.
        # 90 (total padded) - 20 = 70 for the expandable widgets.
        # 104 total width - 70 = 34 of fixed size.
        # The new width is 120.
        # 120 - 34 = 86 instead of 70 for the expandable widgets.
        # That is a factor 86/70.
        # Child 2 has width 40.  40*86/70 = 49.14, so we say 49.
        # Child 3 has width 30.  30*86/70 = 36.86, so we say 37.
        # 49 + 37 = 86 which is indeed what we want.
        c1, c2, c3 = b.cells
        self.assertEquals(c1.allocated_size, size.SizeAllocation(size.Pos(100, 200), size.Size(20, 17)))
        self.assertEquals(c2.allocated_size, size.SizeAllocation(size.Pos(100+20+7, 200), size.Size(49, 17)))
        self.assertEquals(c3.allocated_size, size.SizeAllocation(size.Pos(100+20+7+49+7, 200), size.Size(37, 17)))

if __name__ == "__main__":
    unittest.main()
