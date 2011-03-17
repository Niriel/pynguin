#! /usr/bin/python
"""
Created on Mar 17, 2011

@author: Niriel
"""

import unittest
from pynguin.layout import borderlayout
from pynguin.layout.size import SizeAllocation
from mock import MockWidget

# pylint: disable-msg=R0904
# Because unit tests have tons of public methods and that's normal. 

# pylint: disable-msg=W0212
# Because I know what I'm doing when I use a protected attribute in a test.


class Test(unittest.TestCase):
    """Test the borderlayout module."""
    def testInitNothing(self):
        """BorderLayout.__init__ sets everything to 0 if no parameter."""
        my_layout = borderlayout.BorderLayout()
        self.assertEquals(my_layout.left, 0)
        self.assertEquals(my_layout.top, 0)
        self.assertEquals(my_layout.right, 0)
        self.assertEquals(my_layout.bottom, 0)

    def testInitInt(self):
        """BorderLayout.__init__ sets margins to the provided int."""
        my_layout = borderlayout.BorderLayout(42)
        self.assertEquals(my_layout.left, 42)
        self.assertEquals(my_layout.top, 42)
        self.assertEquals(my_layout.right, 42)
        self.assertEquals(my_layout.bottom, 42)

    def testInitTupleOne(self):
        """BorderLayout.__init__ sets margins to the provided 1-tuple."""
        my_layout = borderlayout.BorderLayout((42,))
        self.assertEquals(my_layout.left, 42)
        self.assertEquals(my_layout.top, 42)
        self.assertEquals(my_layout.right, 42)
        self.assertEquals(my_layout.bottom, 42)

    def testInitTupleTwo(self):
        """BorderLayout.__init__ sets margins to the provided 2-tuple."""
        my_layout = borderlayout.BorderLayout((1, 2))
        self.assertEquals(my_layout.left, 1)
        self.assertEquals(my_layout.top, 2)
        self.assertEquals(my_layout.right, 1)
        self.assertEquals(my_layout.bottom, 2)

    def testInitTupleThree(self):
        """BorderLayout.__init__ sets margins to the provided 4-tuple."""
        my_layout = borderlayout.BorderLayout((1, 2, 3, 4))
        self.assertEquals(my_layout.left, 1)
        self.assertEquals(my_layout.top, 2)
        self.assertEquals(my_layout.right, 3)
        self.assertEquals(my_layout.bottom, 4)

    def testInitTupleWrong(self):
        """BorderLayout.__init__ sets margins to the provided 2-tuple."""
        self.assertRaises(ValueError, borderlayout.BorderLayout,
                          (1, 2, 3))

    def testRequestSize(self):
        """BorderLayout.requestSize adds its margins to the child's size."""
        my_layout = borderlayout.BorderLayout((1, 2, 3, 4))
        child = MockWidget(10, 20)
        child.requestSize(True)
        requested_size = my_layout.requestSize([child])
        self.assertEquals(requested_size.asTuple(), (14, 26))

    def testAllocateSizeIdeal(self):
        """BorderLayout.allocateSize in ideal case."""
        my_layout = borderlayout.BorderLayout((1, 2, 3, 4))
        child = MockWidget(10, 20)
        child.requestSize(True)
        requested_size = my_layout.requestSize([child])
        allocated_size = SizeAllocation((100, 200), requested_size)
        my_layout.allocateSize(allocated_size, requested_size, [child])
        child_size = child.allocated_size
        self.assertEquals(child_size.pos.asTuple(), (101, 202))
        self.assertEquals(child_size.size.asTuple(), (10, 20))

    def testAllocateSizeTooBigExpand(self):
        """BorderLayout.allocateSize expands the child."""
        my_layout = borderlayout.BorderLayout((1, 2, 3, 4))
        child = MockWidget(10, 20)
        child.can_expand_width = True
        child.can_expand_height = True
        child.requestSize(True)
        allocated_size = SizeAllocation((100, 200), (30, 50))
        my_layout.allocateSize(allocated_size, None, [child])
        child_size = child.allocated_size
        # The child expands, so only its size changes.  Its location doesn't.
        self.assertEquals(child_size.pos.asTuple(), (101, 202))
        self.assertEquals(child_size.size.asTuple(), (30 - 4, 50 - 6))

    def testAllocateSizeTooBigNoExpand(self):
        """BorderLayout.allocateSize expands the margins."""
        my_layout = borderlayout.BorderLayout((1, 2, 3, 4))
        child = MockWidget(10, 20)
        child.can_expand_width = False
        child.can_expand_height = False
        child.requestSize(True)
        allocated_size = SizeAllocation((100, 200), (30, 50))
        my_layout.allocateSize(allocated_size, None, [child])
        child_size = child.allocated_size
        # The child does not expand: its size is nominal but the position not.
        #
        # Horizontal margin: 30 - 10 = 20.
        # The original margins are 1 and 3, total 4.
        # ratio = 20 / 4 = 5.
        # New margins are 1 * 5 = 5 and 3 * 5 = 15.
        # Check: 5 + 15 = 50.
        # The child's left is after the first margin: 5.
        #
        # Vertical margin: 50 - 20 = 30.
        # The original margins are 2 and 4, total 6.
        # ratio = 30 / 6 = 5.
        # New margins are 2 * 5 = 10 and 4 * 5 = 20.
        # Check: 10 + 20 = 30.
        # The child's top is after the first margin: 10.
        self.assertEquals(child_size.pos.asTuple(), (105, 210))
        self.assertEquals(child_size.size.asTuple(), (10, 20))

    def testAllocateSizeTooSmall(self):
        """BorderLayout.allocateSize reduces the size of the child."""
        my_layout = borderlayout.BorderLayout((1, 2, 3, 4))
        child = MockWidget(10, 20)
        child.requestSize(True)
        allocated_size = SizeAllocation((100, 200), (5, 10))
        my_layout.allocateSize(allocated_size, None, [child])
        child_size = child.allocated_size
        self.assertEquals(child_size.pos.asTuple(), (101, 202))
        self.assertEquals(child_size.size.asTuple(), (1, 4))

    def testAllocateSizeWayTooSmall(self):
        """BorderLayout.allocateSize reduces the size of the child and margin.

        """
        my_layout = borderlayout.BorderLayout((1, 2, 3, 4))
        child = MockWidget(10, 20)
        child.requestSize(True)
        allocated_size = SizeAllocation((100, 200), (2, 3))
        my_layout.allocateSize(allocated_size, None, [child])
        child_size = child.allocated_size
        self.assertEquals(child_size.pos.asTuple(), (101, 201))
        self.assertEquals(child_size.size.asTuple(), (0, 0))


if __name__ == "__main__":
    unittest.main()
