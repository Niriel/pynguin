#! /usr/bin/python
"""
Created on Nov 9, 2010

@author: Niriel
"""

import unittest
from pynguin.layout.size import Size
from pynguin.layout.size import SizeAllocation
from pynguin.layout import boxlayout
from pynguin.layout.cell import Cell
from mock import MockWidget

class TestDocTest(unittest.TestCase):
    """Checks that the module boxlayout passes its doctests."""
    def testDocTest(self):
        """Module layout.boxlayout passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=boxlayout)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)


class TestHomothecy(unittest.TestCase):
    """Test the function boxlayout.Homothecy."""
    def testAlwaysWork(self):
        """Homothecy always return a result with the proper length."""
        ori_lengths = [50, 100, 33]
        for dest_length in range(sum(ori_lengths) * 2):
            poss, lengths = boxlayout.Homothecy(ori_lengths, dest_length)
            self.assertEquals(sum(lengths), dest_length,
                              "sum(%r) == %i != %i" % (lengths,
                                                       sum(lengths),
                                                       dest_length)
                              )
            positions = [0]
            for length in lengths[:-1]:
                positions.append(positions[-1] + length)
            self.assertEquals(poss, positions)


class TestBox(unittest.TestCase):
    """Test the class boxlayout.BoxLayout"""
    def testInitSpacing(self):
        """BoxLayout.__init__ stores the spacing parameter properly."""
        my_box = boxlayout.BoxLayout(42, False)
        self.assertEquals(my_box.spacing, 42)

    def testInitHomogeneous(self):
        """BoxLayout.__init__ stores the is_homogeneous parameter properly."""
        my_box = boxlayout.BoxLayout(0, False)
        self.assertFalse(my_box.is_homogeneous)
        my_box = boxlayout.BoxLayout(0, True)
        self.assertTrue(my_box.is_homogeneous)

    def testRequestSizeHomogeneous(self):
        """BoxLayout.requestSize is correct in the is_homogeneous case."""
        cells = [Cell(MockWidget(20, 10), 'padded', 'padded'),
                 Cell(MockWidget(40, 10), 'padding', 'padding'),
                 Cell(MockWidget(30, 15), 'padding', 'padding')]
        for cell in cells:
            cell.requestSize(True)
        # The widest padded is 40 pixels wide.  All will get 40 in length.
        # 3 * 40 = 120
        # The max height is 15, we should retrieve that.
        my_box = boxlayout.BoxLayout(7, True)
        # Add two times 7: 120+2*7=134.
        my_box.PRIMARY_LENGTH = 'width'
        my_box.SECONDARY_LENGTH = 'height'
        # No padding.
        requested_size = my_box.requestSize(cells)
        self.assertEquals(requested_size, Size(134, 15))

    def testRequestSizeHeterogeneous(self):
        """BoxLayout.requestSize is correct in the heterogeneous case."""
        cells = [Cell(MockWidget(20, 10), 'padded', 'padded'),
                 Cell(MockWidget(40, 10), 'padding', 'padding'),
                 Cell(MockWidget(30, 15), 'padding', 'padding')]
        for cell in cells:
            cell.requestSize(True)
        # 20 + 40 + 30 = 90.
        # The max height is 15, we should retrieve that.
        my_box = boxlayout.BoxLayout(7, False)
        # Add two times 7: 90 + 2 * 7 = 104.
        my_box.PRIMARY_LENGTH = 'width'
        my_box.SECONDARY_LENGTH = 'height'
        requested_size = my_box.requestSize(cells)
        self.assertEquals(requested_size, Size(104, 15))

    def testAllocateSizeShrinkABit(self):
        """BoxLayout.allocateSize shrinks and leaves space to cells."""
        cells = [Cell(MockWidget(20, 10), 'padded', 'padded'),
                 Cell(MockWidget(40, 10), 'padding', 'padding'),
                 Cell(MockWidget(30, 15), 'padding', 'padding')]
        for cell in cells:
            cell.requestSize(True)
        # 20 + 40 + 30 = 90 for the widgets.
        my_box = boxlayout.BoxLayout(7, False)
        # Add two times 7 = 14 for the total spacing.
        # Total width: 90 + 14 = 104.
        my_box.PRIMARY_LENGTH = 'width'
        my_box.SECONDARY_LENGTH = 'height'
        my_box.PRIMARY_COORD = 'left'
        my_box.SECONDARY_COORD = 'top'
        # No padding.
        requested_size = my_box.requestSize(cells)
        self.assertEquals(requested_size, Size(104, 15))
        allocated_size = SizeAllocation((100, 200), (70, 12))
        my_box.allocateSize(allocated_size, requested_size, cells)
        # All cells must measure 12 in height.
        self.assertEquals(cells[0].allocated_size.height, 12)
        self.assertEquals(cells[1].allocated_size.height, 12)
        self.assertEquals(cells[2].allocated_size.height, 12)
        # Widget height depends on the expand options.
        self.assertEquals(cells[0].padded.allocated_size.height, 12)
        self.assertEquals(cells[1].padded.allocated_size.height, 10)
        self.assertEquals(cells[2].padded.allocated_size.height, 12)
        # Width.  We asked 70.  Remove 14 for the spacing, rest 56.  The
        # widgets wanted 90.  56/90 = 0.62222.
        # 20 * 0.62222 = 12.4444 = 12
        # 40 * 0.62222 = 24.8888 = 25
        # 30 * 0.62222 = 16.6666 = 17
        # But the last is just given the rest:
        # 56 - 12 - 25 = 19.
        self.assertEquals(cells[0].allocated_size.width, 12)
        self.assertEquals(cells[1].allocated_size.width, 25)
        self.assertEquals(cells[2].allocated_size.width, 19)
        self.assertEquals(cells[0].padded.allocated_size.width, 12)
        self.assertEquals(cells[1].padded.allocated_size.width, 25)
        self.assertEquals(cells[2].padded.allocated_size.width, 19)

    def testAllocateSizeInflateButWidgetsDontExpand(self):
        """TextBox.allocateSize breaks if inflate with no expand child.

        It is forbidden to inflate a BoxLayout if none of its child has the
        expand property set to True in the direction in which the boxlayout
        tries to expand.

        In such a case, size.SizeAllocationError is raised.

        """
        cells = [Cell(MockWidget(20, 10), 'not', 'padded'),
                 Cell(MockWidget(40, 10), 'not', 'padding'),
                 Cell(MockWidget(30, 15), 'not', 'padding')]
        for cell in cells:
            cell.requestSize(True)
        # 20 + 40 + 30 = 90 for the widgets.
        my_box = boxlayout.BoxLayout(7, False)
        # Add two times 7 = 14 for the total spacing.
        # Total width: 90 + 14 = 104.
        my_box.PRIMARY_LENGTH = 'width'
        my_box.SECONDARY_LENGTH = 'height'
        my_box.PRIMARY_COORD = 'left'
        my_box.SECONDARY_COORD = 'top'
        # No padding.
        requested_size = my_box.requestSize(cells)
        self.assertEquals(requested_size, Size(104, 15))
        allocated_size = SizeAllocation((100, 200), (120, 20))
        self.assertRaises(boxlayout.BoxError, my_box.allocateSize,
                          allocated_size, requested_size, cells)

    def testAllocateSizeInflate(self):
        """TextBox.allocateSize inflates properly."""
        cells = [Cell(MockWidget(20, 10), 'not', 'padded'),
                 Cell(MockWidget(40, 10), 'padding', 'padding'),
                 Cell(MockWidget(30, 15), 'padding', 'padding')]
        for cell in cells:
            cell.requestSize(True)
        # 20 + 40 + 30 = 90 for the widgets.
        my_box = boxlayout.BoxLayout(7, False)
        # Add two times 7 = 14 for the total spacing.
        # Total width: 90 + 14 = 104.
        my_box.PRIMARY_LENGTH = 'width'
        my_box.SECONDARY_LENGTH = 'height'
        my_box.PRIMARY_COORD = 'left'
        my_box.SECONDARY_COORD = 'top'
        # No padding.
        requested_size = my_box.requestSize(cells)
        self.assertEquals(requested_size, Size(104, 15))
        allocated_size = SizeAllocation((100, 200), (120, 17))
        my_box.allocateSize(allocated_size, requested_size, cells)
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
        cell1, cell2, cell3 = cells
        self.assertEquals(cell1.allocated_size,
                          SizeAllocation((100, 200), (20, 17)))
        self.assertEquals(cell2.allocated_size,
                          SizeAllocation((100+20+7, 200), (49, 17)))
        self.assertEquals(cell3.allocated_size,
                          SizeAllocation((100+20+7+49+7, 200), (37, 17)))

if __name__ == "__main__":
    unittest.main()
