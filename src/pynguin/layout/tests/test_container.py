#! /usr/bin/python
"""
Created on Nov 17, 2010

@author: Niriel
"""

import unittest
from pynguin.layout import container
from pynguin.layout.size import Size
from mock import MockWidget, MockLayout

class TestContainer(unittest.TestCase):
    """Test the layout.container module."""
    def testDocTest(self):
        """Module layout.container passes its doctests."""
        import doctest
        failures, unused = doctest.testmod(m=container)#, verbose=True)
        del unused
        self.assertEquals(failures, 0)

    def testRequestSizeForwardRequest(self):
        """Container.requestSize obeys the forward_request parameter."""
        widget1 = MockWidget(10, 20)
        widget2 = MockWidget(30, 40)
        my_container = container.Container()
        my_container.addChild(widget1, 'end')
        my_container.addChild(widget2, 'end')
        #
        my_container._layout = MockLayout()
        my_container.requestSize(True)
        requested_size = my_container.requested_size
        self.assertEquals(requested_size, Size(40, 60))
        #
        widget1.width = 20
        my_container.requestSize(False)
        requested_size = my_container.requested_size
        self.assertEquals(requested_size, Size(40, 60))
        #
        widget1.requestSize(True) # True/False doesn't matter here.
        my_container.requestSize(False)
        requested_size = my_container.requested_size
        self.assertEquals(requested_size, Size(50, 60))
        #
        widget2.width = 40
        my_container.requestSize(True)
        requested_size = my_container.requested_size
        self.assertEquals(requested_size, Size(60, 60))

    def testMaxChildren(self):
        """Container.max_children is checked when adding a child."""
        widget1 = MockWidget(10, 20)
        widget2 = MockWidget(30, 40)
        my_container = container.Container()
        my_container.max_children = 1
        my_container.addChild(widget1, 'end')
        self.assertRaises(container.ContainerError,
                          my_container.addChild,
                          widget2, 'end')
        my_container.max_children = -1 # No limit.
        my_container.addChild(widget2, 'end')

if __name__ == "__main__":
    unittest.main()
