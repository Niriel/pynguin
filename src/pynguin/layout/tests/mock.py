#! /usr/bin/python
"""
Created on Dec 13, 2010

@author: delforge
"""

from pynguin.layout.size import Size
from pynguin.layout.parentable import Parentable

__all__ = ['MockWidget']

class MockWidget(Parentable):
    """A pseudo GUI element implementing only what I need for test."""
    def __init__(self, width, height):
        """Initialize the new MockWidget and give it a size."""
        Parentable.__init__(self)
        self.width = width
        self.height = height
        self.requested_size = None
        self.allocated_size = None
    def requestSize(self):
        """Return the size given to the constructor."""
        self.requested_size = Size(self.width, self.height)
    def allocateSize(self, allocated_size):
        """Store the allocated size."""
        self.allocated_size = allocated_size
