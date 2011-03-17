#! /usr/bin/python
"""
Created on Nov 4, 2010

@author: Niriel
"""


import unittest
from pynguin.layout import sizeable, size
from mock import MockWidget

class TestSizeable(unittest.TestCase):
    """Test the layout.sizeable module."""

    def testDocTest(self):
        """Module layout.sizeable passes its doctests."""
        import doctest
        failures, tests = doctest.testmod(m=sizeable)
        del tests # Just to remove the eclipse warning on the unused variable.
        self.assertEquals(failures, 0)

    def testNegotiateSize(self):
        """Sizeable.negotiateSize allocates what it requests."""
        widget = MockWidget(32, 16)
        self.assertFalse(widget.requested_size)
        self.assertFalse(widget.allocated_size)
        widget.negotiateSize(True)
        self.assertTrue(widget.requested_size)
        self.assertTrue(widget.allocated_size)
        self.assertEquals(widget.allocated_size.size, widget.requested_size)
        self.assertEquals(widget.allocated_size.pos, size.Pos(0, 0))
        # Check that the position is maintained.
        widget.allocated_size.width = 0
        widget.allocated_size.height = 0
        widget.allocated_size.left = 100
        widget.allocated_size.top = 200
        widget.negotiateSize(True)
        self.assertEquals(widget.allocated_size.size, widget.requested_size)
        self.assertEquals(widget.allocated_size.pos, size.Pos(100, 200))

    def testExpand(self):
        """Sizeable.allocateSize checks the expandability."""
        big_width = size.SizeAllocation((0, 0), (100, 20))
        big_height = size.SizeAllocation((0, 0), (10, 200))
        widget = MockWidget(10, 20)
        widget.requestSize(True)

        widget.can_expand_width = False
        widget.can_expand_height = False
        self.assertRaises(sizeable.ExpandError,
                          widget.allocateSize, big_width)
        self.assertRaises(sizeable.ExpandError,
                          widget.allocateSize, big_height)

        widget.can_expand_width = True
        widget.can_expand_height = False
        widget.allocateSize(big_width)
        self.assertRaises(sizeable.ExpandError,
                          widget.allocateSize, big_height)

        widget.can_expand_width = False
        widget.can_expand_height = True
        self.assertRaises(sizeable.ExpandError,
                          widget.allocateSize, big_width)
        widget.allocateSize(big_height)

        widget.can_expand_width = True
        widget.can_expand_height = True
        widget.allocateSize(big_width)
        widget.allocateSize(big_height)

#if __name__ == "__main__":
#    unittest.main()
