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

#if __name__ == "__main__":
#    unittest.main()
