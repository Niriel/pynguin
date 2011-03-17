#! /usr/bin/python
"""
Created on Dec 12, 2010

@author: Niriel
"""

from size import Size
from size import SizeAllocation
from layout import Layout

__all__ = ['WindowLayout']

class WindowLayout(Layout):
    """A WindowLayout manages only one cell and sets its position to (0, 0).

    The idea of a window is that the children they contain have their position
    relative to that window and not the screen or anything else.

    The WindowLayout layout is made for Bin objects: objects that have only one
    cell.

    Therefore, the position of the child in the window is always (0, 0).

    """

    def requestSize(self, children):
        """Return the max."""
        requested_size = Size(0, 0)
        for child in children:
            requested_size |= child.requested_size
        return requested_size

    def allocateSize(self, allocated_size, requested_size, cells):
        """Windows subtract their position from the child's position.

        As a result, the position of the child is always (0, 0).

        """
        for child in cells:
            cell_size = SizeAllocation((0, 0), allocated_size.size)
            child.allocateSize(cell_size)
