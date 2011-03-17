#! /usr/bin/python
"""
Created on Nov 9, 2010

@author: Niriel
"""

# pylint: disable-msg=R0902
# Because too many instance attributes is acceptable in a test.

# pylint: disable-msg=R0904
# Because too many public methods is acceptable in a test.

import unittest
from pynguin.layout.size import Size
from pynguin.layout.size import SizeAllocation
from pynguin.layout.size import Pos
from pynguin.layout.sizeable import ExpandError
from pynguin.layout import boxlayout
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

class TestHBoxLayout(unittest.TestCase):
    """Test the HBoxLayout."""
    def setUp(self):
        """Prepare the children for the test."""
        self.widget1 = MockWidget(20, 10)
        self.widget2 = MockWidget(40, 10)
        self.widget3 = MockWidget(30, 15)
        self.widget1.can_expand_width = True
        self.widget1.can_expand_height = True
        self.widget2.can_expand_width = False
        self.widget2.can_expand_height = True
        self.widget3.can_expand_width = True
        self.widget3.can_expand_height = True
        self.children = [self.widget1, self.widget2, self.widget3]
        for child in self.children:
            child.requestSize(True)
        self.homo_box = boxlayout.HBoxLayout(7, True)
        self.hetero_box = boxlayout.HBoxLayout(7, False)

    def testRequestSizeHeterogeneous(self):
        """HBoxLayout.requestSize heterogeneous works."""
        requested_size = self.hetero_box.requestSize(self.children)
        # Width: 20+40+30 = 90.
        #     Plus 2*7 of spacing = 104.
        # Height: the biggest is 15.
        self.assertEquals(requested_size, Size(104, 15))

    def testRequestSizeHomogeneous(self):
        """HBoxLayout.requestSize homogeneous works."""
        requested_size = self.homo_box.requestSize(self.children)
        # Width: the biggest is 40.
        #     Time 3 widget = 120.
        #     Plus 2*7 of spacing = 134.
        # Height: the biggest is 15.
        self.assertEquals(requested_size, Size(134, 15))

    def testIdealHeterogeneous(self):
        """HBoxLayout.allocateSize ideal heterogeneous works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(20, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(40, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(30, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(227, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(274, 100))

    def testIdealHomogeneous(self):
        """HBoxLayout.allocateSize ideal homogeneous works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(40, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(40, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(40, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(247, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(294, 100))

    def testInflateButNoExpand(self):
        """HBoxLayout.allocateSize breaks if inflate non-expandable."""
        self.widget1.can_expand_width = False
        self.widget2.can_expand_width = False
        self.widget3.can_expand_width = False
        #
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.width += 100
        self.assertRaises(ExpandError, self.homo_box.allocateSize,
                          allocated_size, requested_size, self.children)
        #
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.width += 100
        self.assertRaises(ExpandError, self.hetero_box.allocateSize,
                          allocated_size, requested_size, self.children)

    def testInflateHeterogeneousPrimary(self):
        """HBoxLayout.allocateSize inflate heterogeneous primary works."""
        requested_size = self.hetero_box.requestSize(self.children) # (104, 15)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.width += 52 # ((200, 100), (156, 15))
        # Original size: 20 + 40 + 30   +   2 * 7 = 104
        # I give 52 more to the expandable children.
        # Homothecy : (20+30+52) / (20+30) = 102/50
        # 20*102/50 = 40.8 = 41
        # 30*102/50 = 61.2 = 61
        # Good: 41 + 61 = 20 + 30 + 52 = 102
        # 102 + 40 + 2 * 7 = 156
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(41, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(40, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(61, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(248, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(295, 100))

    def testInflateHomogeneousPrimary(self):
        """HBoxLayout.allocateSize inflate homogeneous primary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.width += 30
        # The homogeneous box will need all the widgets to be expandable in
        # this case.
        self.widget2.can_expand_width = True
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(50, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(50, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(50, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(257, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(314, 100))

    def testInflateHeterogeneousSecondary(self):
        """HBoxLayout.allocateSize inflate heterogeneous secondary works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.height += 10
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(20, 25))
        self.assertEqual(self.widget2.allocated_size.size, Size(40, 25))
        self.assertEqual(self.widget3.allocated_size.size, Size(30, 25))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(227, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(274, 100))

    def testInflateHomogeneousSecondary(self):
        """HBoxLayout.allocateSize inflate homogeneous secondary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.height += 10
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(40, 25))
        self.assertEqual(self.widget2.allocated_size.size, Size(40, 25))
        self.assertEqual(self.widget3.allocated_size.size, Size(40, 25))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(247, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(294, 100))

    def testShrinkABitHeterogeneourPrimary(self):
        """HBoxLayout.allocateSize shrink a bit heterogeneous primary works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.width -= 30
        # Requested children: 20 + 40 + 30 = 90
        # I remove 30 to the requested total.
        # Allocated for the children: 60.
        # Zoom factor: 60 / 90.
        # 20 * 60 / 90 = 13
        # 40 * 60 / 90 = 27
        # 30 * 60 / 90 = 20
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(13, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(27, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(20, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(220, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(254, 100))

    def testShrinkABitHomogeneousPrimary(self):
        """HBoxLayout.allocateSize shrink a bit homogeneous primary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.width -= 30
        # Requested children: 20, 40, 30, bigger = 40.
        # Requested total: 40 + 40 + 40 = 120.
        # I remove 30 to the requested total.
        # Allocated total = 90.
        # So each cell is going to get 90 / 3 = 30.
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(30, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(30, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(30, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(237, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(274, 100))

    def testShrinkALotHeterogeneousPrimary(self):
        """HBoxLayout.allocateSize shrink a lot heterogeneous primary works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.width = 10
        # 10 is not even enough to hold the spacing.  The children should have
        # a width of 0. Now we have to shrink the spacing.  Its length is 7.
        # There are two spacings: 7, 7 for a total of 14.  We apply a homothecy
        # to make it fit into 10. 7 * 10 / 14 = 5. 14*10/14=10. So we get 5 and
        # 10 for coords out of the homothecy, and therefore 5 and 5 for the
        # lengths of the spacing.  We don't care about the lengths but we are
        # interested in the coords since they give us the positions of our
        # children.  Just add a 0 in front of the list:  0, 5, 10.
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(205, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(210, 100))

    def testShrinkALotHomogeneousPrimary(self):
        """HBoxLayout.allocateSize shrink a lot homogeneous primary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.width = 10
        # 10 is not even enough to hold the spacing.  The children should have
        # a width of 0. Now we have to shrink the spacing.  Its length is 7.
        # There are two spacings: 7, 7 for a total of 14.  We apply a homothecy
        # to make it fit into 10. 7 * 10 / 14 = 5. 14*10/14=10. So we get 5 and
        # 10 for coords out of the homothecy, and therefore 5 and 5 for the
        # lengths of the spacing.  We don't care about the lengths but we are
        # interested in the coords since they give us the positions of our
        # children.  Just add a 0 in front of the list:  0, 5, 10.
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(205, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(210, 100))

    def testShrinkTotallyHeterogeneousPrimary(self):
        """HBoxLayout.allocateSize shrink totally heterogeneous primary works.

        """
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.width = 0
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(200, 100))

    def testShrinkTotallyHomogeneousPrimary(self):
        """HBoxLayout.allocateSize shrink totally homogeneous primary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.width = 0
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget2.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget3.allocated_size.size, Size(0, 15))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(200, 100))

    def testShrinkHeterogeneousSecondary(self):
        """HBoxLayout.allocateSize shrink heterogeneous secondary works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.height = 5
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(20, 5))
        self.assertEqual(self.widget2.allocated_size.size, Size(40, 5))
        self.assertEqual(self.widget3.allocated_size.size, Size(30, 5))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(227, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(274, 100))

    def testShrinkHomogeneousSecondary(self):
        """HBoxLayout.allocateSize shrink homogeneous secondary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.height = 5
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(40, 5))
        self.assertEqual(self.widget2.allocated_size.size, Size(40, 5))
        self.assertEqual(self.widget3.allocated_size.size, Size(40, 5))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(200, 100))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(247, 100))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(294, 100))


class TestVBoxLayout(unittest.TestCase):
    """Test the VBoxLayout."""
    def setUp(self):
        """Prepare the children for the test."""
        self.widget1 = MockWidget(10, 20)
        self.widget2 = MockWidget(10, 40)
        self.widget3 = MockWidget(15, 30)
        self.widget1.can_expand_width = True
        self.widget1.can_expand_height = True
        self.widget2.can_expand_width = True
        self.widget2.can_expand_height = False
        self.widget3.can_expand_width = True
        self.widget3.can_expand_height = True
        self.children = [self.widget1, self.widget2, self.widget3]
        for cell in self.children:
            cell.requestSize(True)
        self.homo_box = boxlayout.VBoxLayout(7, True)
        self.hetero_box = boxlayout.VBoxLayout(7, False)

    def testRequestSizeHeterogeneous(self):
        """VBoxLayout.requestSize heterogeneous works."""
        requested_size = self.hetero_box.requestSize(self.children)
        # Height: 20+40+30 = 90.
        #     Plus 2*7 of spacing = 104.
        # Width: the biggest is 15.
        self.assertEquals(requested_size, Size(15, 104))

    def testRequestSizeHomogeneous(self):
        """VBoxLayout.requestSize homogeneous works."""
        requested_size = self.homo_box.requestSize(self.children)
        # Height: the biggest is 40.
        #     Time 3 widget = 120.
        #     Plus 2*7 of spacing = 134.
        # Width: the biggest is 15.
        self.assertEquals(requested_size, Size(15, 134))

    def testIdealHeterogeneous(self):
        """VBoxLayout.allocateSize ideal heterogeneous works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 20))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 40))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 30))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 227))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 274))

    def testIdealHomogeneous(self):
        """VBoxLayout.allocateSize ideal homogeneous works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 40))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 40))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 40))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 247))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 294))

    def testInflateButNoExpand(self):
        """VBoxLayout.allocateSize breaks if inflate non-expandable."""
        self.widget1.can_expand_height = False
        self.widget2.can_expand_height = False
        self.widget3.can_expand_height = False
        #
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.height += 100
        self.assertRaises(ExpandError, self.homo_box.allocateSize,
                          allocated_size, requested_size, self.children)
        #
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((200, 100), requested_size)
        allocated_size.height += 100
        self.assertRaises(ExpandError, self.hetero_box.allocateSize,
                          allocated_size, requested_size, self.children)

    def testInflateHeterogeneousPrimary(self):
        """VBoxLayout.allocateSize inflate heterogeneous primary works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.height += 52
        # Original size: 20 + 40 + 30   +   2 * 7 = 104
        # I give 52 more to the expandable children.
        # Homothecy : (20 + 30 + 52) / (20 + 30) = 102 / 50
        # 20 * 102 / 50 = 40.8 = 41
        # 30 * 102 / 50 = 61.2 = 61
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 41))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 40))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 61))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 248))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 295))

    def testInflateHomogeneousPrimary(self):
        """VBoxLayout.allocateSize inflate homogeneous primary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.height += 30
        # The homogeneous box will need all the widgets to be expandable in
        # this case.
        self.widget2.can_expand_height = True
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 50))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 50))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 50))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 257))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 314))

    def testInflateHeterogeneousSecondary(self):
        """VBoxLayout.allocateSize inflate heterogeneous secondary works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.width += 10
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(25, 20))
        self.assertEqual(self.widget2.allocated_size.size, Size(25, 40))
        self.assertEqual(self.widget3.allocated_size.size, Size(25, 30))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 227))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 274))

    def testInflateHomogeneousSecondary(self):
        """VBoxLayout.allocateSize inflate homogeneous secondary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.width += 10
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(25, 40))
        self.assertEqual(self.widget2.allocated_size.size, Size(25, 40))
        self.assertEqual(self.widget3.allocated_size.size, Size(25, 40))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 247))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 294))

    def testShrinkABitHeterogeneourPrimary(self):
        """VBoxLayout.allocateSize shrink a bit heterogeneous primary works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.height -= 30
        # Requested children: 20 + 40 + 30 = 90
        # I remove 30 to the requested total.
        # Allocated for the children: 60.
        # Zoom factor: 60 / 90.
        # 20 * 60 / 90 = 13
        # 40 * 60 / 90 = 27
        # 30 * 60 / 90 = 20
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 13))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 27))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 20))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 220))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 254))

    def testShrinkABitHomogeneousPrimary(self):
        """VBoxLayout.allocateSize shrink a bit homogeneous primary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.height -= 30
        # Requested children: 20, 40, 30, bigger = 40.
        # Requested total: 40 + 40 + 40 = 120.
        # I remove 30 to the requested total.
        # Allocated total = 90.
        # So each cell is going to get 90 / 3 = 30.
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 30))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 30))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 30))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 237))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 274))

    def testShrinkALotHeterogeneousPrimary(self):
        """VBoxLayout.allocateSize shrink a lot heterogeneous primary works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.height = 10
        # 10 is not even enough to hold the spacing.  The children should have
        # a width of 0. Now we have to shrink the spacing.  Its length is 7.
        # There are two spacings: 7, 7 for a total of 14.  We apply a homothecy
        # to make it fit into 10. 7 * 10 / 14 = 5. 14*10/14=10. So we get 5 and
        # 10 for coords out of the homothecy, and therefore 5 and 5 for the
        # lengths of the spacing.  We don't care about the lengths but we are
        # interested in the coords since they give us the positions of our
        # children.  Just add a 0 in front of the list:  0, 5, 10.
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 205))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 210))

    def testShrinkALotHomogeneousPrimary(self):
        """VBoxLayout.allocateSize shrink a lot homogeneous primary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.height = 10
        # 10 is not even enough to hold the spacing.  The children should have
        # a width of 0. Now we have to shrink the spacing.  Its length is 7.
        # There are two spacings: 7, 7 for a total of 14.  We apply a homothecy
        # to make it fit into 10. 7 * 10 / 14 = 5. 14*10/14=10. So we get 5 and
        # 10 for coords out of the homothecy, and therefore 5 and 5 for the
        # lengths of the spacing.  We don't care about the lengths but we are
        # interested in the coords since they give us the positions of our
        # children.  Just add a 0 in front of the list:  0, 5, 10.
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 205))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 210))

    def testShrinkTotallyHeterogeneousPrimary(self):
        """VBoxLayout.allocateSize shrink totally heterogeneous primary works.

        """
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.height = 0
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 200))

    def testShrinkTotallyHomogeneousPrimary(self):
        """VBoxLayout.allocateSize shrink totally homogeneous primary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.height = 0
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget2.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget3.allocated_size.size, Size(15, 0))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 200))

    def testShrinkHeterogeneousSecondary(self):
        """VBoxLayout.allocateSize shrink heterogeneous secondary works."""
        requested_size = self.hetero_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.width = 5
        self.hetero_box.allocateSize(allocated_size, requested_size,
                                     self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(5, 20))
        self.assertEqual(self.widget2.allocated_size.size, Size(5, 40))
        self.assertEqual(self.widget3.allocated_size.size, Size(5, 30))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 227))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 274))

    def testShrinkHomogeneousSecondary(self):
        """VBoxLayout.allocateSize shrink homogeneous secondary works."""
        requested_size = self.homo_box.requestSize(self.children)
        allocated_size = SizeAllocation((100, 200), requested_size)
        allocated_size.width = 5
        self.homo_box.allocateSize(allocated_size, requested_size,
                                   self.children)
        self.assertEqual(self.widget1.allocated_size.size, Size(5, 40))
        self.assertEqual(self.widget2.allocated_size.size, Size(5, 40))
        self.assertEqual(self.widget3.allocated_size.size, Size(5, 40))
        self.assertEqual(self.widget1.allocated_size.pos, Pos(100, 200))
        self.assertEqual(self.widget2.allocated_size.pos, Pos(100, 247))
        self.assertEqual(self.widget3.allocated_size.pos, Pos(100, 294))


if __name__ == "__main__":
    unittest.main()
