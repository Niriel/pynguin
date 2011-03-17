#! /usr/bin/python
"""
Created on Dec 12, 2010

@author: Niriel
"""

from size import SizeAllocation
from windowlayout import WindowLayout

__all__ = ['ScrollLayout']

class ScrollLayout(WindowLayout):
    """A Scroll Layout allows its content to be bigger than itself."""
    def allocateSize(self, allocated_size, requested_size, children):
        """The child of a scroll cannot be smaller than its requested size.

        Like any Sizeable object, the ScrollLayout object does obey to
        allocateSize and sets its size to the allocated size.  However, in the
        specific case of a ScrollLayout object, the allocated size only affects
        what will be visible on the screen once the GUI is drawn.  The content
        of the ScrollLayout object may very well be wider or higher than that,
        and that is perfectly valid: that is the very purpose of the
        ScrollLayout object: instead of shrinking the content to fit the
        allocated size, provide the user with a mean of scrolling to see all
        the content.

        In short, the content of a ScrollLayout is always at least as big as
        the scroll itself.

        """
        max_size = allocated_size.size | requested_size
        for child in children:
            child.allocateSize(SizeAllocation((0, 0), max_size))
