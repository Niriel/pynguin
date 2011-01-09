#! /usr/bin/python
"""
Created on Dec 13, 2010

@author: delforge
"""

from pynguin.layout.size import Size
from pynguin.layout.sizeable import Sizeable
from pynguin.layout.parentable import Parentable
from pynguin.layout.layout import Layout

__all__ = ['MockWidget']

class MockWidget(Sizeable, Parentable):
    """A pseudo GUI element implementing only what I need for test."""
    def __init__(self, width, height):
        """Initialize the new MockWidget and give it a size."""
        Sizeable.__init__(self)
        Parentable.__init__(self)
        self.width = width
        self.height = height
        self.requested_size = None
        self.allocated_size = None
    def requestSize(self, forward_request):
        """Return the size given to the constructor."""
        self.requested_size = Size(self.width, self.height)
    def allocateSize(self, allocated_size):
        """Store the allocated size."""
        self.allocated_size = allocated_size

class MockLayout(Layout):
    """A pseudo container layout implementing just what I need for tests."""
    def requestSize(self, cells):
        """Adds the sizes of the cells.  It means nothing, just for test."""
        size = Size(0, 0)
        for cell in cells:
            size += cell.requested_size
        return size
